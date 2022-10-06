# 활성화 함수 - 출력 신호가 라틴 문자 S 모양인 시그모이드 함수
import numpy
import matplotlib.pyplot as plt


def sigmoid(x):
    # exp(x) -> e의 x승, x값이 0으로부터 음수 방향으로 멀어지면 분모의 값이 커지므로 y값이 0에 가까워짐, 반대의 경우 y값이 1에 가까워짐
    return 1/(1 + numpy.exp(-x))


x = numpy.arange(-10, 10, 0.1)
y = sigmoid(x)

plt.plot(x, y)
plt.title('Sigmoid Function')
plt.show()

# 계단 함수는 0 또는 1을 출력하지만, 시그모이드 함수를 사용하면 0~1사이의 연속 실수를 출력한다. -> 복잡한 신경망에 대한 계산이 가능
