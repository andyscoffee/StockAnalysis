# 셀트리온 종가 차트

import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

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
    url = '{}&page={}'.format(sise_url, page)
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    # df = df.append(pd.read_html(html, header=0)[0]) <- 책의 소스 코드
    # 판다스 데이터프레임에서 concat 함수 권장하길래 바꿔봄
    df = pd.concat([df, pd.read_html(html, header=0)[0]])

df = df.dropna()
df = df.iloc[0:30]  # 데이터가 너무 많기에 최근 30개만 사용
df = df.sort_values(by='날짜')  # 네이버 금융의 데이터가 내림차순 정렬이기에 오름차순으로 변경

plt.title('Celltrion (close)')
plt.xticks(rotation=45)  # x축 레이블의 날짜가 겹쳐서 보기 어렵기에 90도 회전
# x축은 날짜, y축은 종가, co는 좌표를 청록색 원으로, -는 각 좌표를 실선으로 연결해서 표시
plt.plot(df['날짜'], df['종가'], 'co-')
plt.grid(color='gray', linestyle='--')
plt.show()
