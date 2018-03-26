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

# fonction à minimiser
cT = sp.Matrix(1, nvars, [3, 2, 1, 0, 0, 0, 0])
assert (cT.shape[1] == nvars)
g = cT.dot(V)

#  solution realisable
xBbase = sp.Matrix(3, 1, [0, 6, 0])
print(xBbase)
# verification que la solution est réalisable
M.dot(xBbase)


def base_is_optimale(_A, _b, _cT, _InB):
    _nInB = _A.shape[0]
    _nvars = _A.shape[1]
    _nOuB = _nvars - _nInB
    _A_col_ind = set([_i + 1 for _i in range(_nvars)])
    _cT = _cT.row_join(sp.Matrix(1, _nvars - len(_cT), [0] * (_nvars - len(_cT))))  # on complète le vecteur avec des 0
    assert (_cT.shape[1] == _nvars)
    #  les indices des colonnes HORS base
    _OuB = list(_A_col_ind - set(_InB))
    assert (len(_InB) == _nInB)
    assert (len(_OuB) == _nOuB)
    _B = _A[:, [_InB[_i] - 1 for _i in range(_nInB)]]
    _N = _A[:, [_OuB[_i] - 1 for _i in range(_nOuB)]]
    _detB = _B.det()
    _sol = dict()
    if _detB == 0:
        _sol['A'] = _A
        _sol['b'] = _b
        _sol['InB'] = _InB
        _sol['ret'] = 'Base de rang < {}, impossible de calculer l\'inverse de B'.format(_nInB)
    else:
        _Binv = _B.inv()
        assert (_Binv * _B == sp.eye(_nInB))
        _Binv_N = _Binv * _N
        _Binv_b = _Binv * _b
        #  solution de base
        _xBsol = _Binv_b
        _xNsol = sp.Matrix(_nOuB, 1, [0] * _nOuB)   # que des 0
        assert (_xBsol.shape[0] == _nInB)
        assert (_xNsol.shape[0] == _nOuB)
        _cTN = sp.Matrix(1, _nOuB, [_cT[_i - 1] for _i in _OuB])
        _cTB = sp.Matrix(1, _nInB, [_cT[_i - 1] for _i in _InB])
        assert (_cTN.shape[1] == _nOuB)
        assert (_cTB.shape[1] == _nInB)
        _dTN = _cTN - _cTB * _Binv_N
        _dTB = sp.Matrix(_nInB, 1, [0] * _nInB) # que des 0
        #  la solution complète
        _temp_xsol = list([None] * _nvars)
        _temp_cT = list([None] * _nvars)
        _temp_dT = list([None] * _nvars)
        for _i in range(_nInB):
            _temp_xsol[_InB[_i] - 1] = _xBsol[_i]
            _temp_cT[_InB[_i] - 1] = _cTB[_i]
            _temp_dT[_InB[_i] - 1] = _dTB[_i]
        for _i in range(_nOuB):
            _temp_xsol[_OuB[_i] - 1] = _xNsol[_i]
            _temp_cT[_OuB[_i] - 1] = _cTN[_i]
            _temp_dT[_OuB[_i] - 1] = _dTN[_i]
        assert (len([_x for _x in _temp_xsol if _x is None]) == 0)  # on a bien toutes les valeurs
        assert (len([_x for _x in _temp_cT if _x is None]) == 0)  # on a bien toutes les valeurs
        assert (len([_x for _x in _temp_dT if _x is None]) == 0)  # on a bien toutes les valeurs
        _xsol = sp.Matrix(_nvars, 1, _temp_xsol)
        _cT = sp.Matrix(1, _nvars, _temp_cT)
        _dT = sp.Matrix(1, _nvars, _temp_dT)
        assert (_xsol.shape[0] == _nvars)
        assert (_xsol.shape[1] == 1)
        assert (_cT.shape[0] == 1)
        assert (_cT.shape[1] == _nvars)
        assert (_dT.shape[0] == 1)
        assert (_dT.shape[1] == _nvars)
        _fun = _cT * _xsol
        _sol['A'] = _A
        _sol['b'] = _b
        _sol['InB'] = _InB
        _sol['OuB'] = _OuB
        _sol['cT'] = _cT
        _sol['dT'] = _dT
        _sol['xsol'] = _xsol
        _sol['Binv'] = _Binv
        _sol['detB'] = _detB
        _sol['Binvb'] = _Binv_b
        _sol['BinvN'] = _Binv_N
        _sol['fun'] = _fun
        _sol['real'] = all([_x >= 0 for _x in _xsol[:, 0]])
        _sol['ret'] = 'OK'
    return _sol


def solution_numerique():
    # solution numérique du problème
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


# if __name__ == "__main__":
solution_numerique()

