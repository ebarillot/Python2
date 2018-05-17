# coding=utf-8

from __future__ import print_function, unicode_literals


import multiprocessing
import logging
import sys


def worker():
    print('Doing some work')
    sys.stdout.flush()


if __name__ == '__main__':
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)
    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()
