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
vars_list_name = ['x{}'.format(i) for i in range(nvars)]
vars_list = sp.symbols(vars_list_name)
V = sp.Matrix(nvars, 1, vars_list)
pvar('V')

b = sp.Matrix(M.shape[0], 1, [1, -1, -1, 1, 2, -2])
pvar('b')

# fonction à maximiser = -f à minimiser
cT = sp.Matrix(1, nvars, [-x for x in [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]])
assert (cT.shape[1] == nvars)
g = cT.dot(V)
pvar('g')

# recherche 1ere solution realisable
xBbase = sp.Matrix(M.shape[1], 1, [0, 0, 1, 1, 2])
pvar('xBbase')
# verification que la solution est réalisable
# pour voir si la solution candidate est réalisable
all([x <= 0 for x in list(M * xBbase - b)])
#  pour en tester d'autres
# all([x <= 0 for x in list(M * sp.Matrix(M.shape[1], 1, [0, 0, 1, 1, 2]) - b)])


step = 0
print('\n**** PROBLÈME STEP {} ****\n'.format(step))
sol = list()
# matrice de départ complète
A = M.row_join(sp.eye(M.shape[0]))
pvar('A')
#  il y a M.shape[0] variables en base, ici c'est 6
#  on essaie avec les colonnes de la 1ere solution réalisable trouvée
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  6,  7,  8]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  6,  7,  9]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  6,  7, 10]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  6,  7, 11]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  6,  8,  9]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  6,  8, 10]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  6,  8, 11]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  6,  9, 10]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  6,  9, 11]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  6, 10, 11]]))

sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  7,  8,  9]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  7,  8, 10]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  7,  8, 11]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  7,  9, 10]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  7,  9, 11]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  7, 10, 11]]))

sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  8,  9, 10]]))
sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  8,  9, 11]]))

sol.append(simplex_step(_A=A, _b=b, _cT=cT, _InB=[i-1 for i in [ 3,  4,  5,  9, 10, 11]]))

# pour afficher toutes les données de toutes les bases testées
for _i in range(len(sol)):
    print('-------------')
    print('solution: {}'.format(_i + 1))
    for _k in sol[_i].keys():
        print('{}: {}'.format(_k, sol[_i][_k]))

# la solution réalisable trouvée est: soldual[5]
sol_real = [_x for _x in sol if _x['real']]
len(sol_real)
for _k in sol_real[0].keys():
    print('{}: {}'.format(_k, sol_real[0][_k]))
# pour afficher le tableau de la solution réalisable trouvée:
pvar("sol_real[{}]['tableau']".format(step))
# sol_real[0]['tableau'] : Matrix([
# [ 1,  1, 1, 0, 0, 0, -1,  0, 0, 0,  0, 1],
# [-2,  1, 0, 1, 0, 0,  0, -1, 0, 0,  0, 1],
# [ 1, -1, 0, 0, 1, 0,  0,  0, 0, 0, -1, 2],
# [ 2,  2, 0, 0, 0, 1, -1,  0, 0, 0,  0, 2],
# [-4,  2, 0, 0, 0, 0,  0, -1, 1, 0,  0, 2],
# [ 2, -2, 0, 0, 0, 0,  0,  0, 0, 1, -1, 4],
# [ 0,  1, 0, 0, 0, 0, -1, -1, 0, 0, -1, 4]])
pvar("[i+1 for i in sol_real[0]['InB']]")
# => [3, 4, 5, 6, 9, 10]
pvar("soldual_real[{}]['xsol'][soldual_real[{}]['InB'], :]".format(step, step))

# au vu du tableau, on peut faire entrer 2 en base et faire sortir 3
# la base devient [2, 4, 5]
step = int(1)
print('\n**** PROBLÈME STEP {} ****\n'.format(step))
# la nouvelle matrice A est égale à BinvA de l'étape précédente
sol_real.append([])
sol_real[step] = simplex_step(_A=sol_real[step - 1]['BinvA'],
                              _b=sol_real[step - 1]['Binvb'],
                              _cT=sol_real[step - 1]['cT'],
                              _InB=[i-1 for i in [2, 4, 5, 6, 9, 10]])
