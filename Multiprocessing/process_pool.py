# coding=utf-8

from __future__ import print_function, unicode_literals

import multiprocessing


def do_calculation(data):
    return data * 2


def start_process():
    print('Starting', multiprocessing.current_process().name)


if __name__ == '__main__':
    inputs = list(range(10))
    print('Input   :', inputs)

    """
    Utilisation de la fonction map classique (builin)
    """
    builtin_outputs = map(do_calculation, inputs)
    print('Built-in:', builtin_outputs)

    """
    Utilisation de la fonction map du module multiprocessing
    """
    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(processes=pool_size,
                                initializer=start_process,
                                )
    # pool = multiprocessing.Pool(processes=pool_size,
    #                             initializer=start_process,
    #                             maxtasksperchild=2,   # demande de redemarrer le worker même si plus de job
    #                             )
    pool_outputs = pool.map(do_calculation, inputs)
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    print('Pool    :', pool_outputs)
