# 선형 회귀 문제

import tensorflow as tf
import matplotlib.pyplot as plt

x_data = [1, 2, 3, 4, 5]
y_data = [2, 3, 4, 5, 6]

w = tf.Variable(0.7)  # 가중치를 임의의 값(0.7)로 초기화
b = tf.Variable(0.7)  # 편향을 임의의 값(0.7)로 초기화
# 학습률은 보통 0.01~0.001 사이의 값으로 설정, 너무 크면 비용이 무한대로 늘어나고, 너무 작으면 학습에 걸리는 시간이 길어진다
learn_rate = 0.01

print(f'step|    w|    b| cost')
print(f'----|-----|-----|-----|')

for i in range(1, 1101):  # 1100회 반복
    with tf.GradientTape() as tape:  # 내부의 계산 과정을 tape에 기록하는 것, 기록해두면 tape.gradient 함수를 이용해 미분값을 구할 수 있음
        hypothesis = w * x_data + b  # 가설을 w * x + b 로 설정
        # == tf.losses.mean_squared_error(hypothesis - y_data), 손실 비용을 오차제곱평균으로 구하기
        cost = tf.reduce_mean((hypothesis-y_data)**2)
    dw, db = tape.gradient(cost, [w, b])  # w와 b에 대해 손실을 미분해 dw, db값을 가함

    w.assign_sub(learn_rate*dw)  # a.assign_sub() == a = a-b와 동일한 연산 수행
    b.assign_sub(learn_rate*db)  # w 값에서 학습률 * dw를 뺀 값을 새로운 w 값으로 설정

    if i in [1, 3, 5, 10, 1000, 1100]:
        print(f'{i:4d}| {w.numpy():.2f}| {b.numpy():.2f}| {cost:.2f}')
        plt.figure(figsize=(7, 7))
        plt.title(f'[Step {i:d}]  h(x) = { w.numpy():.2f}x+{b.numpy():.2f}')
        plt.plot(x_data, y_data, 'o')
        plt.plot(x_data, w*x_data+b, 'r', label='hypothesis')
        plt.xlabel('x_data')
        plt.ylabel('y_data')
        plt.xlim(0, 6)
        plt.ylim(1, 7)
        plt.legend(loc='best')
        plt.show()
