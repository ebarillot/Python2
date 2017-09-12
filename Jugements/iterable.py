#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Emmanuel Barillot'

"""
Code expérimental pour tester les différentes façon de voir si un objet est iterable
"""

from traceback import print_exc


# Duck typing
def is_iterable(theElement):
    try:
        iterator = iter(theElement)
    except TypeError:
        # not iterable
        print_exc()
        pass
    else:
        # iterable
        pass

# for obj in iterator:
#     pass


# Type checking
import collections

def is_iterable(theElement):
    if isinstance(theElement, collections.Iterable):
        # iterable
        pass
    else:
        # not iterable
        pass


def is_iterable(theElement):
    try:
        #treat object as iterable
        pass
    except TypeError, e:
        #object is not actually iterable
        print_exc()
        pass



def iterable(a):
    try:
        (x for x in a)
        return True
    except TypeError:
        print_exc()
        return False


isiterable = lambda obj: isinstance(obj, basestring) \
    or getattr(obj, '__iter__', False)