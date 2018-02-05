# coding=utf-8


import numpy as np
import matplotlib.pyplot as plt

# matplotlib inline

# parametres du modele de Lengyel-Epstein
a = 9.
b = 0.14
sig = 50.
d = 1.07


real_size_factor = 1
real_size = 70.*real_size_factor
discret_size = 100*real_size_factor  # size of the 2D grid
dx = real_size/discret_size  # space step
# T = 1.0  # total time
T = 30000.0  # total time
dt = 2. * d*dx**2/2./sig  # time step h <= (dx^2/2D) avec D~1/d (d est le plus petit coeff de diffusion)
n = int(T/dt)

print('dt={}'.format(dt))
print('n={}'.format(n))

U = np.random.rand(discret_size, discret_size)
V = np.random.rand(discret_size, discret_size)


def laplacian(u):
    u_top    = u[0:-2, 1:-1]
    u_left   = u[1:-1, 0:-2]
    u_bottom = u[2:, 1:-1]
    u_right  = u[1:-1, 2:]
    u_center = u[1:-1, 1:-1]
    return (u_top + u_left + u_bottom + u_right - 4 * u_center) / dx*dx


plt.ion()

# image initiale
plt.imshow(U, cmap=plt.copper(), extent=[-1, 1, -1, 1])
# plt.draw()
plt.show()
plt.xticks([])
plt.yticks([])
plt.pause(0.5)

# We simulate the PDE with the finite difference method.
for i in range(n):
    # We compute the Laplacian of u and v.
    deltaU = laplacian(U)
    deltaV = laplacian(V)
    # We take the values of u and v inside the grid.
    Uc = U[1:-1,1:-1]
    Vc = V[1:-1,1:-1]
    UVc = Uc*Vc / (1+Uc*Uc)
    # We update the variables.
    U[1:-1,1:-1], V[1:-1,1:-1] = \
        Uc + dt * (a - Uc - 4*UVc + deltaU) / sig, \
        Vc + dt * (b * (Uc - UVc) + d * deltaV)
    # Neumann conditions: derivatives at the edges
    # are null.
    for Z in (U, V):
        Z[0,:] = Z[1,:]
        Z[-1,:] = Z[-2,:]
        Z[:,0] = Z[:,1]
        Z[:,-1] = Z[:,-2]

    if (i%(n/50))==0:
        print('i={}, t={}'.format(i, dt*i))
        plt.imshow(U, cmap=plt.copper(), extent=[-1,1,-1,1])
        # plt.draw()
        plt.show()
        plt.pause(0.01)


plt.imshow(U, cmap=plt.copper(), extent=[-1,1,-1,1])
# plt.xticks([]); plt.yticks([])
# plt.draw()
plt.show()
plt.pause(5)
plt.savefig("lengyel_eptsein"+"{0:.0f}".format(T)+".png", dpi=96)
np.savez("lengyel_eptsein"+"{0:.0f}".format(T), U, V)
