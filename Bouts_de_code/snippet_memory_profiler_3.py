# coding=utf-8

'''
code pris ici:
http://deeplearning.net/software/theano/tutorial/python-memory-management.html
'''

from __future__ import print_function, unicode_literals
import sys


def show_sizeof(x, level=0):
    print('{} {} {} {}'.format("\t" * level, x.__class__, sys.getsizeof(x), x))
    if hasattr(x, '__iter__'):
        if hasattr(x, 'items'):
            for xx in x.items():
                show_sizeof(xx, level + 1)
        else:
            for xx in x:
                show_sizeof(xx, level + 1)


show_sizeof(None)
show_sizeof(3)
show_sizeof(2**63)
show_sizeof(102947298469128649161972364837164)
show_sizeof(918659326943756134897561304875610348756384756193485761304875613948576297485698417)

show_sizeof(3.14159265358979323846264338327950288)

show_sizeof("")
show_sizeof("My hovercraft is full of eels")

show_sizeof([])
show_sizeof([4, "toaster", 230.1])

show_sizeof({})
show_sizeof({'a':213, 'b':2131})



from collections import Mapping, Container
from sys import getsizeof

def deep_getsizeof(o, ids):
    """
    Find the memory footprint of a Python object

    This is a recursive function that drills down a Python object graph
    like a dictionary holding nested dictionaries with lists of lists
    and tuples and sets.

    The sys.getsizeof function does a shallow size of only. It counts each
    object inside a container as pointer only regardless of how big it
    really is.

    :param o: the object
    :param ids:
    :return:
    """
    d = deep_getsizeof
    if id(o) in ids:
        return 0

    r = getsizeof(o)
    ids.add(id(o))

    if isinstance(o, str) or isinstance(0, unicode):
        return r

    if isinstance(o, Mapping):
        return r + sum(d(k, ids) + d(v, ids) for k, v in o.iteritems())

    if isinstance(o, Container):
        return r + sum(d(x, ids) for x in o)

    return r


x = '1234567'
print(deep_getsizeof(x, set()))
