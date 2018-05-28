# coding=utf-8

from __future__ import print_function, unicode_literals


def coroutine():
    i = -1
    while True:
        i += 1
        val = (yield i)
        print("Received %s" % val)


sequence = coroutine()
print(sequence) # ==> <generator object coroutine at 0x0000000004800B88>
sequence.next() # ==> 0
sequence.next() # ==> affiche Received None 1 et retourne 1
sequence.send('hello') # ==> affiche Received hello 1 et retourne 2
sequence.close()
