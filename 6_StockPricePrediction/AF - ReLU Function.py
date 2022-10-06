# Rectified Linear Unit 함수, 음수를 0으로 만든다. 입력이 0 이하일경우 0 출력, 0을 넘어갈 경우 입력값을 그대로 출력

import numpy
import matplotlib.pyplot as plt


def relu(x):
    return numpy.maximum(0, x)  # 인수로 주어진 두 수 중 가장 큰 수 반환


x = numpy.arange(-10, 10, 0.1)
y = relu(x)

plt.plot(x, y)
plt.title('ReLU Function')
plt.show()

# 최근 시그모이드 함수를 대체하여 많이 사용
