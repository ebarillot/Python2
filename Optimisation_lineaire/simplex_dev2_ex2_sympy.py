# coding=utf-8

from __future__ import print_function
import sympy as sp
# from sympy import *

sp.init_printing(use_unicode=True)

x0, x1, x2, x3, x4, x5, x6 = sp.symbols('x0 x1 x2 x3 x4 x5 x6')

M = sp.Matrix([[-1,2,-1,2],[-1,2,-3,1],[-1,-1,1,-2]])
print('M: ', end='')
print(M)

V = sp.Matrix(4,1,[x0,x1,x2,x3])
print('V: ', end='')
print(V)

b = sp.Matrix([[4,-5,-1]]).transpose()
print('b: ', end='')
print(b)



# solution numérique
from scipy.optimize import linprog
c = [1, 0, 0, 0]        # attention, linprog cherche à minimiser et non as à maximiser
A = [[-1,2,-1,2],[-1,2,-3,1],[-1,-1,1,-2]]
b = [4,-5,-1]
x0_bnds = (0, None)
x1_bnds = (0, None)
x2_bnds = (0, None)
x3_bnds = (0, None)
res = linprog(c, A, b, bounds=(x0_bnds, x1_bnds, x2_bnds, x3_bnds))
print(res)
