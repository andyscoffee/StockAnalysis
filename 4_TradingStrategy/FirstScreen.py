# 삼중창 매매 시스템 - 추세 추종과 역추세 매매범을 함께 사용, 세 단계의 창을 거쳐 더 정확한 매매 시점을 찾도록 구성
# 첫 번째 창 - 시장 조류
# 첫 번째 창을 통해 매수, 매도, 관망 세 가지 선택지 중 하나를 제거할 수 있음

import pandas as pd
import matplotlib.pyplot as plt
import datetime
# mpl_financee 구버전 경고문 삭제용 변경
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('한화', '2017-01-01')

ema60 = df.close.ewm(span=60).mean()  # 종가의 12주 지수 이동평균
ema130 = df.close.ewm(span=130).mean()  # 종가의 26주 지수 이동평균
macd = ema60-ema130  # MACD선
signal = macd.ewm(span=45).mean()  # 신호선(MACD의 9주 지수 이동평균)
macdhist = macd - signal  # MACD 히스토그램

df = df.assign(ema130=ema130, ema60=ema60, macd=macd,
               signal=signal, macdhist=macdhist).dropna()
# 캔들 차트에 사용할 수 있게 날짜(date)형 인덱스를 숫자형으로 변환
df['number'] = df.index.map(mdates.date2num)
ohlc = df[['number', 'open', 'high', 'low', 'close']]

plt.figure(figsize=(9, 7))
p1 = plt.subplot(2, 1, 1)
plt.title('Triple Screen Trading - First Screen(Hanwha)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', colordown='blue')
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'], color='c', label='EMA130')
plt.legend(loc='best')

p2 = plt.subplot(2, 1, 2)
plt.grid(True)
p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.bar(df.number, df['macdhist'], color='m', label='MACD-Hist')
plt.plot(df.number, df['macd'], color='b', label='MACD')
plt.plot(df.number, df['signal'], 'g--', label='MACD-Signal')
plt.legend(loc='best')
plt.show()
