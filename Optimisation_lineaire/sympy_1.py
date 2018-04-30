# coding=utf-8

from sympy import *
init_printing()
x, y = symbols('x y')
sol = solve(x**2-2, x)
print(sol)
print(latex(sol))

from IPython.display import display, Math, Latex
display(Math(r'F(k) = \int_{-\infty}^{\infty} f(x) e^{2\pi i k} dx'))
