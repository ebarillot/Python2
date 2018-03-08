# coding=utf-8

'''
Exemple d'affichage d'une surface en 3D

ATTENTION mayavi 4.5.0 est buggée:
mlab.axes() provoque une erreur du type: AttributeError: 'PolyDataNormals' object has no attribute 'bounds'

Voir: https://github.com/enthought/mayavi/issues/474

Corriger (en mode administrateur) les fichiers suivants:
C:\ProgramData\Anaconda2\envs\python_mayavi\Lib\site-packages\mayavi\tools\decorations.py
Corriger la fonction suivante:
    def _extent_changed(self):
        """ Code to modify the extents for
        """
        axes = self._target
        axes.axes.use_data_bounds = False
        axes.axes.bounds = self.extent
        if self.ranges is None:
            src = axes.module_manager.source
            data = src.outputs[0] if not hasattr(src.outputs[0], 'output') else src.outputs[0].output
            axes.axes.ranges = data.bounds
#            axes.axes.ranges = \
#                axes.module_manager.source.outputs[0].bounds


C:\ProgramData\Anaconda2\envs\python_mayavi\Lib\site-packages\mayavi\modules\axes.py

    def update_pipeline(self):
        """Override this method so that it *updates* the tvtk pipeline
        when data upstream is known to have changed.

        This method is invoked (automatically) when any of the inputs
        sends a `pipeline_changed` event.
        """
        mm = self.module_manager
        if mm is None or not self.axes.use_data_bounds:
            self.configure_input_data(self.axes, None)
            return
        src = mm.source
#        self.configure_input_data(self.axes, src.outputs[0])
        data = src.outputs[0] if not hasattr(src.outputs[0], 'output') else src.outputs[0].output
        self.configure_input_data(self.axes, data)
        self.pipeline_changed = True

'''


from numpy import pi, sin, cos, mgrid
dphi, dtheta = pi/250.0, pi/250.0
[phi,theta] = mgrid[0:pi+dphi*1.5:dphi,0:2*pi+dtheta*1.5:dtheta]
m0 = 4; m1 = 3; m2 = 2; m3 = 3; m4 = 6; m5 = 2; m6 = 6; m7 = 4;
r = sin(m0*phi)**m1 + cos(m2*phi)**m3 + sin(m4*theta)**m5 + cos(m6*theta)**m7
x = r*sin(phi)*cos(theta)
y = r*cos(phi)
z = r*sin(phi)*sin(theta)

# View it.
from mayavi import mlab
s = mlab.mesh(x, y, z)
mlab.outline()
mlab.axes()
mlab.show()

