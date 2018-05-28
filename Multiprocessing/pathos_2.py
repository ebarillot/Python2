# coding=utf-8

from __future__ import print_function, unicode_literals

'''
On est obligé d'importer les packages random, time et os dans la fonction à cause de l'implémentaion
de pathos sous Windows, qui ne sait pas vraiment faire un fork.
Voir explications:  https://stackoverflow.com/questions/33227545/pathos-multiprocessing-cant-call-any-package-and-function-in-the-class

REMARQUE: cette version fonctionne sans problème sous Linux CentOS7 !!!

'''

from pathos.multiprocessing import ProcessingPool as Pool
from random import random
from time import sleep
from os import getpid


class Tasks(object):

    @staticmethod
    def process_some_task(item):
        _process_some_task(item)


def _process_some_task(item):
    sleep(random() * 2)
    print("Processing...", item, "by pid:", getpid())


if __name__ == "__main__":
    with Pool(4) as pool:
        pool.map(Tasks.process_some_task, range(10))

