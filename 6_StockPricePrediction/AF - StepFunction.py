# 활성화 함수(Activation Function) - 입력 신호의 총합이 임계값을 넘어설 때 특정값을 출력하는 함수
# 출력 신호가 계단 모양을 닮아 계단 함수
import numpy
import matplotlib.pyplot as plt


def stepfunc(x):
    return numpy.where(x <= 0, 0, 1)  # x의 값이 부등식을 만족하면 0, 만족하지 않으면 1 반환


x = numpy.arange(-10, 10, 0.1)  # -10부터 10까지 0.1 간격의 배열, 마지막 값은 9.9
y = stepfunc(x)

plt.plot(x, y)
plt.title('Step Function')
plt.show()
