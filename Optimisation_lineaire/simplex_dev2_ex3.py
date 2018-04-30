# coding=utf-8

import numpy as np

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
Xm, Ym = np.meshgrid(X, Y)  # construit un maiilage 2D : produit cartésien de 2 tableaux 1D
Z1 = Xm + Ym + 2
Z2 = 2*Xm - Ym + 4
Z3 = Xm - Ym + 1

# print(X)
# print(Y)
# print(Xm)
# print(Ym)
# print(Z1.any)
Z1.min()
Z2.min()
Z3.min()


Zmax = None
y1arg = None
y2arg = None
for y1 in np.arange(0, 100, 0.1):
    for y2 in np.arange(0, 100, 0.1):
        Z1 = y1 + y2 + 2
        Z2 = 2 * y1 - y2 + 4
        Z3 = y1 - y2 + 1
        ZZ = min(Z1, Z2, Z3)
        if Zmax is None:
            Zmax = ZZ
        else:
            if Zmax <= ZZ:
                y1arg = y1
                y2arg = y2
                Zmax = ZZ

print(y1arg, y2arg, Zmax)
