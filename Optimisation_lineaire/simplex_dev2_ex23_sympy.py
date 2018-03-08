# coding=utf-8

from __future__ import print_function
import sympy as sp


# solution numérique
from scipy.optimize import linprog
c = [-x for x in  [ 1., -1., 1.]]        # attention, linprog cherche à minimiser et non as à maximiser
A = [[2.,-1.,2.],[2.,-3.,1.],[-1.,1.,-2.]]
b = [4.,-5.,-1.]
x1_bnds = (0, None)
x2_bnds = (0, None)
x3_bnds = (0, None)
res = linprog(c, A, b, bounds=(x1_bnds, x2_bnds, x3_bnds))
print(res)


# solution sympy
sp.init_printing(use_unicode=True)

x1, x2, x3, x4, x5, x6 = sp.symbols('x1 x2 x3 x4 x5 x6')

M = sp.Matrix(A)
print('M: ', end='')
print(M)

V = sp.Matrix(3,1,[x1,x2,x3])
print('V: ', end='')
print(V)

b = sp.Matrix(b).transpose()
print('b: ', end='')
print(b)

r1 = sp.Matrix([  2 , -1 ,  2 ,  1 ,  0 ,  0 ,  4]).transpose()
r2 = sp.Matrix([  2 , -3 ,  1 ,  0 ,  1 ,  0 , -5]).transpose()
r3 = sp.Matrix([ -1 ,  1 , -2 ,  0 ,  0 ,  1 , -1]).transpose()
r4 = sp.Matrix([  1 , -1 ,  1 ,  0 ,  0 ,  0 ,  0]).transpose()
s0p1 = sp.Matrix([0, sp.Rational(11,5), sp.Rational(8,5), 0, 0, 0]).transpose()
sp.latex(s0p1.dot(r1[:-1]))
sp.latex(s0p1.dot(r2[:-1]))
sp.latex(s0p1.dot(r3[:-1]))


r1p1 = r1/2
r2p1 = r2-r1
r3p1 = r3+r1/2
r4p1 = r4-r1/2
sp.latex(r1p1)
sp.latex(r2p1)
sp.latex(r3p1)
sp.latex(r4p1)


r1p2 = r1p1
r2p2 = r2p1 + r1p1
r3p2 = r3p1 + r1p1
r4p2 = r4p1
sp.latex(r1p2)
sp.latex(r2p2)
sp.latex(r3p2)
sp.latex(r4p2)

s0p2 = sp.Matrix([2, 0, 1, 0, 7, 0, 0]).transpose()
sp.latex(s0p2)

min(sp.Rational(7/sp.Rational(5,2)), sp.Rational(2/sp.Rational(5,4)))

r2p3 = r2p2*sp.Rational(4,5)
r1p3 = r1p2 - r2p3*sp.Rational(5,2)
r3p3 = r3p2 - r2p3*sp.Rational(-3,4)
r4p3 = r4p2 - 5*r2p3
sp.latex(r1p3)
sp.latex(r2p3)
sp.latex(r3p3)
sp.latex(r4p3)


x1s = 0
x2s = sp.Rational(11,5)
x3s = sp.Rational(8,5)

sp.Matrix([x1s, x2s, x3s]).transpose() * sp.Matrix([2, -1, 2])
sp.Matrix([x1s, x2s, x3s]).transpose() * sp.Matrix([2, -3, 1])
sp.Matrix([x1s, x2s, x3s]).transpose() * sp.Matrix([-1, 1, -2])