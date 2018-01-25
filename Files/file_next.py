# coding=utf-8

from __future__ import print_function, unicode_literals
import logging
import os
import psutil
from operator import itemgetter
import gc
import re
from typing import List, Dict
from collections import OrderedDict
from functools import reduce

from EBCommons.paths_and_files import filter_files_with_patterns_and_extensions
from EBCommons.prog_helper import LocalError, log_exit, log_init, log_write

__author__ = 'Emmanuel Barillot'

# encoding des fichiers log à analyser, par defaut
# DEFAULT_DATA_ENCODING = r'utf-8'
DEFAULT_DATA_ENCODING = r'iso-8859-15'
csv_sep = ';'


def create_file(file_name, encoding_src, nlines):
    # type: (unicode, unicode, int) -> None
    with open(file_name, 'w') as f:
        for i in xrange(nlines):
            f.write('{0:8}: {0:8}\n'.format(i,i))
    return


def get_file_lines_iter(file_name, encoding_src):
    # type: (unicode, unicode) -> List
    flines = [0]*10
    with open(file_name, 'r') as f:
        i = 0
        for linef in f:
            flines[i%10] = linef.rstrip().decode(encoding_src)
            i+=1
            # yield linef.rstrip().decode(encoding_src)
    # print(flines)
    return flines


def get_file_lines_readline(file_name, encoding_src):
    # type: (unicode, unicode) -> List
    flines = [0]*10
    with open(file_name, 'r') as f:
        i = 0
        for linef in f.readlines():
            flines[i%10] = linef.rstrip().decode(encoding_src)
            i+=1
            # yield linef.rstrip().decode(encoding_src)
    # print(flines)
    return flines


def print_proc_rsrc():
    # pid = os.getpid()
    p = psutil.Process()
    with p.oneshot():
        log_write('--- name: {}'.format(p.name()))  # execute internal routine once collecting multiple info
        log_write('cpu_times: {}'.format(p.cpu_times()))  # return cached value
        log_write('cpu_percent: {}'.format(p.cpu_percent()))  # return cached value
        log_write('memory_info: ')  # return cached value
        mem_info_data = map(lambda x: x/1024L, p.memory_info())
        mem_info_names = ['rss', 'vms', 'num_page_faults', 'peak_wset', 'wset', 'peak_paged_pool', 'paged_pool', 'peak_nonpaged_pool', 'nonpaged_pool', 'pagefile', 'peak_pagefile', 'private']
        for name, data in itemgetter(0,1,3,4)(zip(mem_info_names, mem_info_data)):
            log_write('  {}  : {}'.format(name, data))  # return cached value

        # log_write('status: {}'.format(p.status())) # return cached value
        # log_write('create_time: {}'.format(p.create_time()))  # return cached value
        # log_write('memory use: {}'.format(p.memory_info()[3]/1024))

if __name__ == "__main__":
    # log_init(level=logging.DEBUG)
    log_init(level=logging.INFO)
    log_write(">>>>>>>>>>>>>>>>>>>> test lecture fichier <<<<<<<<<<<<<<<<<<<<")
    path_root = br"C:\Users\emmanuel_barillot\Documents\Work\TEMP"
    path_src = path_root
    path_dest = path_root
    # pattern pour les noms de fichiers à rechercher (syntaxe analogue au ls du shell Unix)
    nlines = 10000000
    file_test = br"fichier_test_{}.txt".format(nlines)

    log_write(">> creation fichier de {} lignes".format(nlines))
    gc.collect()
    print_proc_rsrc()
    create_file(os.path.join(path_dest,file_test), DEFAULT_DATA_ENCODING, nlines)
    print_proc_rsrc()

    log_write(">> lecture fichier {} lignes avec fenetre de lecture".format(nlines))
    gc.collect()
    print_proc_rsrc()
    get_file_lines_iter(os.path.join(path_dest, file_test), DEFAULT_DATA_ENCODING)
    print_proc_rsrc()

    log_write(">> lecture fichier {} lignes avec lecture totale".format(nlines))
    gc.collect()
    print_proc_rsrc()
    get_file_lines_readline(os.path.join(path_dest, file_test), DEFAULT_DATA_ENCODING)
    print_proc_rsrc()
    # on voit très bien que la méthode readlines() consomme beaucoup plus de memoire:
    # peak_wset: 684252 pendant l'exécution sur un fichier de 10 000 000 lignes (192 Mo)

    log_exit()
