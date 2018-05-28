# coding=utf-8

from __future__ import print_function, unicode_literals

from pathos.multiprocessing import ProcessingPool as Pool


class Tasks(object):

    @staticmethod
    def process_some_task(item):
        from random import random
        from time import sleep
        import os
        sleep(random()*2)
        print("Processing...", item, "by pid:", os.getpid())


if __name__ == "__main__":
    with Pool(4) as pool:
        pool.map(Tasks.process_some_task, range(10))


'''
On est obligé d'importer les packages random, time et os dans la fonction à cause de l'implémentaion
de pathos sous Windows, qui ne sait pas vraiment faire un fork.
Voir explications:  https://stackoverflow.com/questions/33227545/pathos-multiprocessing-cant-call-any-package-and-function-in-the-class

'''