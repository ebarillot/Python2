# coding=utf-8


import numpy as np
from mayavi import mlab


def f(y1, y2):
    Z1 = y1 + y2 + 2
    Z2 = 2 * y1 - y2 + 4
    Z3 = y1 - y2 + 1
    return np.minimum(np.minimum(Z1,Z2),Z3)


def Z0(y1, y2):
    return y1 * y2 * 0


x, y = np.mgrid[-7.:7.05:0.1, -5.:5.05:0.05]
s = mlab.surf(x, y, f)
s0 = mlab.surf(x, y, Z0)
# mlab.axes(extent=[-10,10,-10,10,-10,10],x_axis_visibility=True,y_axis_visibility=True,z_axis_visibility=True)
mlab.outline()
mlab.axes()
mlab.show()
