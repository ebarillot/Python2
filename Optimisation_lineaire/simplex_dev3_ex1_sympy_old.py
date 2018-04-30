# coding=utf-8

from __future__ import print_function
import sympy as sp
from typing import List, Dict

sp.init_printing(use_unicode=True)

M = sp.Matrix([[1, -1, 1],
               [2, 1, 3],
               [-1, 0, 1],
               [1, 1, 1]])
print(M)
M.shape
nInB = M.shape[0]
nOuB = M.shape[1]
nvars = nInB + nOuB
vars_list_name = ['x{}'.format(i) for i in range(nvars)]
vars_list = sp.symbols(vars_list_name)
V = sp.Matrix(nvars, 1, vars_list)
print(V)

b = sp.Matrix(M.shape[0], 1, [4, 6, 3, 8])
print(b)

print('M: ' + sp.latex(M))
print('V: ' + sp.latex(V))
print('b: ' + sp.latex(b))
print('systM: ' + sp.latex(M * V[:nOuB, :] - b))


#  solution realisable
Sr = sp.Matrix(3, 1, [0, 6, 0])
print(Sr)
# verification que la solution est réalisable
M.dot(Sr)

# fonction à minimiser
cT = sp.Matrix(1, nvars, [3, 2, 1, 0, 0, 0, 0])
assert (cT.shape[1] == nvars)
g = cT.dot(V)

# Matrice A = (M Id)
A = M.row_join(sp.eye(nInB))
print('systA: ' + sp.latex(A * V - b))

# les indices des colonnes de A, numérotés de 1 à nvars
# de façon à repérer les colonnes eb vase et hors base
# comme dans le cours: de 1 à n
A_col_ind = set([i + 1 for i in range(nvars)])


# le conteneur des solutions testées
sol = list()

#
# une base: colonne 2 de M et colonnes 1 à 3 de IdR4
#  les indices des colonnes EN base
#
numsol = 0  # numero de la base testée
sol.append({})
sol[numsol]['InB'] = [2, 4, 5, 6]
#  les indices des colonnes HORS base
sol[numsol]['OuB'] = list(A_col_ind - set(sol[numsol]['InB']))
assert (len(sol[numsol]['InB']) == nInB)
assert (len(sol[numsol]['OuB']) == nOuB)
sol[numsol]['B'] = A[:, [sol[numsol]['InB'][i] - 1 for i in range(nInB)]]
sol[numsol]['N'] = A[:, [sol[numsol]['OuB'][i] - 1 for i in range(nOuB)]]
sol[numsol]['detB'] = sol[numsol]['B'].det()
if sol[numsol]['detB'] == 0:
    raise Exception('Base de rang < {}, impossible de calculer l\'inverse de B'.format(nInB))
