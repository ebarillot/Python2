# coding=utf-8

# exemple tiré de la doc https://docs.scipy.org/doc/scipy/reference/optimize.linprog-simplex.html
from scipy.optimize import linprog
from scipy import linspace


# maximiser f = 1.02 x1 + 1.04 x2 + 1.05 x3
# x1 + 2*x2 +x3 <= 20000
# x3 <= 3000
#
def solv_simplex(a):
    c = [a, 1.]
    c = map(lambda x:x*(-1.), c)  # car recherche du max(f)
    A = [[1, 2], [4, 2], [-1, 1]]
    b = [4., 12., 1.]
    _res = linprog(c=c, A_ub=A, b_ub=b)
    # print(res.keys())
    _res['fun'] *=(-1.)  # car recherche du max(f)
    return _res


for a in linspace(-4,+4,350,True):
    res=solv_simplex(a)
    print('a: {:3.3f},  fun: {:3.3f},  x: {}'.format(a, res['fun'], res['x']))