sol = list()
# xBbase = sp.Matrix(3, 1, [0, 0, 0])

# matrice de départ complète
A = M.row_join(sp.eye(M.shape[0]))
sol.append(base_is_optimale(_A=A, _b=b, _cT=cT, _InB=[2, 4, 5, 6]))
sol.append(base_is_optimale(_A=A, _b=b, _cT=cT, _InB=[2, 4, 5, 7]))
sol.append(base_is_optimale(_A=A, _b=b, _cT=cT, _InB=[2, 4, 6, 7]))
sol.append(base_is_optimale(_A=A, _b=b, _cT=cT, _InB=[2, 5, 6, 7]))

for _i in range(len(sol)):
    print('-------------')
    print('solution: {}'.format(_i+1))
    for _k in sol[_i].keys():
        print('{}: {}'.format(_k, sol[_i][_k]))

# la solution réalisable trouvée est: soldual[5]
sol_real = [_x for _x in sol if _x['real']]




#  problème dual
Mdual = -M.transpose()
Mdual.shape
print(Mdual)
nInBdual = Mdual.shape[0]
nOuBdual = Mdual.shape[1]
nvarsdual = nInBdual + nOuBdual
vars_list_name_dual = ['y{}'.format(i) for i in range(nvarsdual)]
vars_list_dual = sp.symbols(vars_list_name_dual)
Vdual = sp.Matrix(nvarsdual, 1, vars_list_dual)
print(Vdual)

cT
bdual = -cT.transpose()[:3, :]
print(bdual)

b
cTdual = -b.transpose()
cTdual = cTdual\
    .row_join(sp.Matrix(1, nvarsdual - len(cTdual), [0] * (nvarsdual - len(cTdual))))  # on complète le vecteur avec des 0
print(cTdual)
assert (cTdual.shape[1] == nvarsdual)
gdual = cTdual.dot(Vdual)

print('Mdual: ' + sp.latex(Mdual))
print('Vdual: ' + sp.latex(Vdual))
print('bdual: ' + sp.latex(bdual))
print('systMdual: ' + sp.latex(Mdual * Vdual[:Mdual.shape[1], :] - bdual))


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

soldual = list()
# matrice de départ complète
Adual = list()
Adual.append([])
Adual[0] = Mdual.row_join(sp.eye(Mdual.shape[0]))

# une solution de départ réalisable (vérifiée)
Mdual * sp.Matrix(4, 1, [0, 1, 0, 1])
# comme les variables non nulles sont les colonnes 2 et 4, on va essayer
# toutes les combinaisons avec ces deux colonnes en base pour trouver laquelle convient
soldual.append(base_is_optimale(_A=Adual[0], _b=bdual, _cT=cTdual, _InB=[1, 2, 4]))
soldual.append(base_is_optimale(_A=Adual[0], _b=bdual, _cT=cTdual, _InB=[2, 3, 4]))
soldual.append(base_is_optimale(_A=Adual[0], _b=bdual, _cT=cTdual, _InB=[2, 4, 5]))
soldual.append(base_is_optimale(_A=Adual[0], _b=bdual, _cT=cTdual, _InB=[2, 4, 6]))
soldual.append(base_is_optimale(_A=Adual[0], _b=bdual, _cT=cTdual, _InB=[2, 4, 7]))

for _i in range(len(soldual)):
    print('-------------')
    print('solution: {}'.format(_i+1))
    for _k in soldual[_i].keys():
        print('{}: {}'.format(_k, soldual[_i][_k]))


# la solution réalisable trouvée est: soldual[5]
soldual_real = [_x for _x in soldual if _x['real']]

soldual_real[0]['A']
soldual_real[0]['BinvN']
soldual_real[0]['InB']
soldual_real[0]['OuB']
soldual_real[0]['Binvb']
soldual_real[0]['xsol'][[_i-1 for _i in soldual_real[0]['InB']], :]

# construction de la nouvelle matrice A
Adual.append([])
Adual[1] = sp.Matrix(3, 7, [0] * 21)
for _i in range(len(soldual_real[0]['OuB'])):
    Adual[1][:, soldual_real[0]['OuB'][_i]-1] = soldual_real[0]['BinvN'][:, _i]

for _i in range(len(soldual_real[0]['InB'])):
    Adual[1][:, soldual_real[0]['InB'][_i]-1] = sp.eye(len(soldual_real[0]['InB']))[:, _i]

soldual_real[0]['dT'] # faire entrer 7 et sortit ???
soldual.append(base_is_optimale(_A=Adual[1], _b=bdual, _cT=cTdual, _InB=[2, 4, 7]))


# choix des nouvelles variables en base
# à partir du choix du pivot: dTN

