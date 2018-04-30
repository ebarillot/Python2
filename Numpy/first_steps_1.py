# coding=utf-8

from __future__ import unicode_literals
import numpy as np

#
# ATTENTION avec l'utilisation des strings en unicode
# quand on active:  from __future__ import unicode_literals
# l'unicode en fonctionne pas dans la clé des définitions des dtypes
# Il faut que les chaines des clés soient encodées (ou préfixées par b)
#


# définition de types
dt = np.dtype('>i4')
dt = np.dtype('i4')
# tableau avec utilisation d'un dtype
np.array([9, 3], dtype=dt)
np.array([9, 3], dtype='i4')
np.array([9], dtype='i4')
np.array(['a'], dtype='U25')
np.array(['b'], dtype='a25')
z = np.arange(3, dtype=np.uint8)
z
z = np.array([1, 2, 3], dtype='f')
z


# dtypes composites
a = np.array([('a',9)], dtype='U25, i4')
x = np.array([(1,2.,'Hello'), (2,3.,"World")])
x
#  ATTENTION: les clés des dtypes doivent être encodées, elles ne doivent pas rester en unicode
# x = np.array([(1,2.,'Hello'), (2,3.,"World")], dtype=[(b'foo', 'i4'),(b'bar', 'f4'), (b'baz', 'S10')])
#    ==> TypeError: data type not understood
x = np.array([(1,2.,'Hello'), (2,3.,"World")], dtype=[(b'foo', 'i4'),(b'bar', 'f4'), (b'baz', 'S10')])
x = np.array([(1, 2., 'Hello'), (2, 3., "World")],
             dtype=[('foo'.encode('UTF8'), 'i4'), ('bar'.encode('UTF8'), 'f4'), ('baz'.encode('UTF8'), 'S10')])

dt = np.dtype([(b'name', np.unicode_, 16), (b'grades', np.float64, (2,))])
np.dtype([(b'big', '>i4'), (b'little', '<i4')])

# utilisation d'un dictionnaire explicite des types
dt = np.dtype({'names': ['r','g','b','a'], 'formats': [np.uint8, np.uint8, np.uint8, np.uint8]})
dt = np.dtype({'col1': ('U10', 0), 'col2': (np.float32, 10), 'col3': (int, 14)})
# np.dtype({b'name': ('U10',), b'age': ('i4',), b'weight': ('f4',)})
# ==> ValueError: entry not a 2- or 3- tuple
# np.array([('Rex', 9, 81.0), ('Fido', 3, 27.0)], dtype={b'name': 'U10', b'age': 'i4', b'weight': 'f4'})
# ==> ValueError: entry not a 2- or 3- tuple


# dtype composite avec nom des champs
arr = np.array([(1,2.,'Hello'),(2,3.,"World")], dtype=[(b'foo', 'i4'), (b'bar', 'f4'), (b'baz', 'S10')])
arr['foo']      # => marche
arr[b'foo']     # => marche

np.array([('Rex', 9, 81.0), ('Fido', 3, 27.0)], dtype=[(b'name', 'U10'), (b'age', 'i4'), (b'weight', 'f4')])
np.dtype([(b'x', 'f4')])
np.dtype([(b'y', np.float32)])
np.dtype([(b'x', 'f4'), (b'y', np.float32), (b'z', 'f4', (2,2))])
np.zeros(4,)
np.zeros((2,), dtype=[(b'x', b'i4'), (b'y', b'i4')])



