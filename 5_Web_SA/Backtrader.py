# RSI를 이용한 단순 백테스트
# RS = N일간의 상승폭 평균/N일간의 하락폭 평균, RSI(상대적 강도 지수) = 100-100/(1+RS)

from datetime import datetime
import backtrader as bt
import yfinance as yf


class MyStrategy(bt.Strategy):  # bt.Strategy 클래스를 상속받아 MyStrategy 클래스를 작성
    def __init__(self):  # RSI 지표를 사용하려면 클래스 생성자에서 RSI 지표로 사용할 변수를 지정
        self.rsi = bt.indicators.RSI(self.data.close)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()


cerebro = bt.Cerebro()  # Cerebro 클래스는 주어진 데이터와 지표를 만족시키는 최소 주기마다 자동으로 호출, 시장에 참여하고 있지 않을 때 RSI 지표가 30 미만이면 매수, 시장에 참여하고 있을 때 RSI가 70을 초과하면 매도
cerebro.addstrategy(MyStrategy)
data = bt.feeds.PandasData(dataname=yf.download(
    '036570.KS', '2019-08-01', '2022-08-01', auto_adjust=True))
cerebro.adddata(data)
cerebro.broker.setcash(10000000)  # 초기 투자 자금을 천만원으로 설정
cerebro.addsizer(bt.sizers.SizerFix, stake=30)

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot()
