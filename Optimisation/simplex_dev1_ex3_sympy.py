# coding=utf-8

from __future__ import print_function
from sympy import *

init_printing(use_unicode=True)

x, y, z, lamb = symbols('x y z lamda')

# m = Matrix([[lamb*x, y, z], [x, lamb*y, z], [x, y, lamb*z]])
# print(latex(m))
#
# row = Matrix([[x, y, z]])
# M = row.row_insert(1,row).row_insert(2,row)
# M = M+eye(3)*lamb
# print(M)

M = diag([lamb],[lamb],[lamb])+ones(3)-eye(3)
print('M: ', end='')
print(M)
V = Matrix(3,1,[x,y,z])
print('V: ', end='')
print(V)
b = Matrix([[1],[lamb],[1]])
print('b: ', end='')
print(b)
detM = det(M)
detMf = factor(detM)
print('detM: ', end='')
print(detM)
print('detMf: ', end='')
print(detMf)

rsetM = linsolve((M,b),[x,y,z])
print('rsetM: ', end='')
print(rsetM)

M1 = M.subs(lamb,1)
b1 = b.subs(lamb,1)
print('M1: ', end='')
print(M1)
rsetM1 = linsolve((M1,b1),[x,y,z])
print('rsetM1: ', end='')
print(rsetM1)

Mm2 = M.subs(lamb,-2)
bm2 = b.subs(lamb,-2)
print('Mm2: ', end='')
print(Mm2)
print('bm2: ', end='')
print(bm2)
print('detm2: ', end='')
print(det(Mm2))
rsetMm2 = linsolve((Mm2,bm2),[x,y,z])
print('rsetMm2: ', end='')
print(rsetMm2)

M0 = M.subs(lamb,0)
b0 = b.subs(lamb,0)
print('M0: ', end='')
print(M0)
print('b0: ', end='')
print(b0)
print('detM0: ', end='')
print(det(M0))
rsetM0 = linsolve((M0,b0),[x,y,z])
print('rsetM0: ', end='')
print(rsetM0)

# print((M**-1)*b)

print('M: '+latex(M))
print('V: '+latex(V))
print('b: '+latex(b))
print('detM: '+latex(detM))
print('detMf: '+latex(detMf))

print('M1: '+latex(M1))
print('systM1: '+latex(M1*V-b1))
print('rsetM1: '+latex(rsetM1))

print('Mm2: '+latex(Mm2))
print('systM2: '+latex(Mm2*V-bm2))
print('rsetMm2: '+latex(rsetMm2))

print('M0: '+latex(M0))
print('systM0: '+latex(M0*V-b0))
print('rsetM0: '+latex(rsetM0))

print('M: '+latex(M))
print('systM: '+latex(M*V-b))
print('rsetM: '+latex(rsetM))

