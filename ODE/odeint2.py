# coding=utf-8

import numpy as np
from scipy.integrate import odeint


# def pend(y, t):
#     dydt = -((t + 1) / 2) * y
#     return dydt


def pend(y, t):
    return (1 - y) / (1 + t*t)


y0 = 0.0
t = np.linspace(0., 1, 101)
sol = odeint(pend, y0, t)

# print (sol)

import matplotlib.pyplot as plt

plt.plot(t, sol, 'b', label='y')
plt.legend(loc='best')
plt.xlabel('t')
plt.grid()
plt.show()
