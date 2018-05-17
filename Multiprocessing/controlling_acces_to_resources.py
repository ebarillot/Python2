# coding=utf-8
from __future__ import print_function, unicode_literals

import multiprocessing
import sys

'''
==>ne marche pas
  File "C:\Users\emmanuel_barillot\Documents\Developpements\Python2\Multiprocessing\controlling_acces_to_resources.py", line 23, in worker_no_with
    stream.write('Lock acquired directly\n')
ValueError: I/O operation on closed file


In situations when a single resource needs to be shared between multiple processes, a Lock can be used to avoid
conflicting accesses.
In this example, the messages printed to the console may be jumbled together if the two processes do not synchronize
their access of the output stream with the lock.
'''


def worker_with(lock, stream):
    with lock:
        stream.write('Lock acquired via with\n')


def worker_no_with(lock, stream):
    lock.acquire()
    try:
        stream.write('Lock acquired directly\n')
    finally:
        lock.release()


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    w = multiprocessing.Process(target=worker_with, args=(lock, sys.stdout))
    nw = multiprocessing.Process(target=worker_no_with, args=(lock, sys.stdout))

    w.start()
    nw.start()

    w.join()
    nw.join()

