# coding=utf-8

from __future__ import print_function
import sympy as sp

from Optimisation_lineaire.simplex_fun \
    import pvar, simplex_step, solution_numerique, simplex_callback_print, sol_is_real

sp.init_printing(use_unicode=True)

####################################################################
# calcul solution numérique
# if True:
if False:
    c = [-3, -2, -1]  # attention, linprog cherche à minimiser et non pas à maximiser
    A = [[1, -1, 1],
         [2, 1, 3],
         [-1, 0, 1],
         [1, 1, 1]]
    b = [4, 6, 3, 8]
    solution_numerique(A, b, c)

####################################################################
# solution symbolique
M = sp.Matrix([[1, -1, 1],
               [2, 1, 3],
               [-1, 0, 1],
               [1, 1, 1]])

pvar('M')
pvar('M.shape')
nInB = M.shape[0]
nOuB = M.shape[1]
nvars = nInB + nOuB
vars_list_name = ['x{}'.format(i) for i in range(nvars)] + ['b00']
vars_list = sp.symbols(vars_list_name)
V = sp.Matrix(nvars, 1, vars_list[:nvars])
Vtab = sp.Matrix(nvars+1, 1, vars_list)
pvar('V')
pvar('Vtab')

b = sp.Matrix(M.shape[0], 1, [4, 6, 3, 8])
pvar('b')

# fonction à minimiser
cT = sp.Matrix(1, nvars, [3, 2, 1, 0, 0, 0, 0])
assert (cT.shape[1] == nvars)
g = cT.dot(V)
pvar('g')

#  solution realisable
xBbase = sp.Matrix(3, 1, [0, 6, 0])
xbase  = sp.Matrix(nvars, 1, [0, 6, 0, 0, 0, 0, 0])
pvar('xBbase')
# verification que la solution est réalisable
pvar('sol_is_real(xBbase, M, b)')
# all([_x >= 0 for _x in xBbase[:, 0]]) # toutes les composantes sont >= 0
# all([_x <= 0 for _x in (M * xBbase - b)[:, 0]]) # tout est <= 0 dans le système: les contraintes sont bien vérifiées


sol = list()
# matrice de départ complète
A = M.row_join(sp.eye(M.shape[0]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [2, 4, 5, 6]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [2, 4, 5, 7]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [2, 4, 6, 7]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [2, 5, 6, 7]]))

for _i in range(len(sol)):
    print('-------------')
    print('solution: {}'.format(_i + 1))
    for _k in sol[_i].keys():
        print('{}: {}'.format(_k, sol[_i][_k]))

for _i in range(len(sol)):
    print('-------------')
    print('solution: {}'.format(_i + 1))
    pvar('[x+1 for x in sol[_i]["InB"]]')
    pvar('sol[_i]["ret"]')
    print('B: ' + sp.latex(sol[_i]["B"], mode='equation*'))
    pvar('sol[_i]["detB"]')
    if sol[_i]["ret"] == 'OK':
        print('Binv: ' + sp.latex(sol[_i]["Binv"], mode='equation*'))
        print('dTN: ' + sp.latex(sol[_i]["dTN"], mode='equation*'))
        print('xsol: ' + sp.latex(sol[_i]["xsol"], mode='equation*'))

# la solution réalisable trouvée est: soldual[5]
sol_real = [_x for _x in sol if _x['real']]
pvar('len(sol_real)')
pvar('sol_real[0]["fun"]')
pvar('sol_real[0]["cT"]')
pvar('sol_real[0]["cTB"]')
pvar('sol_real[0]["cTN"]')
pvar('sol_real[0]["dT"]')
pvar('sol_real[0]["dTB"]')
pvar('sol_real[0]["dTN"]')
pvar('sol_real[0]["Binv"]')
pvar('sol_real[0]["xsol"]')
pvar('sol_real[0]["tableau"]')
pvar("Vtab.transpose().col_join(sol_real[{}]['tableau'])".format(0))
print(sp.latex(sol_real[0]["Binv"], mode='equation*'))
-sol_real[0]["cTB"] * sol_real[0]["Binv"]

sol_real[0]["cT"]*xbase
sol_real[0]["cT"]*sol_real[0]["xsol"]

# exit()

####################################################################
#  problème dual
print('\n**** PROBLÈME DUAL ****\n')
Mdual = -M.transpose()
pvar('Mdual.shape')
pvar('Mdual')
nInBdual = Mdual.shape[0]
nOuBdual = Mdual.shape[1]
nvarsdual = nInBdual + nOuBdual
vars_list_name_dual = ['y{}'.format(i) for i in range(nvarsdual)]
vars_list_dual = sp.symbols(vars_list_name_dual)
Vdual = sp.Matrix(nvarsdual, 1, vars_list_dual)
pvar('Vdual')

pvar('cT')
bdual = -cT.transpose()[:3, :]
pvar('bdual')

pvar('b')
cTdual = -b.transpose()
# on complète le vecteur avec des 0
cTdual = cTdual.row_join(sp.Matrix(1, nvarsdual - len(cTdual), [0] * (nvarsdual - len(cTdual))))
pvar('cTdual')
assert (cTdual.shape[1] == nvarsdual)
gdual = cTdual.dot(Vdual)
pvar('gdual')

print('Mdual: ' + sp.latex(Mdual))
print('Vdual: ' + sp.latex(Vdual))
print('bdual: ' + sp.latex(bdual))
print('systMdual: ' + sp.latex(Mdual * Vdual[:Mdual.shape[1], :] - bdual))


