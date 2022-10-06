# 셀트리온 캔들 차트 신버전(새로운 방식)

from matplotlib.pyplot import ylabel
import pandas as pd
from bs4 import BeautifulSoup
from pyparsing import col
import requests
import mplfinance as mpf

# 4.4.3_new 맨 뒤 페이지 숫자 구하기
url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
bs = BeautifulSoup(html, 'lxml')
pgrr = bs.find('td', class_='pgRR')
s = str(pgrr.a['href']).split('=')
last_page = s[-1]

# 4.4.4 전체 페이지 읽어오기
df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'
for page in range(1, int(last_page)+1):
    url = '{}&page={}'.format(sise_url, page)
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    df = pd.concat([df, pd.read_html(html, header=0)[0]])

# 차트 출력을 위한 데이터프레임 가공
df = df.dropna()
df = df.iloc[0:30]
df = df.rename(columns={'날짜': 'Date', '시가': 'Open',  # 영문 칼럼명으로 변경
               '고가': 'High', '저가': 'Low', '종가': 'Close', '거래량': 'Volume'})
df = df.sort_values(by='Date')
df.index = pd.to_datetime(df.Date)
# Open, High, Low, Close, Volume 칼럼만 갖도록 데이터프레임 구조 변경
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

# 셀트리온 시세 데이터를 첫번째 인수로 넘겨주며 캔들 차트 형태로 출력
mpf.plot(df, title='Celltrion candle chart', type='candle')
"""
import mplfinance
mplfinance.plot(OHLC데이터프레임, [,title=차트제목][,type=차트형태]
                [,mav=이동평균선][,volume=거래량 표시 여부][,ylabel=y축레이블])
mplfinance(신버전) 사용법, mpl_finace는 구버전임
"""
mpf.plot(df, title='Celltrion candle chart',
         type='ohlc')  # ohlc 차트(미국에서 개발된 패키지이기에 사실 이게 기본형)

kwarg = dict(title='Celltrion customized chart', type='candle',
             mav=(2, 4, 6), volume=True, ylabel='ohlc candles')
# keyword arguments의 약자로 mpf.plot()함수 호출시 필요한 인수를 담는 딕셔너리
mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
# 상승은 빨간색, 하락은 파란색, 관련색상은 이를 따르도록
s = mpf.make_mpf_style(marketcolors=mc)  # 마켓 색상을 인수로 건내받은 스타일 객체
mpf.plot(df, **kwarg, style=s)  # 마켓 색상, 스타일, kwarg로 설정한 인수를 받은 차트 출력
