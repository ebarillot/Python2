# coding=utf-8

# exemple tiré de la doc https://docs.scipy.org/doc/scipy/reference/optimize.linprog-simplex.html
from __future__ import print_function
from scipy.optimize import linprog
from scipy import linspace


#  sous forme canonique
#
# maximiser f = a x1 + x2
#
#   x1 + 2*x2 <= 4
# 4*x1 + 2*x2 <= 12
#  -x1 +   x2 <= 1
#
def solv_simplex(a):
    c = [a, 1.]
    c = map(lambda x: x*(-1.), c)  # opposé car recherche du max(f)
    A = [[1., 2.], [4., 2.], [-1., 1.]]
    b = [4., 12., 1.]
    _res = linprog(c=c, A_ub=A, b_ub=b)
    # print(res.keys())
    _res['fun'] *=(-1.)  # car recherche du max(f)
    return _res


print('---- 1')
for a in linspace(-3,+3,100,True):
    res=solv_simplex(a)
    print('a: {:+3.3f},  fun: {:3.3f},  x: {}'.format(a, res['fun'], res['x']))




#  sous forme canonique
#
# maximiser f = a x1 + x2
#
#   x1 + 2*x2 <= 4
# 2*x1 +   x2 <= 6
#  -x1 +   x2 <= 1
#
def solv_simplex_2(a):
    c = [a, 1.]
    c = map(lambda x: x*(-1.), c)  # opposé car recherche du max(f)
    A = [[1., 2.], [2., 1.], [-1., 1.]]
    b = [4., 6., 1.]
    _res = linprog(c=c, A_ub=A, b_ub=b)
    # print(res.keys())
    _res['fun'] *=(-1.)  # car recherche du max(f)
    return _res


print('---- 2')
for a in linspace(-3,+3,100,True):
    res=solv_simplex_2(a)
    print('a: {:+3.3f},  fun: {:3.3f},  x: {}'.format(a, res['fun'], res['x']))


#  sous forme canonique
#
# maximiser f = a x1 + x2
#   x1 + 2*x2 <= 4    (1)
# 4*x1 + 2*x2 <= 12   (2)
#  -x1 +   x2 <= 1    (3)
#
#   x1 + 2*x2 <= 4    (1)
# 2*x1 +   x2 <= 6    (2)
#  -x1 +   x2 <= 1    (3)
#
def solv_simplex_2(a):
    c = [a, 1.]
    c = map(lambda x: x*(-1.), c)  # opposé car recherche du max(f)
    A = [[1., 2.], [2., 1.], [-1., 1.]]
    b = [4., 6., 1.]
    _res = linprog(c=c, A_ub=A, b_ub=b)
    # print(res.keys())
    _res['fun'] *=(-1.)  # car recherche du max(f)
    return _res


print('---- 3')
for a in linspace(-3,+3,100,True):
    res=solv_simplex_2(a)
    print('a: {:+3.3f},  fun: {:3.3f},  x: {}'.format(a, res['fun'], res['x']))