step = 0
print('\n**** PROBLÈME DUAL STEP {} ****\n'.format(step))
soldual = list()
# matrice de départ complète
Adual = list()
Adual.append([])
Adual[step] = Mdual.row_join(sp.eye(Mdual.shape[0]))

# une solution de départ réalisable (vérifiée)
Mdual * sp.Matrix(4, 1, [0, 1, 0, 1])
# comme les variables non nulles sont les colonnes 2 et 4, on va essayer
# toutes les combinaisons avec ces deux colonnes en base pour trouver laquelle convient
soldual.append(simplex_step(_A=Adual[step], _b=bdual, _cT=cTdual, _InB=[i-1 for i in [1, 2, 4]]))
soldual.append(simplex_step(_A=Adual[step], _b=bdual, _cT=cTdual, _InB=[i-1 for i in [2, 3, 4]]))
soldual.append(simplex_step(_A=Adual[step], _b=bdual, _cT=cTdual, _InB=[i-1 for i in [2, 4, 5]]))
soldual.append(simplex_step(_A=Adual[step], _b=bdual, _cT=cTdual, _InB=[i-1 for i in [2, 4, 6]]))
soldual.append(simplex_step(_A=Adual[step], _b=bdual, _cT=cTdual, _InB=[i-1 for i in [2, 4, 7]]))

for _i in range(len(soldual)):
    print('-------------')
    print('solution: {}'.format(_i + 1))
    for _k in soldual[_i].keys():
        print('{}: {}'.format(_k, soldual[_i][_k]))

# la solution réalisable trouvée est: soldual[5]
soldual_real = [_x for _x in soldual if _x['real']]

pvar("soldual_real[{}]['A']".format(step))
pvar("soldual_real[{}]['BinvN']".format(step))
pvar("soldual_real[{}]['InB']".format(step))
pvar("soldual_real[{}]['OuB']".format(step))
pvar("soldual_real[{}]['Binvb']".format(step))
pvar("soldual_real[{}]['xsol'][soldual_real[{}]['InB'], :]".format(step, step))
pvar("soldual_real[{}]['xsol'].transpose()".format(step))
pvar("soldual_real[{}]['BinvA']".format(step))
pvar("soldual_real[{}]['dT']".format(step))
pvar("soldual_real[{}]['tableau']".format(step))
print(sp.latex(soldual_real[step]['tableau'], mode='equation*'))


# au vu du tableau, on peut faire entrer 5 et sortir 4
# la base devient [2, 5, 7]
step = 1
print('\n**** PROBLÈME DUAL STEP {} ****\n'.format(step))
Adual.append([])
# la nouvelle matrice A est égale à BinvA de l'étape précédente
Adual[step] = soldual_real[0]['BinvA']
soldual_real.append([])
soldual_real[step] = simplex_step(_A=soldual_real[step - 1]['BinvA'],
                                  _b=soldual_real[step - 1]['Binvb'],
                                  _cT=soldual_real[step - 1]['cT'],
                                  _InB=[i-1 for i in [2, 5, 7]])
pvar("soldual_real[{}]['A']".format(step))
pvar("soldual_real[{}]['BinvN']".format(step))
pvar("soldual_real[{}]['InB']".format(step))
pvar("soldual_real[{}]['OuB']".format(step))
pvar("soldual_real[{}]['Binvb']".format(step))
pvar("soldual_real[{}]['xsol'][soldual_real[{}]['InB'], :]".format(step, step))
pvar("soldual_real[{}]['xsol'].transpose()".format(step))
pvar("soldual_real[{}]['BinvA']".format(step))
pvar("soldual_real[{}]['dT']".format(step))
pvar("soldual_real[{}]['tableau']".format(step))

print(sp.latex(soldual_real[step]['tableau'], mode='equation'))


# résolution numérique du probleme dual
l_Mdual = Mdual.tolist()
l_bdual = list(bdual)
l_cdual = [-x for x in list(cTdual[:, :Mdual.shape[1]])]
solution_numerique(l_Mdual, l_bdual, l_cdual, simplex_callback_print)


# exit()

# # recherche base réalisable de départ
# soldual = list()
# # une base: colonne 2 et 4 de M et colonnes 1 de IdR3
# soldual.append({})
# numsol = 0
# soldual[numsol]['Bdual'] = Mdual[:, [1, 3]].row_join(sp.eye(3)[:, 0])
# soldual[numsol]['Bdualinv'] = soldual[numsol]['Bdual'].inv()
# soldual[numsol]['Bdualinv'].multiply(soldual[numsol]['Bdual'])
# sp.latex(soldual[numsol]['Bdualinv'])
# soldual[numsol]['xBs'] = soldual[numsol]['Bdualinv'].multiply(bdual)
# soldual[numsol]['xNs'] = sp.Matrix(4, 1, [0, 0, 0, 0])
# cTNdual = cTdual[:, [0, 2]].row_join(sp.Matrix(1, 1, [0]))
# cTBdual = cTdual[:, [1, 3]].row_join(sp.Matrix(1, 1, [0]))
# soldual[numsol]['dTN'] = cTNdual - cTBdual.multiply(soldual[numsol]['Bdualinv'])
# #  cette base conduit à une solution non réalisable (0, 8, 0, 12, -1, 3, 0) et qui ne conduit pas à x_2 = 6

