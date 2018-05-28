# coding=utf-8

import os
from multiprocessing import Pool


class Tasks(object):

    @staticmethod
    def process_some_task(item):
        print("Processing...", item, "by pid:", os.getpid())


if __name__ == "__main__":
    pool = Pool(4)
    pool.map(Tasks.process_some_task, range(10))
    pool.close()


'''
Produit normalement ce message:
(qui est dû qu fait que pickle ne sait pas sérialiser une méthode)

Traceback (most recent call last):
  File "C:/Users/emmanuel_barillot/Documents/Developpements/Python2/Multiprocessing/pickle_error.py", line 16, in <module>
    pool.map(Tasks.process_some_task, range(10))
  File "C:\ProgramData\Anaconda2\lib\multiprocessing\pool.py", line 251, in map
    return self.map_async(func, iterable, chunksize).get()
  File "C:\ProgramData\Anaconda2\lib\multiprocessing\pool.py", line 567, in get
    raise self._value
cPickle.PicklingError: Can't pickle <type 'function'>: attribute lookup __builtin__.function failed

'''