# pvar("sol_real[{}]['dT']".format(step))
pvar("sol_real[{}]['tableau']".format(step))
# sol_real[1]['tableau'] : Matrix([
# [ 1, 1,  1, 0, 0, 0, -1,  0, 0, 0,  0, 1],
# [-3, 0, -1, 1, 0, 0,  1, -1, 0, 0,  0, 0],
# [ 2, 0,  1, 0, 1, 0, -1,  0, 0, 0, -1, 3],
# [ 0, 0, -2, 0, 0, 1,  1,  0, 0, 0,  0, 0],
# [-6, 0, -2, 0, 0, 0,  2, -1, 1, 0,  0, 0],
# [ 4, 0,  2, 0, 0, 0, -2,  0, 0, 1, -1, 6],
# [-1, 0, -1, 0, 0, 0,  0, -1, 0, 0, -1, 3]])
pvar("[i+1 for i in sol_real[{}]['InB']]".format(step))
# [i+1 for i in sol_real[1]['InB']] : [2, 4, 5, 6, 9, 10]
pvar("sol_real[{}]['xsol'].transpose()".format(step))
# sol_real[1]['xsol'].transpose() : Matrix([[0, 1, 0, 0, 3, 0, 0, 0, 0, 6, 0]])
pvar("sol_real[{}]['dT']".format(step))
# sol_real[1]['dT'] : Matrix([[-1, 0, -1, 0, 0, 0, 0, -1, 0, 0, -1]])
pvar("sol_real[{}]['Binv']".format(0))
# sol_real[0]['Binv'] : Matrix([
# [0, -1,  0, 0, 0,  0],
# [0,  0, -1, 0, 0,  0],
# [0,  0,  0, 0, 0, -1],
# [1, -1,  0, 0, 0,  0],
# [0,  0, -1, 1, 0,  0],
# [0,  0,  0, 0, 1, -1]])
pvar("sol_real[{}]['Binv']".format(1))
# sol_real[1]['Binv'] : Matrix([
# [ 1, 0, 0, 0, 0, 0],
# [-1, 1, 0, 0, 0, 0],
# [ 1, 0, 1, 0, 0, 0],
# [-2, 0, 0, 1, 0, 0],
# [-2, 0, 0, 0, 1, 0],
# [ 2, 0, 0, 0, 0, 1]])
print(sp.latex(sol_real[step]['tableau'], mode='equation*'))
# \begin{equation*}\left[\begin{array}{cccccccccccc}
# 1 & 1 & 1 & 0 & 0 & 0 & -1 & 0 & 0 & 0 & 0 & 1\\
# -3 & 0 & -1 & 1 & 0 & 0 & 1 & -1 & 0 & 0 & 0 & 0\\
# 2 & 0 & 1 & 0 & 1 & 0 & -1 & 0 & 0 & 0 & -1 & 3\\
# 0 & 0 & -2 & 0 & 0 & 1 & 1 & 0 & 0 & 0 & 0 & 0\\
# -6 & 0 & -2 & 0 & 0 & 0 & 2 & -1 & 1 & 0 & 0 & 0\\
# 4 & 0 & 2 & 0 & 0 & 0 & -2 & 0 & 0 & 1 & -1 & 6\\
# -1 & 0 & -1 & 0 & 0 & 0 & 0 & -1 & 0 & 0 & -1 & 3
# \end{array}\right]\end{equation*}


# recherche d'une solution initiale réalisable
step = 0
print('\n**** PROBLÈME INIT STEP {} ****\n'.format(step))
# matrice de départ complète
Ainit = M.row_join(sp.eye(M.shape[0])).row_join(sp.Matrix(M.shape[0], 1, [-1]*M.shape[0]))
pvar('Ainit')
#
binit = sp.Matrix(M.shape[0], 1, b)
pvar('binit')

# fonction à maximiser
cTinit = sp.Matrix(1, nvars+1, [0]*nvars+[-1])
pvar('cTinit')

# => [1, -1, -1, 1, 2, -2]
# Le plus négatif des b est -2, en position 6 dans b donc en 11 dans Ainit

#  variables en base pour commencer sont donc:
solinit = list()
solinit.append(simplex_step(_A=Ainit, _b=binit, _cT=cTinit, _InB=[i-1 for i in [ 6, 7, 8, 9, 10, 12 ]]))
pvar("solinit[0]['tableau']")
# [ 2,  0, -1,  0, 1, 1, 0, 0, 0, 0, -1, 0, 3],
# [ 0, -2, -1,  0, 1, 0, 1, 0, 0, 0, -1, 0, 1],
# [ 3, -2,  0, -1, 1, 0, 0, 1, 0, 0, -1, 0, 1],
# [-1,  0,  0, -1, 1, 0, 0, 0, 1, 0, -1, 0, 3],
# [ 2, -2,  0,  0, 0, 0, 0, 0, 0, 1, -1, 0, 4],
# [ 1, -1,  0,  0, 1, 0, 0, 0, 0, 0, -1, 1, 2],
# [ 1, -1,  0,  0, 1, 0, 0, 0, 0, 0, -1, 0, 2]])
# au vu du tableau, le pivot est (3, 1), on peut faire entrer 1 en base et faire sortir 8
step = 1
print('\n**** PROBLÈME INIT STEP {} ****\n'.format(step))
# la nouvelle matrice A est égale à BinvA de l'étape précédente
solinit.append([])
solinit[step] = simplex_step(_A=solinit[step - 1]['BinvA'],
                             _b=solinit[step - 1]['Binvb'],
                             _cT=solinit[step - 1]['cT'],
                             _InB=[i - 1 for i in [ 1, 6, 7, 9, 10, 12 ]])
