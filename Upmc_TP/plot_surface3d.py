# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 14:36:39 2016

@author: emmanuel
"""

from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt


# imports specific to the plots in this example
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import get_test_data

# Twice as wide as it is tall.
fig = plt.figure(figsize=plt.figaspect(0.5))

#---- First subplot
ax = fig.add_subplot(1, 2, 1, projection='3d')
d = np.arange(1, 4, 0.25)
q = np.arange(3, 6, 0.25)
d, q = np.meshgrid(d, q)
Z = np.power(q,d)-2*d*(q-1)
surf = ax.plot_surface(d, q, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
#ax.set_zlim3d(-1.01, 1.01)

fig.colorbar(surf, shrink=0.5, aspect=10)

#---- Second subplot
#ax = fig.add_subplot(1, 2, 2, projection='3d')
#Z = np.power(q,d)-2*d*(q-1)
#ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)


plt.show()
