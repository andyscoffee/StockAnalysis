# 분류 문제를 다룰 때 사용, 입력받은 값들을 0~1사이 값으로 정규화
import numpy
import matplotlib.pyplot as plt


def softmax(x):
    return numpy.exp(x)/numpy.sum(numpy.exp(x))  # 전체 출력값의 합은 항상 1
