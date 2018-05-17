# coding=utf-8

from __future__ import print_function, unicode_literals

import multiprocessing
import importable_target_function_worker

'''Importable Target Functions'''

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=importable_target_function_worker.worker, args=(i,))
        jobs.append(p)
        p.start()
