# coding=utf-8

#  sphere ou allipsoide
from numpy import pi, sin, cos, mgrid
dphi, dtheta = pi/250.0, pi/250.0
[phi, theta] = mgrid[0:pi+dphi*1.5:dphi, 0:2*pi+dtheta*1.5:dtheta]
rx = 1
ry = 1
rz = 2
x = rx * cos(phi) * cos(theta)
y = ry * sin(phi) * cos(theta)
z = rz * sin(theta)

# View it.
from mayavi import mlab
s = mlab.mesh(x, y, z, colormap='copper')
mlab.outline()
mlab.axes()
mlab.show()

