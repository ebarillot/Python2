# coding=utf-8


"""Test surf on regularly spaced co-ordinates like MayaVi."""

import numpy as np
from mayavi import mlab


def f(x, y):
    sin, cos = np.sin, np.cos
    return sin(x + y) + sin(2 * x - y) + cos(3 * x + 4 * y)


x, y = np.mgrid[-7.:7.05:0.1, -5.:5.05:0.05]
s = mlab.surf(x, y, f)
mlab.outline()
mlab.axes()
mlab.show()
