# First Python OpenGL program
# ogl1.py


from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys


def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glutWireTeapot(0.5)
    glFlush()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(250, 250)
glutInitWindowPosition(100, 100)
glutCreateWindow("My Second OGL Program")
glutDisplayFunc(draw)
glutMainLoop()
# End of program
