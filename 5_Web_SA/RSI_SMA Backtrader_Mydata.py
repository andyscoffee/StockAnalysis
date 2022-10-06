# RSI_SMA를 이용한 백테스트 판다스 데이터(내가 저장한) 사용

from datetime import datetime
import backtrader as bt
import yfinance as yf
import Analyzer
import pandas as pd


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.butcomm = None
        self.rsi = bt.indicators.RSI_SMA(
            self.data.close, period=21)  # 21일 단순 이동평균에 대한 RSI_SMA 사용

# 주문 상태에 변화가 있을때마다 자동 실행, 주문 객체를 인수로 넘겨받아 주문 상태를 완료, 취소, 마진, 거절로 나타냄
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:  # 주문 상태가 완료인 경우
            if order.isbuy():  # 매수일 경우
                # 상세 주문 정보를 출력
                self.log(
                    f'BUY : 주가 {order.executed.price:,.0f}, 수량 {order.executed.size:,.0f},\
                    수수료 {order.executed.comm:,.0f}, 자산 {cerebro.broker.getvalue():,.0f}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # 매도
                self.log(f'SELL : 주가 {order.executed.price:,.0f}, 수량 {order.executed.size:,.0f},\
                    수수료 {order.executed.comm:,.0f}, 자산 {cerebro.broker.getvalue():,.0f}')
        elif order.status in [order.Canceled]:
            self.log('ORDER CANCELD')
        elif order.status in [order.Margin]:
            self.log('ORDER MARGIN')
        elif order.status in [order.Rejected]:
            self.log('ORDER REJECTED')
        self.order = None

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()
# 텍스트 메시지를 인수로 받아 셀 화면에 주문 일자와 함께 출력

    def log(self, txt, dt=None):
        dt = self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {txt}')


cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
mk = Analyzer.MarketDB()  # 저장된 데이터를 사용하기 위해 생성
df = mk.get_daily_price('000270', '2019-01-01', '2021-08-01')
df.date = pd.to_datetime(df.date)  # 데이터 가공
data = bt.feeds.PandasData(dataname=df, datetime='date')  # 데이터 입력
cerebro.adddata(data)
cerebro.broker.setcash(10000000)
# 수수료의 경우 0.25% 증권거래세, 0.015% 증권거래수수료 ->한 번 거래할때마다 0.28% 비용 소모, 백트레이더의 경우 매수, 매도 시점마다 수수료가 두 번 차감되기에 0.28%/2 = 0.0014
cerebro.broker.setcommission(commission=0.0014)
# size는 매매 주문을 적용할 주식 수, 특별히 지정하지 않으면 1, PercentSizer이용해 자산에 대한 퍼센트로 지정, 100으로 지정하면 수수료를 낼 수 없기에 90 설정
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot(style='candlestick')  # 캔들스틱 차트로 표시
