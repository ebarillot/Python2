#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Emmanuel Barillot'


# exemple pris ici : http://www.saltycrane.com/blog/2007/09/how-to-sort-python-dictionary-by-keys/


# à partir de Python 2.4

my_dict = {'carl': 40,
          'alan': 2,
          'bob': 1,
          'danny': 3}

for key in sorted(my_dict):
    print("%s: %s" % (key, my_dict[key]))