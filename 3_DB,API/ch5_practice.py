# 5.1.1 야후 파이낸스 데이터의 문제점

import matplotlib.pyplot as plt
from cProfile import label
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

df = pdr.get_data_yahoo('005930.KS', '2017-01-01')  # 삼성전자 데이터를 2017-01-01부터 조회

plt.figure(figsize=(9, 6))
plt.subplot(2, 1, 1)  # 2행 1열 영역에서 첫번째 영역을 선택
plt.title('Samsung Electronics (Yahoo Finance)')
plt.plot(df.index, df['Close'], 'c', label='Close')  # 종가를 청록색 실선으로 표시
plt.plot(df.index, df['Adj Close'], 'b--',
         label='Adj Close')  # 수정 종가를 파란색 점선으로 표시
plt.legend(loc='best')
plt.subplot(2, 1, 2)
# 삼성전자 거래량(volume)을 바 차트로 그림
plt.bar(df.index, df['Volume'], color='g', label='Volume')
plt.legend(loc='best')
plt.show()
