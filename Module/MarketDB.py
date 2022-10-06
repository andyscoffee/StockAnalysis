import pandas as pd
import pymysql
from datetime import datetime


class MarketDB:
    def __init__(self):
        # 생성자: MariaDB 연결 및 종목코드 딕셔너리 생성
        self.conn = pymysql.connect(host='localhost', user='root',
                                    password='PASSWORD', db='DBNAME', charset='utf8')
        # 마리아디비에 접속해 인스턴트 멤버인 conn 객체 생성
        self.codes = dict()  # 인스턴트 멤버로 codes딕셔너리 생성
        self.getCompanyInfo()  # getCompanyInfo 함수를 호출해 마리아디비에서 comany_info 테이블을 읽어와 codes에 저장

    def __del__(self):
        # 소멸자: MariaDB 연결 해제
        # 사용자가 mk=MarketDB()로 객체를 생성했다면, del mk로 명시적으로 객체를 삭제해야 마리아디비와 연결이 해제
        self.conn.close()

    def getCompanyInfo(self):
        # company_info 테이블에서 읽어와서 companyData와 codes에 저장
        sql = "SELECT * FROM company_info"
        companyInfo = pd.read_sql(sql, self.conn)  # sql문 수행 결과를 데이터프레임으로 가져옴
        for idx in range(len(companyInfo)):
            self.codes[companyInfo['code'].values[idx]
                       ] = companyInfo['company'].values[idx]  # 종목코드:회사명의 형태로 가공

    def getDailyPrice(self, code, startDate, endDate):
        """daily_price 테이블에서 읽어와서 데이터프레임으로 반환"""
        sql = "SELECT * FROM daily_price WHERE code = '{}' and date >= '{}' and date <= '{}'".format(
            code, startDate, endDate)
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']  # sql문 수행 결과를 데이터프레임으로 가져오면 정수형 인덱스가 별도로 생성,
        # 따라서 df.index = df['date']로 데이터프레임의 인덱스를 date 칼럼으로 새로 설정해야 함
        return df
