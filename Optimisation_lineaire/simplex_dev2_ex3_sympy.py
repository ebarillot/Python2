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
c = [0, 0, -1]        # attention, linprog cherche à minimiser et non as à maximiser
A = [[-1, -1, 1], [-2, 1, 1], [-1, 1, 1]]
b = [2, 4, 1]
x0_bnds = (0, None)
x1_bnds = (0, None)
x2_bnds = (0, None)
res = linprog(c, A, b, bounds=(x0_bnds, x1_bnds, x2_bnds))
print(res)


from __future__ import print_function
import sympy as sp


# solution numérique
from scipy.optimize import linprog

sp.init_printing(use_unicode=True)

x1, x2, x3, x4, x5, x6 = sp.symbols('x1 x2 x3 x4 x5 x6')

# redéfinis avec des entiers
A = [[-1,-1,1],[-2,1,1],[-1,1,1]]
b = [2,4,1]
c = [ 0, 0, 1] + [0]*len(b) + [0]        # attention, linprog cherche à minimiser et non as à maximiser

M = sp.Matrix(A)
print(M)
M.inv()

V = sp.Matrix(3,1,[x1,x2,x3])
print(V)

b = sp.Matrix(b).transpose()
print(b)

c = sp.Matrix(c).transpose()
print(c)

s0p1 = b.col_join(sp.Matrix([0, 0, 0])).transpose()
cp1 = c

M2 = M.row_join(sp.eye(3)).row_join(b).col_join(cp1)
r1 = M2[0,:]
r2 = M2[1,:]
r3 = M2[2,:]
r4 = M2[3,:]

r1p1 = r1-r3
r2p1 = r2-r3
r3p1 = r3/r3[3-1]
r4p1 = r4-r3
sp.latex(r1p1)
sp.latex(r2p1)
sp.latex(r3p1)
sp.latex(r4p1)