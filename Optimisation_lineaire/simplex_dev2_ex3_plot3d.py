# coding=utf-8
'''
======================
3D surface (color map)
======================

Demonstrates plotting a 3D surface colored with the coolwarm color map.
The surface is made opaque by using antialiased=False.

Also demonstrates using the LinearLocator and custom formatting for the
z axis tick labels.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
y1 = np.arange(-5, 10, 0.25)
y2 = np.arange(-5, 10, 0.25)
y1, y2 = np.meshgrid(y1, y2)
Z1 = y1 + y2 + 2
Z2 = 2 * y1 - y2 + 4
Z3 = y1 - y2 + 1

Z4 = np.minimum(np.minimum(Z1,Z2),Z3)

# Plot the surface.
# surf1 = ax.plot_surface(X, Y, Z1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# surf2 = ax.plot_surface(X, Y, Z2, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# surf3 = ax.plot_surface(X, Y, Z3, cmap=cm.coolwarm, linewidth=0, antialiased=False)

surf4 = ax.plot_surface(y1, y2, Z4, cmap=cm.coolwarm, linewidth=0, antialiased=False)

# ax.plot_trisurf(X, Y, Z1, linewidth=0.2, antialiased=True)

# Customize the z axis.
# ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf4, shrink=0.5, aspect=5)

plt.show()