else:
    sol[numsol]['Binv'] = sol[numsol]['B'].inv()
    sol[numsol]['Binv'].multiply(sol[numsol]['B'])
    sol[numsol]['xBsol'] = sol[numsol]['Binv'].multiply(b)
    sol[numsol]['xNsol'] = sp.Matrix(nOuB, 1, [0] * nOuB)
    assert (sol[numsol]['xBsol'].shape[0] == nInB)
    assert (sol[numsol]['xNsol'].shape[0] == nOuB)
    sol[numsol]['cTN'] = sp.Matrix(1, nOuB, [cT[i - 1] for i in sol[numsol]['OuB']])
    sol[numsol]['cTB'] = sp.Matrix(1, nInB, [cT[i - 1] for i in sol[numsol]['InB']])
    assert (sol[numsol]['cTN'].shape[1] == nOuB)
    assert (sol[numsol]['cTB'].shape[1] == nInB)
    sol[numsol]['dTN'] = sol[numsol]['cTN'] - sol[numsol]['cTB']\
        .multiply(sol[numsol]['Binv'])\
        .multiply(sol[numsol]['N'])
    sol[numsol]['dTB'] = sp.Matrix(nInB, 1, [0] * nInB)
    #  la solution complète
    temp_xsol = list([None] * nvars)
    temp_cT = list([None] * nvars)
    temp_dT = list([None] * nvars)
    for i in range(nInB):
        temp_xsol[sol[numsol]['InB'][i] - 1] = sol[numsol]['xBsol'][i]
        temp_cT[sol[numsol]['InB'][i] - 1] = sol[numsol]['cTB'][i]
        temp_dT[sol[numsol]['InB'][i] - 1] = sol[numsol]['dTB'][i]
    for i in range(nOuB):
        temp_xsol[sol[numsol]['OuB'][i] - 1] = sol[numsol]['xNsol'][i]
        temp_cT[sol[numsol]['OuB'][i] - 1] = sol[numsol]['cTN'][i]
        temp_dT[sol[numsol]['OuB'][i] - 1] = sol[numsol]['dTN'][i]
    assert (len([x for x in temp_xsol if x is None]) == 0)  # on a bien toutes les valeurs
    assert (len([x for x in temp_cT if x is None]) == 0)  # on a bien toutes les valeurs
    assert (len([x for x in temp_dT if x is None]) == 0)  # on a bien toutes les valeurs
    sol[numsol]['xsol'] = sp.Matrix(nvars, 1, temp_xsol)
    sol[numsol]['cT'] = sp.Matrix(1, nvars, temp_cT)
    sol[numsol]['dT'] = sp.Matrix(1, nvars, temp_dT)
    assert (sol[numsol]['xsol'].shape[0] == nvars)
    assert (sol[numsol]['xsol'].shape[1] == 1)
    assert (sol[numsol]['cT'].shape[0] == 1)
    assert (sol[numsol]['cT'].shape[1] == nvars)
    assert (sol[numsol]['dT'].shape[0] == 1)
    assert (sol[numsol]['dT'].shape[1] == nvars)
    sol[numsol]['fun'] = sol[numsol]['cT'] * sol[numsol]['xsol']
#  ==> cette base conduit à une solution non réalisable (0, 8, 0, 12, -2, 3, 0) et qui ne conduit pas à x_2 = 6
#      et pour laquelle dT = sol[numsol]['dT'] = (1, 0, -1, 0, 0, 0, -2)


#
# une autre base: colonne 2 de M et colonnes 1, 2 et 4 de IdR4 => matrice B non inversible (rang < 4)
#
numsol = 1  # numero de la base testée
sol.append({})
A
sol[numsol]['InB'] = [2, 4, 5, 7]
#  les indices des colonnes HORS base
sol[numsol]['OuB'] = list(A_col_ind - set(sol[numsol]['InB']))
assert (len(sol[numsol]['InB']) == nInB)
assert (len(sol[numsol]['OuB']) == nOuB)
sol[numsol]['B'] = A[:, [sol[numsol]['InB'][i] - 1 for i in range(nInB)]]
sol[numsol]['N'] = A[:, [sol[numsol]['OuB'][i] - 1 for i in range(nOuB)]]
sol[numsol]['detB'] = sol[numsol]['B'].det()
if sol[numsol]['detB'] == 0:
    raise Exception('Base de rang < {}, impossible de calculer l\'inverse de B'.format(nInB))
