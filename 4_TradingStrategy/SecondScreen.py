# 삼중창 매매 시스템 - 추세 추종과 역추세 매매범을 함께 사용, 세 단계의 창을 거쳐 더 정확한 매매 시점을 찾도록 구성
# 두 번째 창 - 첫 번째 창의 추세 방향과 역행하는 파도를 파악하는데 오실레이터를 활용
# 오실레이터는 시장이 하락할 때 매수 기회를 제공, 시장이 상승할 때 매도 기회를 제공

import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('한화', '2017-01-01')

ema60 = df.close.ewm(span=60).mean()
ema130 = df.close.ewm(span=130).mean()
macd = ema60-ema130
signal = macd.ewm(span=45).mean()
macdhist = macd - signal

df = df.assign(ema130=ema130, ema60=ema60, macd=macd,
               signal=signal, macdhist=macdhist).dropna()
df['number'] = df.index.map(mdates.date2num)
ohlc = df[['number', 'open', 'high', 'low', 'close']]

# 14일간의 최댓값 구하기, min_periods=1 지정할 경우 데이터가 144일 미만이어도 최댓값을 구함
ndays_high = df.high.rolling(window=14, min_periods=1).max()
ndays_low = df.low.rolling(window=14, min_periods=1).min()  # 최솟값 구하기
fast_k = (df.close-ndays_low) / (ndays_high-ndays_low) * 100  # 빠른선 %K 구하기
slow_d = fast_k.rolling(window=3).mean()  # 3일 동안의 %K의 평균을 구해 느린 선 %D에 저장
# %K와 %D로 데이터프레임을 생성한 뒤 결측치 제거
df = df.assign(fast_k=fast_k, slow_d=slow_d).dropna()


plt.figure(figsize=(9, 7))
p1 = plt.subplot(2, 1, 1)
plt.title('Triple Screen Trading - Second Screen (Hanwha)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', colordown='blue')
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'], color='c', label='EMA130')
plt.legend(loc='best')

p1 = plt.subplot(2, 1, 2)
plt.grid(True)
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['fast_k'], color='c', label='%K')
plt.plot(df.number, df['slow_d'], color='k', label='%D')
plt.yticks([0, 20, 80, 100])  # Y축 눈금을 0,20,80,100으로 설정하여 스토캐스틱의 기준선을 나타냄
plt.legend(loc='best')
plt.show()

# 차트 해석 - 130일 지수 이동 평균이 상승하고 있을 때 스토캐스틱이 30 아래로 내려가면 매수 기회로 보고,
# 130일 지수 이동 평균이 하락하고 있을 때 스토캐스틱이 70 위로 올라가면 매도 기회로 본다
