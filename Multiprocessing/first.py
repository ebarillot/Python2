# coding=utf-8

from __future__ import print_function, unicode_literals
# import os
# import codecs
# import time
# import csv


import multiprocessing


def worker(num):
    """thread worker function"""
    print('Worker:', num)
    return


if __name__ == '__main__':
    print("Number of cpu : ", multiprocessing.cpu_count())
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()

