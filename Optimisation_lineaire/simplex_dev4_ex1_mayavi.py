# coding=utf-8


import numpy as np
from mayavi import mlab
from scipy.optimize import fmin
import math


def f(x, y):
    return x*x*x*x + y*y*y*y -2*(x-y)*(x-y)


# calcul et affichage de f()
xf, yf = np.mgrid[-3.:3.05:0.05, -3.:3.05:0.05]
zf = f(xf, yf)
sf = mlab.surf(xf, yf, zf, colormap='copper')
# sf = mlab.surf(xf, yf, zf, warp_scale="auto", colormap='copper')  # voir à quoi sert warp_scale="auto"

print(xf.min(), xf.max())
print(yf.min(), yf.max())
print(zf.min(), zf.max())


#  calcul du minimum à partir de la fonction transformée pour accepter un tableau en entrée
# x -> x[0]
# y -> x[1]
def ftab(x):
    return x[0]*x[0]*x[0]*x[0] + x[1]*x[1]*x[1]*x[1] -2*(x[0]-x[1])*(x[0]-x[1])


print(fmin(ftab,np.array([1,0])))
print(fmin(ftab,np.array([0,1])))


# Affichage 3D
eng = mlab.get_engine()
fig = mlab.gcf(engine=eng)
mlab.axes(figure=fig,
          color=(.7, .7, .7),
          xlabel='', ylabel='',
          zlabel='$f(x,y)$',
          x_axis_visibility=True, y_axis_visibility=True, z_axis_visibility=True)
# fig_extent = (-7, 7, -5, 5, -10, 10)
# extent = fig_extent,
# ranges = (-7, 7, -5, 5, -5, 5),
# mlab.scalarbar()
# mlab.orientation_axes(figure=fig)



# from mayavi.filters.cut_plane import CutPlane
# warp_scalar = eng.scenes[0].children[0].children[0]
# warp_scalar.children[1:2] = []
# cut_plane1 = CutPlane()
# eng.add_filter(cut_plane1, warp_scalar)

# calcul et affichage des plans
Rmax = 100.
drplane, dphi = Rmax / 250.0, np.pi / 250.0
[rplane, phi] = np.mgrid[0:Rmax:drplane, 0:2.*np.pi+dphi*1.5:dphi]
xplane = rplane * np.cos(phi)
yplane = rplane * np.sin(phi)
z0plane = 0.* xplane * yplane

sz = mlab.mesh(xplane, yplane, z0plane, colormap='black-white', opacity=1.0)
sy = mlab.mesh(xplane, z0plane, yplane, colormap='black-white', opacity=0.9)
sx = mlab.mesh(z0plane, xplane, yplane, colormap='black-white', opacity=0.9)

mlab.outline(figure=fig, extent=(-Rmax, Rmax, -Rmax, Rmax, -Rmax, Rmax))

mlab.show()


