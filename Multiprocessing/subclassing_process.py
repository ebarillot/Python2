# coding=utf-8

from __future__ import print_function, unicode_literals

import multiprocessing


class Worker(multiprocessing.Process):

    def run(self):
        print('In %s' % self.name)
        return


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = Worker()
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()
