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
# Sous forme canonique:
#
#    y1 + y2 - y3            <=  1
#   -y1 - y2 - y3            <= -1
#
#  2 y1 - y2      - y4       <= -1
# -2 y1 + y2      - y4       <=  1
#
#    y1 - y2           - y5  <=  2
#   -y1 + y2           - y5  <= -2
#

####################################################################
# calcul solution numérique
# if True:
if False:
    # attention, linprog cherche à minimiser et non pas à maximiser: c'est bien ce qu'on veut pour ce pb
    c = [0, 0, 1, 1, 1]
    A = [[  1,   1, -1,  0,  0],
         [ -1,  -1, -1,  0,  0],
         [  2,  -1,  0, -1,  0],
         [ -2,   1,  0, -1,  0],
         [  1,  -1,  0,  0, -1],
         [ -1,   1,  0,  0, -1]]
    b = [ 1,
         -1,
         -1,
          1,
          2,
         -2]
    solution_numerique(A, b, c, simplex_callback_print)

####################################################################
# solution symbolique
M = sp.Matrix([[  1,   1, -1,  0,  0],
               [ -1,  -1, -1,  0,  0],
               [  2,  -1,  0, -1,  0],
               [ -2,   1,  0, -1,  0],
               [  1,  -1,  0,  0, -1],
               [ -1,   1,  0,  0, -1]])
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

# matrice de départ complète
Atab = M.row_join(sp.eye(M.shape[0]))
pvar('V.transpose().col_join(Atab)')
#
b = sp.Matrix(M.shape[0], 1, [1, -1, -1, 1, 2, -2])
pvar('b')

# fonction à maximiser = -fonction à minimiser
cT = sp.Matrix(1, nvars, [-x for x in [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]])
assert (cT.shape[1] == nvars)
g = cT.dot(V)
pvar('g')


# recherche d'une solution initiale réalisable
# par la méthode du cours
step = 0
print('\n**** INIT STEP {} ****\n'.format(step))
# matrice de départ complète
Ainit = M.row_join(sp.eye(M.shape[0])).row_join(sp.Matrix(M.shape[0], 1, [-1]*M.shape[0]))
#
# liste des variables pour le probleme d'initialisation
vars_list_name_init = ['x{}'.format(i) for i in range(nvars+1)] + ['b00']
vars_list_init = sp.symbols(vars_list_name_init)
Vinit = sp.Matrix(nvars+2, 1, vars_list_init)
pvar("Vinit[:nvars+1, :].transpose().col_join(Ainit)".format(step))

binit = sp.Matrix(M.shape[0], 1, b)
pvar('binit')

# fonction à maximiser
cTinit = sp.Matrix(1, nvars+1, [0]*nvars+[-1])
pvar('Vinit[:nvars+1, :].transpose().col_join(cTinit)')

pvar("Vinit.transpose().col_join(Ainit.row_join(binit))".format(step))
# [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, b00],
# [ 1,  1, -1,  0,  0,  1,  0,  0,  0,  0,   0,  -1,   1],
# [-1, -1, -1,  0,  0,  0,  1,  0,  0,  0,   0,  -1,  -1],
# [ 2, -1,  0, -1,  0,  0,  0,  1,  0,  0,   0,  -1,  -1],
# [-2,  1,  0, -1,  0,  0,  0,  0,  1,  0,   0,  -1,   1],
# [ 1, -1,  0,  0, -1,  0,  0,  0,  0,  1,   0,  -1,   2],
# [-1,  1,  0,  0, -1,  0,  0,  0,  0,  0,   1,  -1,  -2]])
# => [1, -1, -1, 1, 2, -2]
# Le plus négatif des b est -2, en position 6 dans b
# donc correspond à x10 (col 11) dans Ainit

