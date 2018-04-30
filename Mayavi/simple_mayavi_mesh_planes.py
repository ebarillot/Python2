# coding=utf-8

#  plan z=0
from numpy import pi, sin, cos, mgrid
Rmax = 1
dr, dphi = Rmax/250.0, pi/250.0
[r, phi] = mgrid[0:Rmax:dr, 0:2*pi+dphi*1.5:dphi]
x = r * cos(phi)
y = r * sin(phi)
z0 = 0.* x * y


# View it.
from mayavi import mlab
sz = mlab.mesh(x, y, z0, colormap='copper', opacity=1.0)
sy = mlab.mesh(x, z0, y, colormap='copper', opacity=0.8)
sx = mlab.mesh(z0, x, y, colormap='copper', opacity=0.8)
mlab.outline(extent=(-Rmax, Rmax, -Rmax, Rmax, -Rmax, Rmax))
mlab.axes()
mlab.show()

