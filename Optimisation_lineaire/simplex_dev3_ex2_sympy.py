# coding=utf-8

from __future__ import print_function
import sympy as sp
from Optimisation_lineaire.simplex_fun import pvar, simplex_step, solution_numerique, simplex_callback_print

sp.init_printing(use_unicode=True)

####################################################################
#
# min(sur y1, y2) de:
#   |   y1 + y2 - 1 |
# + | 2 y1 - y2 + 1 |
# + |   y1 - y2 - 2 |
#
# avec:
#
# |X| = min{z, z >= 0, X-z <= 0, x+z >= 0 }
#
# Equivalent à
#
# min(sur y1, y2, y3, y4, y5) de y3 + y4 + y5
#
#    y1 + y2 - 1 - y3 <= 0
#    y1 + y2 - 1 + y3 >= 0
#
#  2 y1 - y2 + 1 - y4 <= 0
#  2 y1 - y2 + 1 + y4 >= 0
#
#    y1 - y2 - 2 - y5 <= 0
#    y1 - y2 - 2 + y5 >= 0
#
# Equivalent à
#
# min(sur y1, y2, y3, y4, y5) de y3 + y4 + y5
#
#    y1 + y2 - y3            <= 1
#    y1 + y2 + y3            >= 1
#
#  2 y1 - y2      - y4       <= -1
#  2 y1 - y2      + y4       >= -1
#
#    y1 - y2           - y5  <= 2
#    y1 - y2           + y5  >= 2
#

####################################################################
# calcul solution numérique
# if True:
if False:
    c = [-x for x in [0, 0, 1, 1, 1]]   # attention, linprog cherche à minimiser et non pas à maximiser
    A = [[ 1,  1, -1,  0,  0],
         [ 1,  1,  1,  0,  0],
         [ 2, -1,  0, -1,  0],
         [ 2, -1,  0,  1,  0],
         [ 1, -1,  0,  0, -1],
         [ 1, -1,  0,  0,  1]]
    b = [1, 1, -1, -1, 2, 2]
    solution_numerique(A, b, c, simplex_callback_print)

####################################################################
# solution symbolique
M = sp.Matrix([[1, 1, -1, 0, 0],
               [1, 1, 1, 0, 0],
               [2, -1, 0, -1, 0],
               [2, -1, 0, 1, 0],
               [1, -1, 0, 0, -1],
               [1, -1, 0, 0, 1]])
pvar('M')
pvar('M.shape')
nInB = M.shape[0]
nOuB = M.shape[1]
nvars = nInB + nOuB
vars_list_name = ['x{}'.format(i) for i in range(nvars)]
vars_list = sp.symbols(vars_list_name)
V = sp.Matrix(nvars, 1, vars_list)
pvar('V')

b = sp.Matrix(M.shape[0], 1, [1, 1, -1, -1, 2, 2])
pvar('b')

# fonction à minimiser
cT = sp.Matrix(1, nvars, [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0])
assert (cT.shape[1] == nvars)
g = cT.dot(V)

#  solution realisable
xBbase = sp.Matrix(3, 1, [0, 6, 0])
pvar('xBbase')
# verification que la solution est réalisable
M.dot(xBbase)

sol = list()
# matrice de départ complète
A = M.row_join(sp.eye(M.shape[0]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[2, 4, 5, 6]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[2, 4, 5, 7]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[2, 4, 6, 7]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[2, 5, 6, 7]))

for _i in range(len(sol)):
    print('-------------')
    print('solution: {}'.format(_i + 1))
    for _k in sol[_i].keys():
        print('{}: {}'.format(_k, sol[_i][_k]))

# la solution réalisable trouvée est: soldual[5]
sol_real = [_x for _x in sol if _x['real']]

