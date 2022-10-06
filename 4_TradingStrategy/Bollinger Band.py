# 볼린저 밴드
# 주가의 20일 이동 평균선을 기준으로, 상대적인 고점을 나타내는 상단 밴드와 상대적 저점을 나타내는 하단 밴드로 구성

import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('기아', '2019-01-02')  # DB 저장 시간 문제로 코드가 앞쪽인 기아 선택

df['MA20'] = df['close'].rolling(window=20).mean()  # 20개 종가를 이용해 평균을 구함
df['stddev'] = df['close'].rolling(
    window=20).std()  # 표준 편차를 구한 뒤 stddev칼럼으로 df에 추가
# 중간 볼린저 밴드 + (2*표준편차)를 상단 볼린저 밴드로 계산
df['upper'] = df['MA20']+(df['stddev']*2)
# 중간 볼린저 밴드 - (2*표준편차)를 하단 볼린저 밴드로 계산
df['lower'] = df['MA20']-(df['stddev']*2)
df = df[19:]  # 위의 4개지는 19번째 행까지 NaN이므로 값이 있는 20번째 행부터 사용

plt.figure(figsize=(9, 5))
plt.plot(df.index, df['close'], color='#0000ff',
         label='Close')  # 종가를 y좌표로 설정해 파란색 실선으로 표시
# 상단 볼린저 밴드 값을 y좌표로 설정해 검은 실선으로 표시
plt.plot(df.index, df['upper'], 'r--', label='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
# 상단 볼린저 밴드와 하단 볼린저 밴드 사이를 회색으로 색칠
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
plt.legend(loc='best')
plt.title('KIA Bollinger Band (20 day, 2 std)')
plt.show()
