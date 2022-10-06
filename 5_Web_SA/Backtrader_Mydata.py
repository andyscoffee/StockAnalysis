# RSI를 이용한 단순 백테스트 판다스 데이터(내가 저장한) 사용

from datetime import datetime
import backtrader as bt
import yfinance as yf
import Analyzer
import pandas as pd


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()


cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
mk = Analyzer.MarketDB()  # 저장된 데이터를 사용하기 위해 생성
df = mk.get_daily_price('000270', '2019-01-01', '2021-08-01')
df.date = pd.to_datetime(df.date)  # 데이터 가공
data = bt.feeds.PandasData(dataname=df, datetime='date')  # 데이터 입력
cerebro.adddata(data)
cerebro.broker.setcash(10000000)
cerebro.addsizer(bt.sizers.SizerFix, stake=30)

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot()