else:
    sol[numsol]['Binv'] = sol[numsol]['B'].inv()
    sol[numsol]['Binv'].multiply(sol[numsol]['B'])
    sol[numsol]['xBsol'] = sol[numsol]['Binv'].multiply(b)
    sol[numsol]['xNsol'] = sp.Matrix(nOuB, 1, [0] * nOuB)
    assert (sol[numsol]['xBsol'].shape[0] == nInB)
    assert (sol[numsol]['xNsol'].shape[0] == nOuB)
    sol[numsol]['cTN'] = sp.Matrix(1, nOuB, [cT[i - 1] for i in sol[numsol]['OuB']])
    sol[numsol]['cTB'] = sp.Matrix(1, nInB, [cT[i - 1] for i in sol[numsol]['InB']])
    assert (sol[numsol]['cTN'].shape[1] == nOuB)
    assert (sol[numsol]['cTB'].shape[1] == nInB)
    sol[numsol]['dTN'] = sol[numsol]['cTN'] - sol[numsol]['cTB']\
        .multiply(sol[numsol]['Binv'])\
        .multiply(sol[numsol]['N'])
    sol[numsol]['dTB'] = sp.Matrix(nInB, 1, [0] * nInB)
    #  la solution complète
    temp_xsol = list([None] * nvars)
    temp_cT = list([None] * nvars)
    temp_dT = list([None] * nvars)
    for i in range(nInB):
        temp_xsol[sol[numsol]['InB'][i] - 1] = sol[numsol]['xBsol'][i]
        temp_cT[sol[numsol]['InB'][i] - 1] = sol[numsol]['cTB'][i]
        temp_dT[sol[numsol]['InB'][i] - 1] = sol[numsol]['dTN'][i]
    for i in range(nOuB):
        temp_xsol[sol[numsol]['OuB'][i] - 1] = sol[numsol]['xNsol'][i]
        temp_cT[sol[numsol]['OuB'][i] - 1] = sol[numsol]['cTN'][i]
        temp_cT[sol[numsol]['OuB'][i] - 1] = sol[numsol]['dTN'][i]
    assert (len([x for x in temp_xsol if x is None]) == 0)  # on a bien toutes les valeurs
    assert (len([x for x in temp_cT if x is None]) == 0)  # on a bien toutes les valeurs
    assert (len([x for x in temp_dT if x is None]) == 0)  # on a bien toutes les valeurs
    sol[numsol]['xsol'] = sp.Matrix(nvars, 1, temp_xsol)
    sol[numsol]['cT'] = sp.Matrix(1, nvars, temp_cT)
    sol[numsol]['dT'] = sp.Matrix(1, nvars, temp_dT)
    assert (sol[numsol]['xsol'].shape[0] == nvars)
    assert (sol[numsol]['xsol'].shape[1] == 1)
    assert (sol[numsol]['cT'].shape[0] == 1)
    assert (sol[numsol]['cT'].shape[1] == nvars)
    assert (sol[numsol]['dT'].shape[0] == 1)
    assert (sol[numsol]['dT'].shape[1] == nvars)
    sol[numsol]['fun'] = sol[numsol]['cT'] * sol[numsol]['xsol']


#
# une autre base: colonne 2 de M et colonnes 1, 3 et 4 de IdR4
#
numsol = 2  # numero de la base testée
sol.append({})
A
sol[numsol]['InB'] = [2, 4, 6, 7]
#  les indices des colonnes HORS base
sol[numsol]['OuB'] = list(A_col_ind - set(sol[numsol]['InB']))
assert (len(sol[numsol]['InB']) == nInB)
assert (len(sol[numsol]['OuB']) == nOuB)
sol[numsol]['B'] = A[:, [sol[numsol]['InB'][i] - 1 for i in range(nInB)]]
sol[numsol]['N'] = A[:, [sol[numsol]['OuB'][i] - 1 for i in range(nOuB)]]
sol[numsol]['detB'] = sol[numsol]['B'].det()
if sol[numsol]['detB'] == 0:
    raise Exception('Base de rang < {}, impossible de calculer l\'inverse de B'.format(nInB))
