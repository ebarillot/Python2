import os
os.chdir(r'D:\Emmanuel\2015-10_MOOC_Python')
from collections import Iterable

def intersect(A,B):
    dA = dict(A)
    dB = dict(B)
    print dA, dB
    sA = set(dA.keys())
    sB = set(dB.keys())
    print sA, sB
    sAB = sA.intersection(sB)
    print sAB
    return {dA[key] for key in sAB}.union({dB[key] for key in sAB})
##    return set([dA[key] for key in sAB] + [ dB[key] for key in sAB])


print intersect(
  set([ (8, 'huit'),
        (10, 'dixA'),
        (12, 'douze')]),
  set([ (5, 'cinq'),
        (10, 'dixB'),
        (15, 'quinze')]))

print intersect(
  set([ (1, 'unA'),
        (2, 'deux'),
        (3, 'troisA')]),
  set([ (1, 'unB'),
        (2, 'deux'),
        (4, 'quatreB')]))
