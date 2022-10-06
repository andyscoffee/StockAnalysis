import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from matplotlib import pyplot as plt


krx_list = pd.read_html(
    'C:/Users/monar/Desktop/Python_Workspace/DataAnalysis/Pyhthon_StockAnaysis/상장법인목록.xls')  # 다운로드받은 엑셀파일에서 읽어오기
krx_list[0].종목코드 = krx_list[0].종목코드.map('{:06d}'.format)  # 종목코드의 자리수 6자리로 통일
# print(krx_list[0])

df = pd.read_html(
    'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13')[0]  # url에서 바로 읽어오기
df['종목코드'] = df['종목코드'].map('{:06d}'.format)
df = df.sort_values(by='종목코드')
# print(df)

# 4.4.3 맨 뒤 페이지 숫자 구하기
"""
url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
with urlopen(url) as doc:
    # 뷰티풀 수프 생성자의 첫번째 인수로 html/xml페이지의 파일 경로나 url을 넘겨주고, 두번째 인수로 웹 페이지를 파싱할 방법을 알려줌
    html = BeautifulSoup(doc, 'lxml')
    # find함수를 통해서 클래스 속성이 prRR인 td태그를 찾으면, 결과값은 bs4.element.Tag타입으로 pgrr(Page Right Right)변수에 반환, class_로 지은 이유는 파이썬에 이미 class라는 지시어가 존재하기 때문에
    pgrr = bs.find('td', class_='pgRR')
    # <td> 태그 하부 <a>태그의 href 속성값인 item/sise_day.nhn?code=068270&page= 문자열을 얻을 수 있음
    # print(pgrr.a['href'])
    s = str(pgrr.a['href']).split('=')
    # pgrr.a['href']로 구한 문자열을 '='기준으로 분리해 리스트를 얻고, 리스트의 마지막 원소가 구하려는 전채 페이지 수임
    last_page = s[-1]
네이버 금융 서버에서 http 패킷 헤더의 웹 브라우저 정보(User-Agent)를 체크하기 때문에, 
웹 스크레이핑을 하려면 requests 라이브러리를 이용해 웹 브라우저 정보를 보내야 합니다. 
"""
# 4.4.3_new 맨 뒤 페이지 숫자 구하기
url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
bs = BeautifulSoup(html, 'lxml')
pgrr = bs.find('td', class_='pgRR')
s = str(pgrr.a['href']).split('=')
last_page = s[-1]

# 4.4.4 전체 페이지 읽어오기
df = pd.DataFrame()  # 일별 시세를 저장할 dataframe
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'
for page in range(1, int(last_page)+1):  # 1페이지부터 마지막 페이지까지 반복
    """page_url = '{}&page'.format(sise_url, page)  # page변수를 이용해 요청할 url페이지 수를 변경
    # read_html함수로 읽은 한 페이지 분량의 데이터프레임을 df에 추가
    df = df.append(pd.read_html(page_url, header=0)[0])
    여기도 새로운 방식 필요
    """
    url = '{}&page={}'.format(sise_url, page)
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    df = df.append(pd.read_html(html, header=0)[0])

df = df.dropna()  # 값이 빠진 행을 제거
print(df)
