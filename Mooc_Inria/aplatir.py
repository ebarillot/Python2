import os
os.chdir(r'D:\Emmanuel\2015-10_MOOC_Python')
from collections import Iterable

def aplatir(conteneurs):
    return [item for liste in conteneurs for item in liste]

    


print aplatir([])
print aplatir([(1,)])
print aplatir(([1],))
print aplatir(
  [ (0, 6, 2),
    [1, ('a', 4), 5]])
print aplatir(
  ( [1, [2, 3]],
    ('a', 'b', 'c')))
print aplatir(
  ( [1, 6],
    ('c', 'b'),
    [2, 3]))
print aplatir(
  ( (1, [2, 3]),
    [],
    'a',
    ['b', 'c']))


def alternat(c1,c2):
    return aplatir(zip([item for item in c1],[item for item in c2]))

print alternat(
  (1, 2),
  ('a', 'b'))
print alternat(
  (1, 2, 3),
  ('a', 'b', 'c'))
print alternat(
  (1, (2, 3)),
  ('a', ['b', 'c']))