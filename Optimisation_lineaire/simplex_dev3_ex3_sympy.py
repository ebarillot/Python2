# coding=utf-8

from __future__ import print_function
import sympy as sp
from Optimisation_lineaire.simplex_fun import pvar, simplex_step, solution_numerique, simplex_callback_print

sp.init_printing(use_unicode=True)

nvars = 4
vars_list_name_x = ['x_{}'.format(i) for i in range(1, nvars + 1)]
vars_list_name_y = ['y_{}'.format(i) for i in range(1, nvars + 1)]
vars_list = sp.symbols(vars_list_name_x)


# exemple dans R^3
A2 = sp.Matrix(2, 2, [0, sp.Rational(1, 2), sp.Rational(1, 2), 0])
pvar("A2")
b2 = sp.Matrix(2, 1, [0, 0])
pvar("b")
c2 = sp.Matrix(1, 1, [-1])
pvar("c")

V2 = sp.Matrix(2, 1, vars_list[:2])
pvar("V2")

V2.transpose() * A2 * V2 + b2.transpose() * V2 + c2


# exemple dans R^3
A3 = sp.Matrix(3, 3, [1 , 1 , 1 ,
                      1 , 1 , 1 ,
                      1 , 1 , 1  ])
pvar("A3")
b3 = sp.Matrix(3, 1, [0, 0, 0])
pvar("b3")
c3 = sp.Matrix(1, 1, [-1])
pvar("c3")

V3 = sp.Matrix(3, 1, vars_list[:3])
pvar("V3")

V3.transpose() * A3 * V3 + b3.transpose() * V3 + c3


#
# question 2, traitée dans R^4 (dimension adoptée dans Numerical Recipes)
#
dim = 4
vars_list_name_x = ['x_{}'.format(i) for i in range(1, dim + 1)]
vars_list_x = sp.symbols(vars_list_name_x)

vars_list_name_a = ['a_{}{}'.format(i, j) for i in range(1, dim + 1) for j in range(1, dim + 1)]
vars_list_a = sp.symbols(vars_list_name_a)

vars_list_name_b = ['b_{}'.format(i) for i in range(1, dim + 1)]
vars_list_b = sp.symbols(vars_list_name_b)

vars_list_name_c = ['c']
vars_list_b = sp.symbols(vars_list_name_c)

A4 = sp.Matrix(dim, dim, vars_list_name_a)
pvar("A4")
b4 = sp.Matrix(dim, 1, vars_list_name_b)
pvar("b4")
c4 = sp.Matrix(1, 1, vars_list_name_c)
pvar("c4")

V4 = sp.Matrix(dim, 1, vars_list[:dim])
pvar("V4")

Phi = V4.transpose() * A4 * V4 + b4.transpose() * V4 + c4
pvar("Phi")

# t x + (1-t) y
t = sp.symbols('t')
# x_1 = sp.symbols('x_1')
# eval("x_1, x_2, x_3, x_4 = sp.symbols(vars_list_name_x)")
x_1, x_2, x_3, x_4 = sp.symbols(vars_list_name_x)
y_1, y_2, y_3, y_4 = sp.symbols(vars_list_name_y)

# Phi.subs([(x_1, t*x_1+(1-t)*y_1)])
Phi.subs([(x_1, (t*x_1+(1-t)*y_1)),
          (x_2, (t*x_2+(1-t)*y_2)),
          (x_3, (t*x_3+(1-t)*y_3)),
          (x_4, (t*x_4+(1-t)*y_4))])

