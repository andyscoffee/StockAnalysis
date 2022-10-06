# 볼린저 밴드 밴드폭((상단볼린저밴드-하단볼린저밴드)/중간볼린저밴드) 추가

import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('기아', '2019-01-02')

df['MA20'] = df['close'].rolling(window=20).mean()
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20']+(df['stddev']*2)
df['lower'] = df['MA20']-(df['stddev']*2)

df['bandwidth'] = (df['upper']-df['lower'])/df['MA20'] * 100  # 밴드폭 계산해서 칼럼 생성
df = df[19:]

plt.figure(figsize=(9, 8))
plt.subplot(2, 1, 1)  # 기존의 볼린저 밴드 차트를 2행 1열의 그리드에서 1열에 배치
plt.plot(df.index, df['close'], color='#0000ff', label='Close')
plt.plot(df.index, df['upper'], 'r--', label='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
plt.title('KIA Bollinger Band (20 day, 2 std)')
plt.legend(loc='best')

plt.subplot(2, 1, 2)  # 밴드폭 차트를 2열에 배치
plt.plot(df.index, df['bandwidth'], color='m', label='BandWidth')  # 밴드폭 차트를 표시
plt.grid(True)
plt.legend(loc='best')
plt.show()
