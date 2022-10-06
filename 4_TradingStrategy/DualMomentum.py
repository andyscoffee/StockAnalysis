from multiprocessing import connection
from tracemalloc import start
import pandas as pd
import pymysql
from datetime import datetime
from datetime import timedelta
import Analyzer


class DualMomentum:
    def __init__(self):
        """생성자: KRX 종목코드(codes)를 구하기 위한 MarkgetDB 객체 생성"""
        self.mk = Analyzer.MarketDB()

    def get_rltv_momentum(self, start_date, end_date, stock_count):
        """특정 기간 동안 수익률이 제일 높았던 stock_count 개의 종목들 (상대 모멘텀)
            - start_date  : 상대 모멘텀을 구할 시작일자 ('2020-01-01')   
            - end_date    : 상대 모멘텀을 구할 종료일자 ('2020-12-31')
            - stock_count : 상대 모멘텀을 구할 종목수
        """
    # 사용자로부터 시작일과 종료일을 입력받아 실제로 DB에서 조회되는 일자로 변경
        connection = pymysql.connect(
            host='localhost', port=3306, db='INVESTAR', user='root', passwd='forsaproject', autocommit=True)
        cursor = connection.cursor()

        sql = f"SELECT MAX(DATE) FROM DAILY_PRICE WHERE DATE <='{start_date}'"
        # daily_price 테이블에서 사용자가 입력한 일자와 같거나 작은 일자를 조회함으로써 실제 거래일을 구한다
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print('start_date : {} -> returned None'.format(sql))
            return
        # DB에서 조회된 거래일을 %Y-%m-%d 포맷 문자열로 변환해 사용자가 입력한 조회 시작 일수 변수에 반영
        start_date = result[0].strftime('%Y-%m-%d')

        sql = f"SELECT MAX(DATE) FROM DAILY_PRICE WHERE DATE <='{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print('end_date : {} -> returned None'.format(sql))
            return
        end_date = result[0].strftime('%Y-%m-%d')

    # 종목별 수익률 계산
        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for _, code in enumerate(self.mk.codes):
            sql = f"SELECT CLOSE FROM DAILY_PRICE WHERE CODE='{code}' and DATE = '{start_date}'"
            # start_date 일자에 해당하는 가격(old_price)을 daily_price 테이블로부터 조회
            cursor.execute(sql)
            result = cursor.fetchone()
            if (result is None):
                continue
            old_price = int(result[0])

            sql = f"SELECT CLOSE FROM DAILY_PRICE WHERE CODE='{code}' and DATE = '{end_date}'"
            # end_date 일자에 해당하는 가격(new_price)을 daily_price 테이블로부터 조회
            cursor.execute(sql)
            result = cursor.fetchone()
            if (result is None):
                continue
            new_price = int(result[0])
            returns = (new_price/old_price - 1) * 100  # 해당 종목의 수익률 계산
            # 구한 종목코드, 종목명, 구 가격, 신 가격, 수익률을 rows에 2차원 리스트 형태로 추가
            rows.append([code, self.mk.codes[code],
                        old_price, new_price, returns])
    # 상대 모멘텀 데이터프레임 생성
        # rows 리스트를 인수로 받아서 데이터프레임을 생성
        df = pd.DataFrame(rows, columns=columns)
        # 칼럼 5개만 갖도록 구조를 수정한다
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)
        df = df.head(stock_count)
        df.index = pd.Index(range(stock_count))

        connection.close()
        print(df)
        print(
            f"\nRelative mommentum ({start_date} ~ {end_date}) : {df['returns'].mean():.2f}% \n")
        return df

    def get_abs_momentum(self, rltv_momentum, start_date, end_date):
        """특정 기간 동안 상대 모멘텀에 투자했을 때의 평균 수익률 (절대 모멘텀)
            - rltv_momentum : get_rltv_momentum() 함수의 리턴값 (상대 모멘텀)
            - start_date    : 절대 모멘텀을 구할 매수일 ('2020-01-01')   
            - end_date      : 절대 모멘텀을 구할 매도일 ('2020-12-31')
        """
        stockList = list(rltv_momentum['code'])
        connection = pymysql.connect(host='localhost', port=3306,
                                     db='INVESTAR', user='root', passwd='forsaproject', autocommit=True)
        cursor = connection.cursor()

    # 사용자가 입력한 매수일을 DB에서 조회되는 일자로 변경
        sql = f"select max(date) from daily_price "\
            f"where date <= '{start_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print("{} -> returned None".format(sql))
            return
        start_date = result[0].strftime('%Y-%m-%d')

    # 사용자가 입력한 매도일을 DB에서 조회되는 일자로 변경
        sql = f"select max(date) from daily_price "\
            f"where date <= '{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print("{} -> returned None".format(sql))
            return
        end_date = result[0].strftime('%Y-%m-%d')

    # 상대 모멘텀의 종목별 수익률을 구해서 2차원 리스트 형태로 추가
        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for _, code in enumerate(stockList):
            sql = f"select close from daily_price "\
                f"where code='{code}' and date='{start_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if (result is None):
                continue
            old_price = int(result[0])
            sql = f"select close from daily_price "\
                f"where code='{code}' and date='{end_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if (result is None):
                continue
            new_price = int(result[0])
            returns = (new_price / old_price - 1) * 100
            rows.append([code, self.mk.codes[code], old_price, new_price,
                         returns])

    # 절대 모멘텀 데이터프레임을 생성한 후 수익률순으로 출력
        df = pd.DataFrame(rows, columns=columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)
        connection.close()
        print(df)
        print(f"\nAbasolute momentum ({start_date} ~ {end_date}) : "
              f"{df['returns'].mean():.2f}%")

        return


# 작동 테스트
dm = DualMomentum()
rm = dm.get_rltv_momentum('2022-05-08', '2022-08-08', 10)  # 상대 모멘텀
am = dm.get_abs_momentum(rm, '2022-05-08', '2022-08-08')  # 절대 모멘텀
