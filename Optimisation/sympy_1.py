# coding=utf-8

from sympy import *
init_printing()
x, y = symbols('x y')
sol = solve(x**2-2, x)
print(sol)
print(latex(sol))

