# coding=utf-8

from __future__ import print_function, unicode_literals

import multiprocessing


def worker(num):
    """thread worker function"""
    p = multiprocessing.current_process()
    print('Worker {}: {} {}'.format(num, p.name, p.pid))
    return
