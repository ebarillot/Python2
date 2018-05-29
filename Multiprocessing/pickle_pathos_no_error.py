# coding=utf-8

import os
from pathos.multiprocessing import ProcessingPool as Pool


class Tasks(object):

    @staticmethod
    def process_some_task(item):
        print("Processing...", item, "by pid:", os.getpid())


if __name__ == "__main__":
    pool = Pool(4)
    pool.map(Tasks.process_some_task, range(10))
    pool.close()


'''
Avec pathos, pas d'erreur pickle ! normal, il utilise la sérialisatrion dill
'''