# RNN을 이용한 주가 예측

import tensorflow as tf
from keras import Sequential
from keras.layers import Dense, LSTM, Dropout
import numpy
import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
raw_df = mk.get_daily_price('한화', '2020-08-15', '2022-08-15')


def MinMaxScaler(data):
    # 최솟값과 최댓값을 이용하여 0~1 사이로 변환
    numerator = data - numpy.min(data, 0)
    denominator = numpy.max(data, 0) - numpy.min(data, 0)
    # 숫자 단위가 클수록 계산 소요 시간이 늘어나므로 데이터를 0~1 사이 작은 단위로 변환 후 계산해 소요 시간을 단축,
    # 0으로 나누는 에러가 발생하지 않도록 매우 작은 값을 더해서 나눈다.
    return numerator/(denominator+1e-7)


"""데이터 전처리"""
dfx = raw_df[['open', 'high', 'low', 'volume', 'close']]
dfx = MinMaxScaler(dfx)
dfy = dfx[['close']]

x = dfx.values.tolist()
y = dfy.values.tolist()

"""
출력 확인용
print('raw_df \n', raw_df, '\n')
print('dfx.info() \n', dfx.info(), '\n')
print('dfy.info() \n', dfy.info(), '\n')
print('x[-6:] \n', x[-6:], '\n')
print('y[-6:] \n', y[-6:])
"""

"""데이터셋 준비"""
data_x = []
data_y = []
window_size = 10  # 10일 동안의 OHLVC 데이터를 이용
for i in range(len(y)-window_size):
    _x = x[i:i+window_size]  # 다음날 종가(x[i+window_size])는 포함되지 않음
    _y = y[i+window_size]  # 다음날 종가
    data_x.append(_x)
    data_y.append(_y)
# print(_x, "->", _y) 데이터셋 출력

"""훈련용 데이터셋과 테스트용 데이터셋 분리"""

# 훈련용 데이터셋
train_size = int(len(data_y) * 0.7)  # 492개의 데이터셋 중 70%를 훈련용으로 사용
train_x = numpy.array(data_x[0:train_size])
train_y = numpy.array(data_y[0:train_size])

# 테스트용 데이터셋
test_size = len(data_y) - train_size  # 30%는 테스트용으로 사용
test_x = numpy.array(data_x[train_size:len(data_x)])
test_y = numpy.array(data_y[train_size:len(data_y)])

"""모델 생성하기, 케라스 API 활용"""

model = Sequential()  # 시퀀셜 모델 객체 생성
# (10,5) 입력 형태를 가지는 LSTM층, 전체 유닛 개수는 10개, 활성화 함수는 relu를 사용
model.add(LSTM(units=10, activation='relu',
          return_sequences=True, input_shape=(window_size, 5)))
# 드롭아웃을 10%로 지정, 드롭아웃층은 입력값의 일부분을 선택하여 그 값을 0으로 치환하여
# 다음 층으로 출력함으로써 훈련 데이터를 늘리지 않고도 과적합을 방지
model.add(Dropout(0.1))
model.add(LSTM(units=10, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(units=1))  # 유닛이 하나인 출력층 추가
model.summary()

# 최적화 도구는 adam, 손실 함수는 MSE를 사용
model.compile(optimizer='adam', loss='mean_squared_error')
# 훈련용 데이터셋으로 모델을 학습, epochs는 전체 데이터셋에 대한 학습 횟수, batch_size는 한번에 제공되는 훈련 데이터 개수
model.fit(train_x, train_y, epochs=60, batch_size=30)
pred_y = model.predict(test_x)  # 예측치 데이터셋 생성

"""예측치와 실제 종가 비교"""

plt.figure()
plt.plot(test_y, color='red', label='Real Hanwha stock price')
plt.plot(pred_y, color='blue', label='Predicted Hanwha stock price')
plt.title('Hanwha stock price prediction')
plt.xlabel('time')
plt.ylabel('stock price')
plt.legend()
plt.show()

"""내일의 종가 출력 예측"""
print("Hanwha tommorow's price :", raw_df.close[-1]*pred_y[-1]/dfy.close[-1])
