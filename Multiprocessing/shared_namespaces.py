# coding=utf-8
from __future__ import print_function, unicode_literals

import multiprocessing

'''
In addition to dictionaries and lists, a Manager can create a shared Namespace.
Any named value added to the Namespace is visible to all of the clients that receive the Namespace instance.
'''


def producer(ns, event):
    ns.value = 'This is the value'
    event.set()


def consumer(ns, event):
    try:
        value = ns.value
    except Exception as err:
        print('Before event, consumer got:', str(err))
    event.wait()
    print('After event, consumer got:', ns.value)


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    namespace = mgr.Namespace()
    event = multiprocessing.Event()
    p = multiprocessing.Process(target=producer, args=(namespace, event))
    c = multiprocessing.Process(target=consumer, args=(namespace, event))

    c.start()
    p.start()

    c.join()
    p.join()
