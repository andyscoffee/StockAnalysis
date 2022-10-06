# 효율적 투자선

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()
for s in stocks:
    # 내 DB를 사용하기에 내 DB에 저장된 날짜만 불러올 수 있음
    df[s] = mk.get_daily_price(s, '2016-01-04', '2022-07-28')['close']
# print(df)
daily_ret = df.pct_change()  # df에서 제공하는 함수를 사용해 일간 변동률 구하기
# 일간변동률의 평균값에 252(미국 1년 평균 개장일)를 곱해서 연간 수익률 구하기
annual_ret = daily_ret.mean() * 252
daily_cov = daily_ret.cov()  # cov()함수를 이용해 일간 변동률의 공분산으로 일간 리스크 구하기
annual_cov = daily_cov * 252  # 일간 리스크에 252를 곱해 연간 리스크(공분산) 구하기

port_ret = []
port_risk = []
port_weights = []
# 각 포트폴리오 구성마다 수익률, 리스크, 비중을 저장하기 위한 리스트

# 몬테카를로 시뮬레이션 - 매우 많은 난수를 이용해 함수의 값을 확률적으로 계산

for _ in range(20000):
    weights = np.random.random(len(stocks))  # 4개의 랜덤한 숫자로 구성된 배열 생성
    weights /= np.sum(weights)  # 4개의 무작위 수를 무작위 수의 총합으로 나눠 4종목 비중의 합이 1이되도록 조정

    # 무작위 생성된 종목별 비중 배열과 종목별 연간 수익률을 곱해 포트폴리오 전체 수익률 구하기
    returns = np.dot(weights, annual_ret)
    # 종목별 연간 공분산과 종목별 비중 배열을 곱한 뒤 이를 다시 종목별 비중의 전치로 곱함, 구한 결과값의 제곱근을 구하면 해당 포트폴리오 전체의 리스크를 구할 수 있음
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)  # 각 항목을 저장

portfolio = {'Returns': port_ret, 'Risk': port_risk}
for i, s in enumerate(stocks):
    portfolio[s] = [weights[i]
                    for weight in port_weights]  # 포트폴리오 딕셔너리에 각 키 순서로 비중값을 추가
df = pd.DataFrame(portfolio)
# 4가지 종목의 보유 비율에 따라 포트폴리오 20000개가 각기 다른 리스크와 예상 수익률을 갖음
df = df[['Returns', 'Risk']+[s for s in stocks]]

df.plot.scatter(x='Risk', y='Returns', figsize=(10, 7), grid=True)
plt.title('Efficient Frontier')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()
