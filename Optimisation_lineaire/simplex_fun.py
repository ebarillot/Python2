# coding=utf-8
from __future__ import print_function
import sympy as sp
from typing import List, Dict
import sys


# fontion qui marche même si l'objet à afficher est dans un autre module
def pvar(expression):
    frame = sys._getframe(1)
    print(expression, ':', repr(eval(expression, frame.f_globals, frame.f_locals)))


# fontion qui marche si l'objet à afficher est dans ce module
def pvar2(var):
    print('{}: {}'.format(var, repr(eval(var))))


def simplex_step(_A, _b, _cT, _InB):
    # type: (sp.Matrix, sp.Matrix, sp.Matrix, List) -> Dict
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
        _sol['real'] = False
    else:
        _Binv = _B.inv()
        assert (_Binv * _B == sp.eye(_nInB))
        _Binv_A = _Binv * _A
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
        _sol['BinvA'] = _Binv_A
        _sol['BinvN'] = _Binv_N
        _sol['fun'] = _fun
        _sol['tableau'] = (_Binv_A.col_join(_dT)).row_join(_Binv_b.col_join(-_fun))
        _sol['real'] = all([_x >= 0 for _x in _xsol[:, 0]])
        _sol['ret'] = 'OK'
    return _sol


def solution_numerique(_M, _b, _c, callback=None):
    # solution numérique du problème
    from scipy.optimize import linprog
    return linprog(c=_c, A_ub=_M, b_ub=_b, bounds=(0, None), options={'disp': True}, callback=callback)


def simplex_callback_print(xk, **kwargs):
    print('--> Phase {}, it {}:'.format(kwargs['phase'], kwargs['nit']))
    print('xk: {}'.format(xk))
    for k in set(kwargs.keys())-{'phase', 'nit', 'tableau'}:
        print('{}: {}'.format(k, kwargs[k]))
    print('tableau:\n {}'.format(kwargs['tableau']))


if __name__ == "__main__":
    c = [-3, -2, -1]  # attention, linprog cherche à minimiser et non pas à maximiser
    A = [[1, -1, 1],
         [2, 1, 3],
         [-1, 0, 1],
         [1, 1, 1]]
    b = [4, 6, 3, 8]
    solution_numerique(A, b, c, simplex_callback_print)
