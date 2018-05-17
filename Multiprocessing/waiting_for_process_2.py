# coding=utf-8

from __future__ import print_function, unicode_literals


import multiprocessing
import time
import sys

'''
By default, join() blocks indefinitely. It is also possible to pass a timeout argument
 (a float representing the number of seconds to wait for the process to become inactive).
  If the process does not complete within the timeout period, join() returns anyway.
'''


def daemon():
    print('Starting:', multiprocessing.current_process().name)
    time.sleep(2)
    print('Exiting :', multiprocessing.current_process().name)


def non_daemon():
    print('Starting:', multiprocessing.current_process().name)
    print('Exiting :', multiprocessing.current_process().name)


if __name__ == '__main__':
    d = multiprocessing.Process(name='daemon', target=daemon)
    d.daemon = True

    n = multiprocessing.Process(name='non-daemon', target=non_daemon)
    n.daemon = False

    d.start()
    n.start()

    d.join(1)   # timeout
    print('d.is_alive()', d.is_alive())
    n.join()

'''
Since the timeout passed is less than the amount of time the daemon sleeps, the process is still “alive” after join() returns.
'''