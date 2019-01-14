# coding=utf-8
from numpy import linspace, pi


def cal(x, y):
    f = x**3 * y / (x**4 + y**2)
    return f


x = linspace(0, 2 * pi, 30)

print(cal(0.1, 0.0))
print(cal(0.1, 0.1))
print(cal(0.0, 0.1))

print(cal(0.01, 0.00))
print(cal(0.01, 0.01))
print(cal(0.00, 0.01))

print(cal(0.001, 0.000))
print(cal(0.001, 0.001))
print(cal(0.000, 0.001))

print(cal(-0.1, -0.0))
print(cal(-0.1, -0.1))
print(cal(-0.0, -0.1))

print(cal(-0.01, -0.00))
print(cal(-0.01, -0.01))
print(cal(-0.00, -0.01))

print(cal(-0.001, -0.000))
print(cal(-0.001, -0.001))
print(cal(-0.000, -0.001))
