# coding=utf-8

# exemple tiré de la doc https://docs.scipy.org/doc/scipy/reference/optimize.linprog-simplex.html
from scipy.optimize import linprog


# Romuald possède 20 000 € qu’il souhaite investir dans trois types d’actions notées A1, A2 et A3. Au
# moment de l’acquisition, l’action A1 possède un rendement de 2 % et le risque de perte est limité. L’action
# A2 possède un rendement de 4 % et le risque de perte est moyennement important. Enﬁn, l’action A3
# possède un rendement de 5 % mais le risque de perte est élevé. Par sécurité, Romuald souhaite investir au
# maximum 3 000 € dans le fond F3, et deux fois autant dans le fond F1 que dans le fond F2.
# En supposant que le rendement de chaque action sera le même à la ﬁn de l’année qu’au moment de
# l’achat, quel est le rendement maximal que Romuald peut espérer obtenir et le cas échéant, quelle sera la
# composition de son portefeuille d’actions ?
#

# maximiser f = 1.02 x1 + 1.04 x2 + 1.05 x3
# x1 + 2*x2 +x3 <= 20000
# x3 <= 3000
#
print('== Version 1')
c = [1.02, 1.04, 1.05]
c = map(lambda x:x*(-1.), c)  # car recherche du max(f)
A = [[1, 2, 1], [0, 0, 1]]
b = [20000., 3000.]
res = linprog(c=c, A_ub=A, b_ub=b)
# print(res.keys())
res['fun'] *=(-1.)  # car recherche du max(f)
print(res)


# maximiser f = 1.02 x1 + 1.04 x2 + 1.05 x3
# x1 - 2*x2 = 0
# x1 + x2 + x3 <= 20000
# x3 <= 3000
#
print('== Version 2')
c = [1.02, 1.04, 1.05]
c = map(lambda x:x*(-1.), c)  # car recherche du max(f)
A_eq = [[1, -2, 0]]
b_eq = [0]
A_ub = [[1, 1, 1], [0, 0, 1]]
b_ub = [20000., 3000.]
res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq)
# print(res.keys())
res['fun'] *=(-1.)  # car recherche du max(f)
print(res)


# maximiser f = 1.02 x1 + 1.04 x2 + 1.05 x3
#  x1 - 2*x2 <= 0
# -x1 + 2*x2 <= 0
# x1 + x2 + x3 <= 20000
# x3 <= 3000
#
print('== Version 3')
c = [1.02, 1.04, 1.05]
c = map(lambda x:x*(-1.), c)  # car recherche du max(f)
A_ub = [[1, 1, 1], [0, 0, 1], [1, -2, 0], [-1, 2, 0]]
b_ub = [20000., 3000., 0., 0.]
res = linprog(c=c, A_ub=A_ub, b_ub=b_ub)
# print(res.keys())
res['fun'] *=(-1.)  # car recherche du max(f)
print(res)


# maximiser f = 1.02 x1 + 1.04 x2 + 1.05 x3
# x1 = 2*x2
# 3 x2 + x3 <= 20000
# x3 <= 3000
#
print('== Version 4')
c = [3.08, 1.05]
c = map(lambda x:x*(-1.), c)  # car recherche du max(f)
A_ub = [[3, 1], [0, 1]]
b_ub = [20000., 3000.]
res = linprog(c=c, A_ub=A_ub, b_ub=b_ub)
# print(res.keys())
res['fun'] *=(-1.)  # car recherche du max(f)
print(res)