pvar("solinit[{}]['tableau']".format(step))
# [1, -2/3,  0, -1/3,  1/3, 0, 0,  1/3, 0, 0, -1/3, 0,  1/3],
# [0,  4/3, -1,  2/3,  1/3, 1, 0, -2/3, 0, 0, -1/3, 0,  7/3],
# [0,   -2, -1,    0,    1, 0, 1,    0, 0, 0,   -1, 0,    1],
# [0, -2/3,  0, -4/3,  4/3, 0, 0,  1/3, 1, 0, -4/3, 0, 10/3],
# [0, -2/3,  0,  2/3, -2/3, 0, 0, -2/3, 0, 1, -1/3, 0, 10/3],
# [0, -1/3,  0,  1/3,  2/3, 0, 0, -1/3, 0, 0, -2/3, 1,  5/3],
# [0, -1/3,  0,  1/3,  2/3, 0, 0, -1/3, 0, 0, -2/3, 0,  5/3]])
# au vu du tableau, le pivot est (2, 4), on peut faire entrer 4 en base et faire sortir 6
step = 2
print('\n**** PROBLÈME INIT STEP {} ****\n'.format(step))
# la nouvelle matrice A est égale à BinvA de l'étape précédente
solinit.append([])
solinit[step] = simplex_step(_A=solinit[step - 1]['BinvA'],
                             _b=solinit[step - 1]['Binvb'],
                             _cT=solinit[step - 1]['cT'],
                             _InB=[i - 1 for i in [ 1, 4, 7, 9, 10, 12 ]])
pvar("solinit[{}]['tableau']".format(step))
# [1,  0, -1/2, 0, 1/2,  1/2, 0,  0, 0, 0, -1/2, 0, 3/2],
# [0,  2, -3/2, 1, 1/2,  3/2, 0, -1, 0, 0, -1/2, 0, 7/2],
# [0, -2,   -1, 0,   1,    0, 1,  0, 0, 0,   -1, 0,   1],
# [0,  2,   -2, 0,   2,    2, 0, -1, 1, 0,   -2, 0,   8],
# [0, -2,    1, 0,  -1,   -1, 0,  0, 0, 1,    0, 0,   1],
# [0, -1,  1/2, 0, 1/2, -1/2, 0,  0, 0, 0, -1/2, 1, 1/2],
# [0, -1,  1/2, 0, 1/2, -1/2, 0,  0, 0, 0, -1/2, 0, 1/2]])
# au vu du tableau, le pivot est (6, 3), on peut faire entrer 3 en base et faire sortir 12
step = 3
print('\n**** PROBLÈME INIT STEP {} ****\n'.format(step))
# la nouvelle matrice A est égale à BinvA de l'étape précédente
solinit.append([])
solinit[step] = simplex_step(_A=solinit[step - 1]['BinvA'],
                             _b=solinit[step - 1]['Binvb'],
                             _cT=solinit[step - 1]['cT'],
                             _InB=[i - 1 for i in [ 1, 3, 4, 7, 9, 10 ]])
pvar("solinit[{}]['tableau']".format(step))
# [1, -1, 0, 0,  1,  0, 0,  0, 0, 0, -1,  1,  2],
# [0, -2, 1, 0,  1, -1, 0,  0, 0, 0, -1,  2,  1],
# [0, -1, 0, 1,  2,  0, 0, -1, 0, 0, -2,  3,  5],
# [0, -4, 0, 0,  2, -1, 1,  0, 0, 0, -2,  2,  2],
# [0, -2, 0, 0,  4,  0, 0, -1, 1, 0, -4,  4, 10],
# [0,  0, 0, 0, -2,  0, 0,  0, 0, 1,  1, -2,  0],
# [0,  0, 0, 0,  0,  0, 0,  0, 0, 0,  0, -1,  0]])
pvar("solinit[{}]['InB']".format(step))
# solinit[3]['InB'] : [0, 2, 3, 6, 8, 9]
# ==> voir si on obtient la même solution qu'avant