#  variables en base pour commencer sont donc:
solinit = list()
solinit.append(simplex_step(_A=Ainit, _b=binit, _cT=cTinit, _InB=[i-1 for i in [ 6, 7, 8, 9, 10, 12 ]]))
pvar("Vinit.transpose().col_join(solinit[{}]['tableau'])".format(step))
pvar("sp.latex(Vinit.transpose().col_join(solinit[{}]['tableau']), mode='equation*')".format(step))
# [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, b00],
# [ 2,  0, -1,  0,  1,  1,  0,  0,  0,  0,  -1,   0,   3],
# [ 0, -2, -1,  0,  1,  0,  1,  0,  0,  0,  -1,   0,   1],
# [ 3, -2,  0, -1,  1,  0,  0,  1,  0,  0,  -1,   0,   1],
# [-1,  0,  0, -1,  1,  0,  0,  0,  1,  0,  -1,   0,   3],
# [ 2, -2,  0,  0,  0,  0,  0,  0,  0,  1,  -1,   0,   4],
# [ 1, -1,  0,  0,  1,  0,  0,  0,  0,  0,  -1,   1,   2],
# [ 1, -1,  0,  0,  1,  0,  0,  0,  0,  0,  -1,   0,   2]])
# au vu du tableau, le pivot est (3, 1), coeff 1/3, on peut faire entrer x0(col1) en base et faire sortir x7(col8)
step = 1
print('\n**** INIT STEP {} ****\n'.format(step))
# la nouvelle matrice A est égale à BinvA de l'étape précédente
solinit.append([])
solinit[step] = simplex_step(_A=solinit[step - 1]['BinvA'],
                             _b=solinit[step - 1]['Binvb'],
                             _cT=solinit[step - 1]['cT'],
                             _InB=[i - 1 for i in [ 1, 6, 7, 9, 10, 12 ]])
pvar("Vinit.transpose().col_join(solinit[{}]['tableau'])".format(step))
pvar("sp.latex(Vinit.transpose().col_join(solinit[{}]['tableau']), mode='equation*')".format(step))
# [x0,   x1, x2,   x3,   x4, x5, x6,   x7, x8, x9,  x10, x11,  b00],
# [ 1, -2/3,  0, -1/3,  1/3,  0,  0,  1/3,  0,  0, -1/3,   0,  1/3],
# [ 0,  4/3, -1,  2/3,  1/3,  1,  0, -2/3,  0,  0, -1/3,   0,  7/3],
# [ 0,   -2, -1,    0,    1,  0,  1,    0,  0,  0,   -1,   0,    1],
# [ 0, -2/3,  0, -4/3,  4/3,  0,  0,  1/3,  1,  0, -4/3,   0, 10/3],
# [ 0, -2/3,  0,  2/3, -2/3,  0,  0, -2/3,  0,  1, -1/3,   0, 10/3],
# [ 0, -1/3,  0,  1/3,  2/3,  0,  0, -1/3,  0,  0, -2/3,   1,  5/3],
# [ 0, -1/3,  0,  1/3,  2/3,  0,  0, -1/3,  0,  0, -2/3,   0,  5/3]])
# au vu du tableau, le pivot est (2, 4), coeff 7/2 le plus petit, on peut faire entrer x3(col4)
# en base et faire sortir x5(col6)
step = 2
print('\n**** INIT STEP {} ****\n'.format(step))
# la nouvelle matrice A est égale à BinvA de l'étape précédente
solinit.append([])
solinit[step] = simplex_step(_A=solinit[step - 1]['BinvA'],
                             _b=solinit[step - 1]['Binvb'],
                             _cT=solinit[step - 1]['cT'],
                             _InB=[i - 1 for i in [ 1, 4, 7, 9, 10, 12 ]])
pvar("Vinit.transpose().col_join(solinit[{}]['tableau'])".format(step))
pvar("sp.latex(Vinit.transpose().col_join(solinit[{}]['tableau']), mode='equation*')".format(step))
# [x0, x1,   x2, x3,  x4,   x5, x6, x7, x8, x9,  x10, x11, b00],
# [ 1,  0, -1/2,  0, 1/2,  1/2,  0,  0,  0,  0, -1/2,   0, 3/2],
# [ 0,  2, -3/2,  1, 1/2,  3/2,  0, -1,  0,  0, -1/2,   0, 7/2],
# [ 0, -2,   -1,  0,   1,    0,  1,  0,  0,  0,   -1,   0,   1],
# [ 0,  2,   -2,  0,   2,    2,  0, -1,  1,  0,   -2,   0,   8],
# [ 0, -2,    1,  0,  -1,   -1,  0,  0,  0,  1,    0,   0,   1],
# [ 0, -1,  1/2,  0, 1/2, -1/2,  0,  0,  0,  0, -1/2,   1, 1/2],
# [ 0, -1,  1/2,  0, 1/2, -1/2,  0,  0,  0,  0, -1/2,   0, 1/2]])
# au vu du tableau, le pivot est (6, 3), on peut faire entrer x2(col 3) en base et faire sortir x9(col 10)
step = 3
print('\n**** INIT STEP {} ****\n'.format(step))
# la nouvelle matrice A est égale à BinvA de l'étape précédente
solinit.append([])
solinit[step] = simplex_step(_A=solinit[step - 1]['BinvA'],
                             _b=solinit[step - 1]['Binvb'],
                             _cT=solinit[step - 1]['cT'],
                             _InB=[i - 1 for i in [ 1, 3, 4, 7, 9, 12 ]])
