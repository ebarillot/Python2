# coding=utf-8

from __future__ import print_function
import sympy as sp
from Optimisation_lineaire.simplex_fun import pvar, simplex_step, solution_numerique, simplex_callback_print

sp.init_printing(use_unicode=True)


x, y = sp.symbols('x y')

f = x*x*x*x + y*y*y*y -2*(x-y)*(x-y)

sp.factor(sp.diff(f, x))