else:
    sol[numsol]['Binv'] = sol[numsol]['B'].inv()
    sol[numsol]['Binv'].multiply(sol[numsol]['B'])
    sol[numsol]['xBsol'] = sol[numsol]['Binv'].multiply(b)
    sol[numsol]['xNsol'] = sp.Matrix(nOuB, 1, [0] * nOuB)
    assert (sol[numsol]['xBsol'].shape[0] == nInB)
    assert (sol[numsol]['xNsol'].shape[0] == nOuB)
    sol[numsol]['cTN'] = sp.Matrix(1, nOuB, [cT[i - 1] for i in sol[numsol]['OuB']])
    sol[numsol]['cTB'] = sp.Matrix(1, nInB, [cT[i - 1] for i in sol[numsol]['InB']])
    assert (sol[numsol]['cTN'].shape[1] == nOuB)
    assert (sol[numsol]['cTB'].shape[1] == nInB)
    sol[numsol]['dTN'] = sol[numsol]['cTN'] - sol[numsol]['cTB']\
        .multiply(sol[numsol]['Binv'])\
        .multiply(sol[numsol]['N'])
    sol[numsol]['dTB'] = sp.Matrix(nInB, 1, [0] * nInB)
    #  la solution complète
    temp_xsol = list([None] * nvars)
    temp_cT = list([None] * nvars)
    temp_dT = list([None] * nvars)
    for i in range(nInB):
        temp_xsol[sol[numsol]['InB'][i] - 1] = sol[numsol]['xBsol'][i]
        temp_cT[sol[numsol]['InB'][i] - 1] = sol[numsol]['cTB'][i]
        temp_dT[sol[numsol]['InB'][i] - 1] = sol[numsol]['dTB'][i]
    for i in range(nOuB):
        temp_xsol[sol[numsol]['OuB'][i] - 1] = sol[numsol]['xNsol'][i]
        temp_cT[sol[numsol]['OuB'][i] - 1] = sol[numsol]['cTN'][i]
        temp_dT[sol[numsol]['OuB'][i] - 1] = sol[numsol]['dTN'][i]
    assert (len([x for x in temp_xsol if x is None]) == 0)  # on a bien toutes les valeurs
    assert (len([x for x in temp_cT if x is None]) == 0)  # on a bien toutes les valeurs
    assert (len([x for x in temp_dT if x is None]) == 0)  # on a bien toutes les valeurs
    sol[numsol]['xsol'] = sp.Matrix(nvars, 1, temp_xsol)
    sol[numsol]['cT'] = sp.Matrix(1, nvars, temp_cT)
    sol[numsol]['dT'] = sp.Matrix(1, nvars, temp_dT)
    assert (sol[numsol]['xsol'].shape[0] == nvars)
    assert (sol[numsol]['xsol'].shape[1] == 1)
    assert (sol[numsol]['cT'].shape[0] == 1)
    assert (sol[numsol]['cT'].shape[1] == nvars)
    assert (sol[numsol]['dT'].shape[0] == 1)
    assert (sol[numsol]['dT'].shape[1] == nvars)
    sol[numsol]['fun'] = sol[numsol]['cT'] * sol[numsol]['xsol']
#  cette base conduit à une solution réalisable (0, 6, 0, 10, 0, 3, 2) qui conduit bien à x_2 = 6
#  et pour laquelle dTN = [-1  0  -5  0  -2  0  0] n'a que des coefficients négatifs


#
# une autre base: colonne 2 de M et colonnes 2, 3 et 4 de IdR4
#
numsol = 3
sol.append({})
A
sol[numsol]['InB'] = [2, 5, 6, 7]
#  les indices des colonnes HORS base
sol[numsol]['OuB'] = list(A_col_ind - set(sol[numsol]['InB']))
assert (len(sol[numsol]['InB']) == nInB)
assert (len(sol[numsol]['OuB']) == nOuB)
sol[numsol]['B'] = A[:, [sol[numsol]['InB'][i] - 1 for i in range(nInB)]]
sol[numsol]['N'] = A[:, [sol[numsol]['OuB'][i] - 1 for i in range(nOuB)]]
sol[numsol]['detB'] = sol[numsol]['B'].det()
if sol[numsol]['detB'] == 0:
    raise Exception('Base de rang < {}, impossible de calculer l\'inverse de B'.format(nInB))