pvar("Vinit.transpose().col_join(solinit[{}]['tableau'])".format(step))
pvar("sp.latex(Vinit.transpose().col_join(solinit[{}]['tableau']), mode='equation*')".format(step))
# [x0, x1, x2, x3, x4, x5, x6, x7, x8,   x9,  x10, x11, b00],
# [ 1, -1,  0,  0,  0,  0,  0,  0,  0,  1/2, -1/2,   0,   2],
# [ 0, -2,  1,  0, -1, -1,  0,  0,  0,    1,    0,   0,   1],
# [ 0, -1,  0,  1, -1,  0,  0, -1,  0,  3/2, -1/2,   0,   5],
# [ 0, -4,  0,  0,  0, -1,  1,  0,  0,    1,   -1,   0,   2],
# [ 0, -2,  0,  0,  0,  0,  0, -1,  1,    2,   -2,   0,  10],
# [ 0,  0,  0,  0,  1,  0,  0,  0,  0, -1/2, -1/2,   1,   0],
# [ 0,  0,  0,  0,  1,  0,  0,  0,  0, -1/2, -1/2,   0,   0]])
# au vu du tableau, le pivot est (6, 5), on peut faire entrer x4(col 5) en base et faire sortir x11(col 12)
step = 4
print('\n**** INIT STEP {} ****\n'.format(step))
# la nouvelle matrice A est égale à BinvA de l'étape précédente
solinit.append([])
solinit[step] = simplex_step(_A=solinit[step - 1]['BinvA'],
                             _b=solinit[step - 1]['Binvb'],
                             _cT=solinit[step - 1]['cT'],
                             _InB=[i - 1 for i in [ 1, 3, 4, 5, 7, 9 ]])
pvar("Vinit.transpose().col_join(solinit[{}]['tableau'])".format(step))
pvar("sp.latex(Vinit.transpose().col_join(solinit[{}]['tableau']), mode='equation*')".format(step))
# [x0, x1, x2, x3, x4, x5, x6, x7, x8,   x9,  x10, x11, b00],
# [ 1, -1,  0,  0,  0,  0,  0,  0,  0,  1/2, -1/2,   0,   2],
# [ 0, -2,  1,  0,  0, -1,  0,  0,  0,  1/2, -1/2,   1,   1],
# [ 0, -1,  0,  1,  0,  0,  0, -1,  0,    1,   -1,   1,   5],
# [ 0,  0,  0,  0,  1,  0,  0,  0,  0, -1/2, -1/2,   1,   0],
# [ 0, -4,  0,  0,  0, -1,  1,  0,  0,    1,   -1,   0,   2],
# [ 0, -2,  0,  0,  0,  0,  0, -1,  1,    2,   -2,   0,  10],
# [ 0,  0,  0,  0,  0,  0,  0,  0,  0,    0,    0,  -1,   0]])
pvar("Vinit[:nvars+1, :].row_join(solinit[{}]['xsol']).transpose()".format(step))
# la solution réalisable trouvée
# [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11],
# [ 2,  0,  1,  5,  0,  0,  2,  0, 10,  0,   0,   0]])
pvar("solinit[{}]['InB']".format(step))
# La base
# [0, 2, 3, 4, 6, 8] => à reporter dans la base initiale
# phase 2 du simplex


step = 0
sol_real = list()
print('\n**** PHASE 2 STEP {} ****\n'.format(step))
pvar('V.transpose().col_join(Atab)')
pvar("sp.latex(V.transpose().col_join(Atab), mode='equation*')")
# [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10],
# [ 1,  1, -1,  0,  0,  1,  0,  0,  0,  0,   0],
# [-1, -1, -1,  0,  0,  0,  1,  0,  0,  0,   0],
# [ 2, -1,  0, -1,  0,  0,  0,  1,  0,  0,   0],
# [-2,  1,  0, -1,  0,  0,  0,  0,  1,  0,   0],
# [ 1, -1,  0,  0, -1,  0,  0,  0,  0,  1,   0],
# [-1,  1,  0,  0, -1,  0,  0,  0,  0,  0,   1]])
# au vu du tableau, on peut faire entrer 2 en base et faire sortir 3
sol_real.append([])
sol_real[step] = simplex_step(_A=Atab,
                              _b=b,
                              _cT=cT,
                              _InB=[0, 2, 3, 4, 6, 8])  # indices 0 based
