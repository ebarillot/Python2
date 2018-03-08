# coding=utf-8
#
# NumExpr est une API vers une pachine virtuelle qui exécute le code python
# compilé en byte code python puis en byte code spécifique à cette VM
# et qui s'exécute théoriquement plus vite que numpy
# Cette VM tire profit du multithreading (OpenMP ?) et de VML, MKL de Intel (si activé / installé)
#
# exemples de https://github.com/pydata/numexpr
# https://numexpr.readthedocs.io/en/latest/index.html

import numpy as np
import numexpr as ne
import timeit


def init_1D():
    return np.arange(1e6)   # Choose large arrays for better speedups


setup_for_run="""
import numexpr as ne
from __main__ import init_1D
a = init_1D()
b = init_1D()
"""


timeit.timeit('init_1D()', setup=setup_for_run, number=100)

timeit.timeit('ne.evaluate("a + 1")', setup=setup_for_run, number=100)  # a simple expression

timeit.timeit('ne.evaluate("a*b-4.1*a > 2.5*b")', setup=setup_for_run, number=100)  # a more complex one

timeit.timeit('ne.evaluate("sin(a) + arcsinh(a/b)")', setup=setup_for_run, number=100)     # you can also use functions

ne.print_versions()
ne.detect_number_of_cores()
ne.detect_number_of_threads()
ne.get_vml_version()

s = np.array(['abba', 'abbb', 'abbcdef'])
ne.evaluate("'abba' == s")   # string arrays are supported too

