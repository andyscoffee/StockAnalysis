# 퍼셉트론 알고리즘 - 신경망 알고리즘의 기초
# 여러 입력 신호(x1, x2)에 대해 각각 고유한 가중치 보유
def AND(x1, x2):
    w1 = 0.5
    w2 = 0.5
    theta = 0.7

    if w1*x1 + w2*x2 > theta:  # 신호의 총합이 임계값(세타) 이하면 0, 넘어서면 1 출력 -> 활성화
        return 1
    else:
        return 0

# 퍼셉트론은 구조를 변경하지 않으면서 매개변수만 변경하여 AND, OR, NAND 세 가지의 논리 회로 구성 가능


def NAND(x1, x2):
    w1 = -0.5
    w2 = -0.5
    theta = -0.7

    if w1*x1 + w2*x2 > theta:
        return 1
    else:
        return 0


def OR(x1, x2):
    w1 = 0.5
    w2 = 0.5
    theta = 0.2

    if w1*x1 + w2*x2 > theta:
        return 1
    else:
        return 0
# XOR 논리 회로는 퍼셉트론 하나로는 만들 수 없고 퍼셉트론을 여러 층으로 쌓은 다층 퍼셉트론이 필요


def XOR(x1, x2):
    return AND(NAND(x1, x2), OR(x1, x2))
