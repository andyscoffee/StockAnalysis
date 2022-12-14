# 볼린저 밴드 반전 매매법

import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('기아', '2018-11-02')

df['MA20'] = df['close'].rolling(window=20).mean()
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20']+(df['stddev']*2)
df['lower'] = df['MA20']-(df['stddev']*2)
df['PB'] = (df['close']-df['lower'])/(df['upper']-df['lower'])

df['II'] = (2*df['close']-df['high']-df['low']) / \
    (df['high']-df['low'])*df['volume']
df['IIP21'] = df['II'].rolling(window=21).sum(
)/df['volume'].rolling(window=21).sum()*100
df = df.dropna()

plt.figure(figsize=(9, 9))
plt.subplot(3, 1, 1)
plt.plot(df.index, df['close'], 'b', label='Close')
plt.plot(df.index, df['upper'], 'r--', label='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
plt.title('KIA Bollinger Band (20 day, 2 std) - Reversals')
for i in range(0, len(df.close)):
    # %b가 0.05보다 작고, 21일 기준 II%가 0보다 크면
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
        # 첫 번째 그래프에 매수 시점을 나타내는 종가 위치에 빨간색 삼각형 표시
        plt.plot(df.index.values[i], df.close.values[i], 'r^')
    # %b가 0.95보다 크고, 21일 기준 II%가 0보다 작으면
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
        # 첫 번째 그래프에 매도 시점을 나타내는 종가 위치에 파란색 삼각형 표시
        plt.plot(df.index.values[i], df.close.values[i], 'bv')
plt.legend(loc='best')

plt.subplot(3, 1, 2)
plt.plot(df.index, df['PB'] * 100, 'b', label='%b')
plt.grid(True)
plt.legend(loc='best')

plt.subplot(3, 1, 3)
plt.bar(df.index, df['IIP21'], color='g', label='II% 21day')
for i in range(0, len(df.close)):
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
        # 일중 강도율 그래프에 매수 시점을 표시
        plt.plot(df.index.values[i], 0, 'r^')
    # %b가 0.95보다 크고, 21일 기준 II%가 0보다 작으면
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
        # 매도 시점을 표시
        plt.plot(df.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show()
