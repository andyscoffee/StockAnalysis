# 볼린저 밴드 일중 강도율
# 일중 강도 = (2 * 종가-고가-저가)/(고가-저가) * 거래량
# 일중 강도율 = 일중 강조의 21일 합/거래량의 21일 합 * 100

import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('기아', '2019-01-02')

df['MA20'] = df['close'].rolling(window=20).mean()
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20']+(df['stddev']*2)
df['lower'] = df['MA20']-(df['stddev']*2)
df['PB'] = (df['close']-df['lower'])/(df['upper']-df['lower'])

# 공식에 따른 일중 강도(Intraday Intencity) 계산
df['II'] = (2*df['close']-df['high']-df['low']) / \
    (df['high']-df['low'])*df['volume']
# 일중 강도율 계산
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
plt.legend(loc='best')

plt.subplot(3, 1, 2)
plt.plot(df.index, df['PB'] * 100, 'b', label='%b')
plt.grid(True)
plt.legend(loc='best')

plt.subplot(3, 1, 3)
plt.bar(df.index, df['IIP21'], color='g', label='II% 21day')
plt.grid(True)
plt.legend(loc='best')
plt.show()
"""
주가가 하단 볼린저 밴드에 닿을 때 일중 강도율이 +이면 매수하고, 반대로 주가가 상단 볼린저 밴드에 닿을 때 일중 강도율이 -이면 매도
"""
