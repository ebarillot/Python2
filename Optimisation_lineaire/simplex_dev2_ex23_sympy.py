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

# redéfinis avec des entiers
A = [[2,-1,2],[2,-3,1],[-1,1,-2]]
b = [4,-5,-1]
c = [ 1, -1, 1] + [0]*len(b) + [0]        # attention, linprog cherche à minimiser et non as à maximiser

M = sp.Matrix(A)
print('M: ', end='')
print(M)
M.inv()


V = sp.Matrix(3,1,[x1,x2,x3])
print('V: ', end='')
print(V)

b = sp.Matrix(b).transpose()
print('b: ', end='')
print(b)

c = sp.Matrix(c).transpose()
print('c: ', end='')
print(c)

# r1 = sp.Matrix([  2 , -1 ,  2 ,  1 ,  0 ,  0 ,  4]).transpose()
# r2 = sp.Matrix([  2 , -3 ,  1 ,  0 ,  1 ,  0 , -5]).transpose()
# r3 = sp.Matrix([ -1 ,  1 , -2 ,  0 ,  0 ,  1 , -1]).transpose()
# r4 = sp.Matrix([  1 , -1 ,  1 ,  0 ,  0 ,  0 ,  0]).transpose()

s0p1 = sp.Matrix([0, sp.Rational(11,5), sp.Rational(8,5), 0, 0, 0]).transpose()
s0p1[:,:3] * M.inv()
s0p1.shape
type(s0p1)
cp1 = sp.Matrix([0]*len(c)).transpose()
cp1[:,-1] = c[:,:-1] * s0p1.transpose()
cp1[:,3:6] = -c[:,:3] * M.inv()

M.inv()*b
M2 = sp.eye(3).row_join(M.inv()).row_join(M.inv()*b).col_join(cp1)
r1 = M2[0,:]
r2 = M2[1,:]
r3 = M2[2,:]
r4 = M2[3,:]
sp.latex(s0p1.dot(r1[:-1]))
sp.latex(s0p1.dot(r2[:-1]))
sp.latex(s0p1.dot(r3[:-1]))
sp.latex(s0p1.dot(r4[:-1]))


r1p1 = r1/r1[6-1]
r2p1 = r2-r1*r2[6-1]
r3p1 = r3-r1*r3[6-1]
r4p1 = r4-r1*r4[6-1]
sp.latex(r1p1)
sp.latex(r2p1)
sp.latex(r3p1)
sp.latex(r4p1)
