# coding=utf-8


import numpy as np
from mayavi import mlab
from mayavi.modules.grid_plane import GridPlane

#  pour avoir l'interface complète
mlab.options.backend = 'envisage'

# prepare some interesting function:
def f(x, y):
    return 3.0*np.sin(x*y+1e-4)/(x*y+1e-4)


x, y = np.mgrid[-7.:7.05:0.1, -5.:5.05:0.05]

# 3D visualization of f:
fig_extent = (-7, 7, -5, 5, -5, 5)
s = mlab.surf(x, y, f)
eng = mlab.get_engine()
fig = mlab.gcf(engine=eng)
mlab.outline(figure=fig)
# mlab.scalarbar()
# mlab.orientation_axes(figure=fig)


mlab.axes(figure=fig,
          color=(.7, .7, .7),
          extent=fig_extent,
          ranges=(-7, 7, -5, 5, -5, 5),
          xlabel='', ylabel='',
          zlabel='Probability',
          x_axis_visibility=False, z_axis_visibility=False)

# code récupéré gràace à la possibilité de recording des opérations faites sur la scene
grid_plane = GridPlane()
array_source = eng.scenes[0].children[0]
eng.add_filter(grid_plane, array_source)

# from mayavi.modules.scalar_cut_plane import ScalarCutPlane
# scalar_cut_plane = ScalarCutPlane()
# eng.add_filter(scalar_cut_plane, array_source)
# scene = eng.scenes[0]

from mayavi.filters.cut_plane import CutPlane
warp_scalar = eng.scenes[0].children[0].children[0]
warp_scalar.children[1:2] = []
cut_plane1 = CutPlane()
eng.add_filter(cut_plane1, warp_scalar)

module_manager = eng.scenes[0].children[0].children[0].children[0].children[0]
module_manager.scalar_lut_manager.lut_mode = 'copper'

mlab.show()