else:
    sol[numsol]['Binv'] = sol[numsol]['B'].inv()
    sol[numsol]['Binv'].multiply(sol[numsol]['B'])
    sol[numsol]['xBsol'] = sol[numsol]['Binv'].multiply(b)
    sol[numsol]['xNsol'] = sp.Matrix(nOuB, 1, [0] * nOuB)
    assert (sol[numsol]['xBsol'].shape[0] == nInB)
    assert (sol[numsol]['xNsol'].shape[0] == nOuB)
    sol[numsol]['cTN'] = sp.Matrix(1, nOuB, [cT[i - 1] for i in sol[numsol]['OuB']])
    sol[numsol]['cTB'] = sp.Matrix(1, nInB, [cT[i - 1] for i in sol[numsol]['InB']])
    assert (sol[numsol]['cTN'].shape[1] == nOuB)
    assert (sol[numsol]['cTB'].shape[1] == nInB)
    sol[numsol]['dTN'] = sol[numsol]['cTN'] - sol[numsol]['cTB']\
        .multiply(sol[numsol]['Binv'])\
        .multiply(sol[numsol]['N'])
    sol[numsol]['dTB'] = sp.Matrix(nInB, 1, [0] * nInB)
    #  la solution complète
    temp_xsol = list([None] * nvars)
    temp_cT = list([None] * nvars)
    temp_dT = list([None] * nvars)
    for i in range(nInB):
        temp_xsol[sol[numsol]['InB'][i] - 1] = sol[numsol]['xBsol'][i]
        temp_cT[sol[numsol]['InB'][i] - 1] = sol[numsol]['cTB'][i]
        temp_dT[sol[numsol]['InB'][i] - 1] = sol[numsol]['dTB'][i]
    for i in range(nOuB):
        temp_xsol[sol[numsol]['OuB'][i] - 1] = sol[numsol]['xNsol'][i]
        temp_cT[sol[numsol]['OuB'][i] - 1] = sol[numsol]['cTN'][i]
        temp_dT[sol[numsol]['OuB'][i] - 1] = sol[numsol]['dTN'][i]
    assert (len([x for x in temp_xsol if x is None]) == 0)  # on a bien toutes les valeurs
    assert (len([x for x in temp_cT if x is None]) == 0)  # on a bien toutes les valeurs
    assert (len([x for x in temp_dT if x is None]) == 0)  # on a bien toutes les valeurs
    sol[numsol]['xsol'] = sp.Matrix(nvars, 1, temp_xsol)
    sol[numsol]['cT'] = sp.Matrix(1, nvars, temp_cT)
    sol[numsol]['dT'] = sp.Matrix(1, nvars, temp_dT)
    assert (sol[numsol]['xsol'].shape[0] == nvars)
    assert (sol[numsol]['xsol'].shape[1] == 1)
    assert (sol[numsol]['cT'].shape[0] == 1)
    assert (sol[numsol]['cT'].shape[1] == nvars)
    assert (sol[numsol]['dT'].shape[0] == 1)
    assert (sol[numsol]['dT'].shape[1] == nvars)
    sol[numsol]['fun'] = sol[numsol]['cT'] * sol[numsol]['xsol']
# ==> conduit à une solution non realisable: [0  -4  0  0  10  3  12]
#     avec dT = [5  0  3  2  0  0  0]



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
cTNdual = cTdual[:, [0, 2]].row_join(sp.Matrix(1, 1, [0]))
cTBdual = cTdual[:, [1, 3]].row_join(sp.Matrix(1, 1, [0]))
soldual[numsol]['dTN'] = cTNdual - cTBdual.multiply(soldual[numsol]['Bdualinv'])
#  cette base conduit à une solution non réalisable (0, 8, 0, 12, -1, 3, 0) et qui ne conduit pas à x_2 = 6
