import pandas as pd
from bs4 import BeautifulSoup
import pymysql
import calendar
import time
import json
import requests
from datetime import datetime
from threading import Timer


class DBUpdater:  # 객체가 생성될 때 마리아디비에 접속하고, 소멸될 때 접속을 해제
    def __init__(self):  # 생성자: MariaDB 연결 및 종목코드 딕셔너리 생성
        self.conn = pymysql.connect(host='localhost', user='root',
                                    password='PASSWORD', db='DBNAME', charset='utf8')
        # 한글 회사명을 사용하기에 인코딩 오류 방지용 charset=utf8

        with self.conn.cursor() as curs:  # 이미 존재하는 테이블에 create table 구문 사용시 오류 발생
            sql = """
            CREATE TABLE IF NOT EXISTS company_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code))
            """
            curs.execute(sql)
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """  # code, date 복합 기본키를 사용, 기본키에는 자동으로 인덱스가 설정되므로 code, date 칼럼을 이용해 데이터 조회시 다른 칼럼에 비해 속도가 빠르다
            curs.execute(sql)
        self.conn.commit()

        self.codes = dict()
        self.update_comp_info()  # KRX 주식 코드를 읽어와 DB의 company_info 테이블에 업데이트

    def __del__(self):  # 소멸자: MariaDB 연결 해제
        self.conn.close()

    def read_krx_code(self):  # KRX로부터 상장기업 목록 파일을 읽어와서 데이터프레임으로 반환
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method='\
            'download&searchType=13'
        krx = pd.read_html(url, header=0)[0]  # 상장법인목록.xls파일을 read_html합수로 읽기
        krx = krx[['종목코드', '회사명']]  # 종목코드, 회사명 칼럼만 남기기
        # 한글 칼럼을 영문으로 변경
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        krx.code = krx.code.map('{:06d}'.format)  # 포맷 변경
        return krx

    def update_comp_info(self):  # 종목코드를 company_info 테이블에 업데이트 한 후 딕셔너리에 저장
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn)  # company_info 테이블 읽기
        for idx in range(len(df)):
            # 종목코드와 회사명을 사용한 사전 생성
            self.codes[df['code'].values[idx]] = df['company'].values[idx]

        with self.conn.cursor() as curs:
            # 가장 최신 업데이트 날짜를 가져오기
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')

            # 최신 업데이트가 존재하지 않거나 오늘보다 오래된 경우 업데이트
            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code()  # KRX 상장목록 파일을 읽어 krx 데이터프레임에 저장
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    sql = f"REPLACE INTO company_info (code, company, last"\
                        f"_update) VALUES ('{code}', '{company}', '{today}')"
                    # REPLACE INTO 구문을 이용해 '종목코드,회사명,오늘날짜'행을 DB에 저장
                    # (INSERT INTO 사용시 데이터 행이 테이블에 이미 존재하는 경우 오류 발생)
                    curs.execute(sql)
                    self.codes[code] = company  # code 사전에 키-값으로 종목코드와 회사명 추가
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] #{idx+1:04d} REPLACE INTO company_info "
                          f"VALUES ({code}, {company}, {today})")
                self.conn.commit()
                print('')
# 여기서부터 내일 시작

    def read_naver(self, code, company, pages_to_fetch):  # 네이버에서 주식 시세를 읽어서 데이터프레임으로 반환
        try:
            url = f"http://finance.naver.com/item/sise_day.nhn?code={code}"
            html = BeautifulSoup(requests.get(url,
                                              headers={'User-agent': 'Mozilla/5.0'}).text, "lxml")
            pgrr = html.find("td", class_="pgRR")
            if pgrr is None:
                return None
            s = str(pgrr.a["href"]).split('=')
            lastpage = s[-1]
            df = pd.DataFrame()
            # 설정 파일에 저장된 페이지 수와 lastpage 중 적은것을 고름
            pages = min(int(lastpage), pages_to_fetch)
            for page in range(1, pages+1):
                pg_url = '{}&page={}'.format(url, page)
                df = pd.concat([df, pd.read_html(requests.get(
                    pg_url, headers={'User-agent': 'Mozilla/5.0'}).text)[0]])  # 일별 시세 페이지를 읽어 데이터프레임에 추가
                # df = df.append(pd.read_html(requests.get(pg_url,headers={'User-agent': 'Mozilla/5.0'}).text)[0])
                # 판다스 데이터프레임에서 concat 함수 권장하기에 변경(기본 코드는 위의 코드 )
                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')  # 시간정보
                print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.
                      format(tmnow, company, code, page, pages), end="\r")
            df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff',
                           '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})  # 칼럼명 영어로 변경
            df['date'] = df['date'].replace('.', '-')  # 연.월.일 형식을 연-월-일로 변경
            df = df.dropna()
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close',
                                                                         'diff', 'open', 'high', 'low', 'volume']].astype(int)
            # BIGINT타입의 데이터를 int로 변경
            df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]
            # 칼럼 순서 조정
        except Exception as e:
            print('Exception occured :', str(e))
            return None
        return df

    def replace_into_db(self, df, num, code, company):  # 네이버에서 읽어온 주식 시세를 DB에 REPLACE
        with self.conn.cursor() as curs:
            for r in df.itertuples():  # 인수로 넘겨받은 데이터프레임을 튜플로 순회처리
                sql = f"REPLACE INTO daily_price VALUES ('{code}', "\
                    f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, "\
                    f"{r.diff}, {r.volume})"
                curs.execute(sql)  # daily_price 테이블 업데이트(REPLACE INTO 구문 사용)
            self.conn.commit()  # MariaDB에 반영
            print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_'
                  'price [OK]'.format(datetime.now().strftime('%Y-%m-%d'
                                                              ' %H:%M'), num+1, company, code, len(df)))

    def update_daily_price(self, pages_to_fetch):
        # KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트
        # self.codes 딕셔너리에 저장된 모든 종목코드 순회
        for idx, code in enumerate(self.codes):
            # read_naver 메서드 사용해 종목코드에 대한 일별 시세 df 구하기
            df = self.read_naver(code, self.codes[code], pages_to_fetch)
            if df is None:
                continue
            # 일별 시세 데이터프레임을 구하면 DB에 저장
            self.replace_into_db(df, idx, code, self.codes[code])

    def execute_daily(self):
        # 실행 즉시 및 매일 오후 다섯시에 daily_price 테이블 업데이트
        self.update_comp_info()  # 상장 법인 목록을 DB에 업데이트
        try:
            # DBUpdater.py가 있는 디렉토리에서 config.json파일을 읽기모드로 열기
            with open('config.json', 'r') as in_file:
                config = json.load(in_file)
                # 파일이 있다면 pages_to_fetch값을 읽어 사용
                pages_to_fetch = config['pages_to_fetch']
        except FileNotFoundError:  # 존재하지 않는 경우
            with open('config.json', 'w') as out_file:
                pages_to_fetch = 100  # 최초 실행 시 프로그램에서 사용할 pages_to_fetch값을 100으로 설정
                config = {'pages_to_fetch': 1}
                json.dump(config, out_file)
        # pages_to_fetch값으로 update_daily_price 메서드 호출
        self.update_daily_price(pages_to_fetch)

        tmnow = datetime.now()
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[
            1]  # 이달의 마지막 날을 구해 다음날 오후 5시를 계산하는데 사용
        if tmnow.month == 12 and tmnow.day == lastday:
            tmnext = tmnow.replace(year=tmnow.year+1, month=1, day=1,
                                   hour=17, minute=0, second=0)
        elif tmnow.day == lastday:
            tmnext = tmnow.replace(month=tmnow.month+1, day=1, hour=17,
                                   minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day+1, hour=17, minute=0,
                                   second=0)
        tmdiff = tmnext - tmnow
        secs = tmdiff.seconds
        # 다음 날 오후 5시에 execute_daily메서드를 실행하는 타이머 객체 생성
        t = Timer(secs, self.execute_daily)
        print("Waiting for next update ({}) ... ".format(tmnext.strftime
                                                         ('%Y-%m-%d %H:%M')))
        t.start()


if __name__ == '__main__':
    dbu = DBUpdater()
    dbu.execute_daily()
