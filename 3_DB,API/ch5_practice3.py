# sql 관련

import pymysql

connection = pymysql.connect(host='localhost', port=3306, db='INVESTAR',
                             user='root', passwd='forsaproject', autocommit=True)  # 오토커밋 인수를 T로 바꿔 commit()함수를 호출하지 않아도 결과가 반영
cursor = connection.cursor()  # 커서 객체를 생성해 SQL문 실행 가능
cursor.execute("SELECT VERSION();")  # SQL문 실행(마리아디비 버전 확인)
result = cursor.fetchone()  # 위의 수행 결과를 튜플로 받음

print("MariaDB version : {}".format(result))

connection.close()
