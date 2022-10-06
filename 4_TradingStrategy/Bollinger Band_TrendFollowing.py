# 볼린저 밴드 추세 추종 매매기법
# MFI = 100 - (100/(1+긍정적현금흐름/부정적현금흐름))
import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('기아', '2019-01-02')

df['MA20'] = df['close'].rolling(window=20).mean()
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20']+(df['stddev']*2)
df['lower'] = df['MA20']-(df['stddev']*2)
df['PB'] = (df['close']-df['lower'])/(df['upper']-df['lower'])

# 고가, 저가, 종가의 합을 3으로 나눠서 중심 가격(Typical Price)를 구함
df['TP'] = (df['high']+df['low']+df['close'])/3
df['PMF'] = 0  # 긍정적 현금 흐름(Positive Money Flow): 중심 가격이 전일보다 상승한 날들의 현금 흐름
df['NMF'] = 0  # 부정적 현금 흐름(Negative Money Flow)을 저장할 칼럼
for i in range(len(df.close)-1):  # 0부터 종가 개수-2 까지
    if df.TP.values[i] < df.TP.values[i+1]:  # i번째 중심 가격보다 i+1번째 중심 가격이 높으면
        # i+1번째 중심 가격과 i+1번째 거래량의 곱을 i+1번째 긍정적 현금 흐름(Positive Money Flow)에 저장
        df.PMF.values[i+1] = df.TP.values[i+1]*df.volume.values[i+1]
        df.NMF.values[i+1] = 0  # i+1번째 부정적 현금 흐름 값은 0으로 저장
    else:
        df.NMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.PMF.values[i+1] = 0
# 10일 동안의 긍정적 현금 흐름의 합을 10일 동안의 부정적 현금흐름의 합으로 나눈 결과를 현금 흐름 비율(MFR) 칼럼에 저장
df['MFR'] = df.PMF.rolling(window=10).sum()/df.NMF.rolling(window=10).sum()
df['MFI10'] = 100-100/(1+df['MFR'])  # 현금 흐름 지수를 저장한 결과를 MFI10 칼럼에 저장
df = df[19:]

plt.figure(figsize=(9, 8))
plt.subplot(2, 1, 1)
plt.plot(df.index, df['close'], color='#0000ff', label='Close')
plt.plot(df.index, df['upper'], 'r--', label='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
plt.title('KIA Bollinger Band (20 day, 2 std) - Trend Following')
for i in range(len(df.close)):
    # %b가 0.8보다 크고 MFI가 80보다 크면(강력한 매수 신호)
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        # 매수 시점을 나타내기 위해 첫 번째 그래프에 종가 위치에 빨간색 삼각형 표시
        plt.plot(df.index.values[i], df.close.values[i], 'r^')
    # %b가 0.2보다 작고 MFI가 20보다 작으면(강력한 매도 신호)
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        # 매도 시점을 나타내기 위해 첫 번째 그래프의 종가 위치에 파란색 삼각형 표시
        plt.plot(df.index.values[i], df.close.values[i], 'bv')
plt.legend(loc='best')

plt.subplot(2, 1, 2)
plt.plot(df.index, df['PB'] * 100, 'b', label='%B x 100')  # %b * 100 차트 표시
# 10일기준 MFI를 녹색의 점선으로 표시
plt.plot(df.index, df['MFI10'], 'g--', label='MFI(10 day)')
plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])  # y축 눈금을 -20부터 120까지 20단위로 표시
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        plt.plot(df.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show()
