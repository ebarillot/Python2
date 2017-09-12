# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 09:22:48 2016

@author: emmanuel_barillot
"""


from rpy2.robjects import r

# si on est dans le repertoire de la base
r.load("base_val.RData")

# avec le chemin complet
r.load(r"D:\Documents\Projets\Developpements\Python\RData\base_val.RData")