pvar("Vtab.transpose().col_join(sol_real[{}]['tableau'])".format(step))
pvar("sp.latex(Vtab.transpose().col_join(sol_real[{}]['tableau']), mode='equation*')".format(step))
# [x0, x1, x2, x3, x4, x5, x6, x7, x8,   x9,  x10, b00],
# [ 1, -1,  0,  0,  0,  0,  0,  0,  0,  1/2, -1/2,   2],
# [ 0, -2,  1,  0,  0, -1,  0,  0,  0,  1/2, -1/2,   1],
# [ 0, -1,  0,  1,  0,  0,  0, -1,  0,    1,   -1,   5],
# [ 0,  0,  0,  0,  1,  0,  0,  0,  0, -1/2, -1/2,   0],
# [ 0, -4,  0,  0,  0, -1,  1,  0,  0,    1,   -1,   2],
# [ 0, -2,  0,  0,  0,  0,  0, -1,  1,    2,   -2,  10],
# [ 0, -3,  0,  0,  0, -1,  0, -1,  0,    1,   -2,   6]])
pvar("sol_real[{}]['xsol'].transpose()".format(step))
#
# au vu du tableau, le pivot est (lig 2, col 10)
# on peut faire entrer x9 en base et faire sortir x2
step = 1
sol_real.append([])
sol_real[step] = simplex_step(_A=sol_real[step - 1]['BinvA'],
                             _b=sol_real[step - 1]['Binvb'],
                             _cT=sol_real[step - 1]['cT'],
                             _InB=[0, 3, 4, 6, 8, 9])  # indices 0 based
pvar("Vtab.transpose().col_join(sol_real[{}]['tableau'])".format(step))
pvar("sp.latex(Vtab.transpose().col_join(sol_real[{}]['tableau']), mode='equation*')".format(step))
# [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, b00],
# [ 1,  1, -1,  0,  0,  1,  0,  0,  0,  0,   0,   1],
# [ 0,  3, -2,  1,  0,  2,  0, -1,  0,  0,   0,   3],
# [ 0, -2,  1,  0,  1, -1,  0,  0,  0,  0,  -1,   1],
# [ 0,  0, -2,  0,  0,  1,  1,  0,  0,  0,   0,   0],
# [ 0,  6, -4,  0,  0,  4,  0, -1,  1,  0,   0,   6],
# [ 0, -4,  2,  0,  0, -2,  0,  0,  0,  1,  -1,   2],
# [ 0,  1, -2,  0,  0,  1,  0, -1,  0,  0,  -1,   4]])
# au vu du tableau, le pivot est (lig 1, col 2)
# on peut faire entrer x1 en base et faire sortir x0
step = 2
sol_real.append([])
sol_real[step] = simplex_step(_A=sol_real[step - 1]['BinvA'],
                             _b=sol_real[step - 1]['Binvb'],
                             _cT=sol_real[step - 1]['cT'],
                             _InB=[1, 3, 4, 6, 8, 9])  # indices 0 based
pvar("Vtab.transpose().col_join(sol_real[{}]['tableau'])".format(step))
pvar("sp.latex(Vtab.transpose().col_join(sol_real[{}]['tableau']), mode='equation*')".format(step))
# [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, b00],
# [ 1,  1, -1,  0,  0,  1,  0,  0,  0,  0,   0,   1],
# [-3,  0,  1,  1,  0, -1,  0, -1,  0,  0,   0,   0],
# [ 2,  0, -1,  0,  1,  1,  0,  0,  0,  0,  -1,   3],
# [ 0,  0, -2,  0,  0,  1,  1,  0,  0,  0,   0,   0],
# [-6,  0,  2,  0,  0, -2,  0, -1,  1,  0,   0,   0],
# [ 4,  0, -2,  0,  0,  2,  0,  0,  0,  1,  -1,   6],
# [-1,  0, -1,  0,  0,  0,  0, -1,  0,  0,  -1,   3]])
# Tous les coeff dT sont <= 0
pvar("[i+1 for i in sol_real[{}]['InB']]".format(step))
# [i+1 for i in sol_real[1]['InB']] : [2, 4, 5, 7, 9, 10] => 1 based
pvar("sol_real[{}]['xsol'].transpose()".format(step))
# sol_real[2]['xsol'].transpose() : Matrix([[0, 1, 0, 0, 3, 0, 0, 0, 0, 6, 0]])
