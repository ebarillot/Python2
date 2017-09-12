# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""


from rpy2.robjects import r
r('x <- rnorm(100)')  # generate x at R
r('y <- x + rnorm(100,sd=0.5)')  # generate y at R
r('plot(x,y)')  # have R plot them


r.load(r"D:\Documents\Projets\Developpements\Python\RData\base_val.RData")

