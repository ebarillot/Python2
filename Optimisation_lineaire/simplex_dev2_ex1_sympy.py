# coding=utf-8

from __future__ import print_function
import sympy as sp

sp.init_printing(use_unicode=True)

x, y = sp.symbols('x y ')

M = sp.Matrix(2,2,[3,1,1,4])
print('M: ', end='')
print(M)

V = sp.Matrix(2,1,[x,y])
print('V: ', end='')
print(V)

b = sp.Matrix([[1,1]]).transpose()
print('b: ', end='')
print(b)

detM = sp.det(M)
detMf = sp.factor(detM)
print('detM: ', end='')
print(detM)
print('detMf: ', end='')
print(detMf)

rsetM = sp.linsolve((M,b),[x,y])
print('rsetM: ', end='')
print(rsetM)


# print((M**-1)*b)

print('M: '+sp.latex(M))
print('V: '+sp.latex(V))
print('b: '+sp.latex(b))
print('detM: '+sp.latex(detM))
print('detMf: '+sp.latex(detMf))


print('M: '+sp.latex(M))
print('systM: '+sp.latex(M*V-b))
print('rsetM: '+sp.latex(rsetM))

# Sr = sp.Matrix([[sp.fraction(sp.Rational(3,11)),sp.fraction(sp.Rational(2,11))]]).transpose()
Sr = sp.Matrix([[sp.Rational(3,11),sp.Rational(2,11)]]).transpose()
print('Sr: ', end='')
print(Sr)

M.dot(Sr)

# fonction à maximiser, fonction implicitement définie avec les variables x et y
g = -4*x - 5*y

4*sp.Rational(3,11) + 5*sp.Rational(2,11)

# inverse dela matrice
Minv = M.inv()

sp.latex(M.inv())

sp.Matrix(2,1,[4,5]).transpose() * (Minv)
sp.Matrix(2,1,[4,5]).transpose().multiply(Minv)


# solution numérique
from scipy.optimize import linprog
c = [-4, -5]        # attention, linprog cherche à minimiser et non as à maximiser
A = [[3, 1], [1, 4]]
b = [1, 1]
x0_bnds = (0, None)
x1_bnds = (0, None)
res = linprog(c, A, b, bounds=(x0_bnds, x1_bnds))
print(res)
