# coding=utf-8
from __future__ import print_function, unicode_literals

import multiprocessing

'''
It is important to know that updates to the contents of mutable values in the namespace are not propagated automatically.
To update the list, attach it to the namespace object again.
'''


def producer(ns, event):
    ns.my_list.append('This is the value')  # DOES NOT UPDATE GLOBAL VALUE!
    event.set()


def consumer(ns, event):
    print('Before event, consumer got:', ns.my_list)
    event.wait()
    print('After event, consumer got:', ns.my_list)


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    namespace = mgr.Namespace()
    namespace.my_list = []

    event = multiprocessing.Event()
    p = multiprocessing.Process(target=producer, args=(namespace, event))
    c = multiprocessing.Process(target=consumer, args=(namespace, event))

    c.start()
    p.start()

    c.join()
    p.join()
