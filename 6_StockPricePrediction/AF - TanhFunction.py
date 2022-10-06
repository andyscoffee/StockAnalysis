# 활성화 함수 - 출력 신호가 쌍곡탄젠트인 함수
import numpy as np
import matplotlib.pyplot as plt


def tanh(x):
    return (np.exp(x) - np.exp(-x))/(np.exp(x) + np.exp(-x))  # -1~1 까지의 값을 출력


x = np.arange(-10, 10, 0.1)
y = tanh(x)  # == y = np.tanh(x)

plt.plot(x, y)
plt.title('Tanh Function')
plt.show()
