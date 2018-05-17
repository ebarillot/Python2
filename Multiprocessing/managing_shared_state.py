# coding=utf-8


from __future__ import print_function, unicode_literals

import multiprocessing


'''
In the previous example (controlling_concurrent_access_to_resources.py),
the list of active processes is maintained centrally
in the ActivePool instance via a special type of list object created by a Manager.
The Manager is responsible for coordinating shared information state between all of its users.

By creating the list through the manager, it is shared and updates are seen in all processes. Dictionaries are also supported.
'''

def worker(d, key, value):
    d[key] = value


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    d = mgr.dict()
    jobs = [ multiprocessing.Process(target=worker, args=(d, i, i*2))
             for i in range(10)
             ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print('Results:', d)
