# coding=utf-8

import os
from pathos.multiprocessing import ProcessPool as Pool


class Bar:

    def foo(self, name):
        return len(str(name))

    def boo(self, things):
        print("{} ({})  things: {}".format(os.getpid(), os.getppid(), things))
        for thing in things:
            self.sum += self.foo(thing)
        return self.sum
    sum = 0


if __name__ == "__main__":
    b = Bar()
    pool = Pool(4)
    results = pool.map(b.boo, [[12, 3, 456], [8, 9, 10], ['a', 'b', 'cde']])
    pool.close()
    print(results)
    print(b.sum)


