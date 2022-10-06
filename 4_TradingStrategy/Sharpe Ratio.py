# 샤프 지수
# 측정된 위험 단위당 수익률을 계산, 샤프지수 = (포트폴리오 예상 수익률-무위험률)/수익률의 표준편차

# 효율적 투자선

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2016-01-04', '2022-07-28')['close']

daily_ret = df.pct_change()
annual_ret = daily_ret.mean() * 252
daily_cov = daily_ret.cov()
annual_cov = daily_cov * 252

port_ret = []
port_risk = []
port_weights = []
sharpe_ratio = []  # 샤프 지수 저장용 배열

for _ in range(20000):
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)

    returns = np.dot(weights, annual_ret)
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)
    sharpe_ratio.append(returns/risk)  # 무위험률이 0이라고 가정, 예상수익률/표준편차의 샤프지수 값을 저장

portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio}
for i, s in enumerate(stocks):
    portfolio[s] = [weights[i] for weight in port_weights]

df = pd.DataFrame(portfolio)
df = df[['Returns', 'Risk', 'Sharpe'] + [s for s in stocks]]

max_sharpe = df.loc[df['Sharpe'] == df['Sharpe'].max()]  # 샤프 지수값이 가장 큰 행
min_risk = df.loc[df['Risk'] == df['Risk'].min()]  # 리스크값이 제일 작은 행

# 컬러맵을 viridis로 표시하고 테두리는 검정(k)으로 표시
df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis',
                edgecolors='k', figsize=(11, 7), grid=True)

plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r',
            marker='*', s=300)  # 샤프 지수가 가장 큰 포트폴리오를 300크기의 붉은 별로 표시
plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r',
            marker='X', s=200)  # 리스크가 가장 작은 포트폴리올르 200크기의 붉은 X로 표시
plt.title('Portfolio Optimization')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()
print('max_sharpe')
print(max_sharpe)
print('min_risk')
print(min_risk)
