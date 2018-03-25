# coding=utf-8

from __future__ import print_function
import sympy as sp

sp.init_printing(use_unicode=True)

x1, x2, x3, x4, x5, x6, x7 = sp.symbols('x1 x2 x3 x4, x5, x6, x7')

M = sp.Matrix([[1, -1, 1],
               [2, 1, 3],
               [-1, 0, 1],
               [1, 1, 1]])
print(M)

V = sp.Matrix(4, 1, [x1, x2, x3, x4])
print(V)

b = sp.Matrix([[4, 6, 3, 8]]).transpose()
print(b)

print('M: ' + sp.latex(M))
print('V: ' + sp.latex(V))
print('b: ' + sp.latex(b))
print('systM: ' + sp.latex(M * V - b))

#  solution realisable
Sr = sp.Matrix([[0, 6, 0]]).transpose()
print(Sr)
# verification que la solution est réalisable
M.dot(Sr)

# fonction à minimiser, fonction implicitement définie avec les variables x1, x2, x3
cT = sp.Matrix([[3, 2, 1, 0]])
g = cT.dot(V)

sol = list()
# une base: colonne 2 de M et colonnes 1 à 3 de IdR4
sol.append({})
numsol = 0
sol[numsol]['B'] = M[:, 1].row_join(sp.eye(4)[:, 0:3])
sol[numsol]['Binv'] = sol[numsol]['B'].inv()
sol[numsol]['Binv'].multiply(sol[numsol]['B'])
sp.latex(sol[numsol]['Binv'])
sol[numsol]['xBs'] = sol[numsol]['Binv'].multiply(b)
sol[numsol]['xNs'] = sp.Matrix(3, 1, [0, 0, 0])
sol[numsol]['dTN'] = -cT.multiply(sol[numsol]['Binv'])
#  cette base conduit à une solution non réalisable (0, 8, 0, 12, -1, 3, 0) et qui ne conduit pas à x_2 = 6

# une autre base: colonne 2 de M et colonnes 1, 2 et 4 de IdR4 => matrice B non inversible (rang < 4)

# une autre base: colonne 2 de M et colonnes 1, 3 et 4 de IdR4
sol.append({})
numsol = 1
sol[numsol]['B'] = M[:, 1].row_join(sp.eye(4)[:, [0, 2, 3]])
sol[numsol]['Binv'] = sol[numsol]['B'].inv()
sol[numsol]['Binv'].multiply(sol[numsol]['B'])
sp.latex(sol[numsol]['Binv'])
sol[numsol]['xBs'] = sol[numsol]['Binv'].multiply(b)
sol[numsol]['xNs'] = sp.Matrix(3, 1, [0, 0, 0])
sol[numsol]['dTN'] = -cT.multiply(sol[numsol]['Binv'])
#  cette base conduit à une solution réalisable (0, 6, 0, 10, , 3, 2) qui conduit bien à x_2 = 6
#  et pour laquelle dTN n'a que des coefficients négatifs

[sol[numsol]['dTN'] for numsol in range(2)]

# une autre base: colonne 2 de M et colonnes 2, 3 et 4 de IdR4
sol.append({})
numsol = 2
sol[numsol]['B'] = M[:, 1].row_join(sp.eye(4)[:, [1, 2, 3]])
sol[numsol]['Binv'] = sol[numsol]['B'].inv()
sol[numsol]['Binv'].multiply(sol[numsol]['B'])
sp.latex(sol[numsol]['Binv'])
sol[numsol]['xBs'] = sol[numsol]['Binv'].multiply(b)
sol[numsol]['xNs'] = sp.Matrix(3, 1, [0, 0, 0])
sol[numsol]['dTN'] = -cT.multiply(sol[numsol]['Binv'])
#  cette base conduit à une solution non réalisable

[(sol[numsol]['xBs'], sol[numsol]['dTN']) for numsol in range(3)]
#  on voit que c'est le choix de base colonne 2 de M et colonnes 1, 3 et 4 de IdR4
# qui conduit à la bonne solution


# solution numérique
from scipy.optimize import linprog

c = [-3, -2, -1]  # attention, linprog cherche à minimiser et non pas à maximiser
A = [[1, -1, 1],
     [2, 1, 3],
     [-1, 0, 1],
     [1, 1, 1]]
b = [4, 6, 3, 8]
x0_bnds = (0, None)
x1_bnds = (0, None)
x2_bnds = (0, None)
res = linprog(c, A, b, bounds=(x0_bnds, x1_bnds, x2_bnds))
print(res)

#  problème dual
Mdual = -M.transpose()
print(Mdual)

y1, y2, y3, y4, y5, y6, y7 = sp.symbols('y1 y2 y3 y4, y5, y6, y7')

Vdual = sp.Matrix(4, 1, [y1, y2, y3, y4])
print(Vdual)
cT
bdual = -cT.transpose()[:3, :]
print(bdual)

b
cTdual = -b.transpose()

print('Mdual: ' + sp.latex(Mdual))
print('Vdual: ' + sp.latex(Vdual))
print('bdual: ' + sp.latex(bdual))
print('systMdual: ' + sp.latex(Mdual * Vdual - bdual))

# une solution de départ réalisable
Mdual * sp.Matrix(4, 1, [0, 1, 0, 1])
bdual

# recherche base réalisable de départ
soldual = list()
# une base: colonne 2 et 4 de M et colonnes 1 de IdR3
soldual.append({})
numsol = 0
soldual[numsol]['Bdual'] = Mdual[:, [1, 3]].row_join(sp.eye(3)[:, 0])
soldual[numsol]['Bdualinv'] = soldual[numsol]['Bdual'].inv()
soldual[numsol]['Bdualinv'].multiply(soldual[numsol]['Bdual'])
sp.latex(soldual[numsol]['Bdualinv'])
soldual[numsol]['xBs'] = soldual[numsol]['Bdualinv'].multiply(bdual)
soldual[numsol]['xNs'] = sp.Matrix(4, 1, [0, 0, 0, 0])
cTNdual = cTdual[:, [0, 2]].row_join(sp.Matrix(1,1, [0]))
cTBdual = cTdual[:, [1, 3]].row_join(sp.Matrix(1,1, [0]))
soldual[numsol]['dTN'] = cTNdual-cTBdual.multiply(soldual[numsol]['Bdualinv'])
#  cette base conduit à une solution non réalisable (0, 8, 0, 12, -1, 3, 0) et qui ne conduit pas à x_2 = 6
