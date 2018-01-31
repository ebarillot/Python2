# coding=utf-8

from __future__ import print_function, unicode_literals
import logging
import os
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
csv_sep = r';'
date_seps = r'/_.- '


def create_file(file_name, encoding_src, nlines):
    # type: (unicode, unicode, int) -> None
    with open(file_name, 'w') as f:
        for i in xrange(nlines,0,-1):
            f.write('{0:02}/{1:02}/{2:4}\n'.format(i%27+1,(i*i)%11+1,2010+((i*i*i)%7)).encode(encoding_src))
    return


def get_file_lines(file_name, encoding_src):
    # type: (unicode, unicode) -> List
    flines = []
    with open(file_name, 'r') as f:
        for linef in f:
            flines.append(linef.rstrip().decode(encoding_src))
            # yield linef.rstrip().decode(encoding_src)
    return flines


def process_data_file(file_name_src, encoding_src=DEFAULT_DATA_ENCODING):
    # type: (unicode, unicode) -> None

    file_lines_src = get_file_lines(file_name_src, encoding_src)
    guess_date_format(file_lines_src)
    return


def guess_date_format(lines):
    # type: (List) -> unicode
    guess = ''
    #
    # 1. chercher la presence de separateur
    # 2. mettre les valeurs DD, MM, YYYY ou YY dans des variables
    # 3. si format YYYY => champ année est trouvé, reste à départager DD et MM
    # 4. analyser les valeurs de chaque collection
    # 5. YY: 01 -> 99
    #    MM: 01 -> 12
    #    DD: 01 -> 31
    #  si il existe une ligne avec un champ > 31 => année
    #  si il existe une ligne avec un champ > 12 => jour
    # 6. tenter avec le nb de valeurs différentes: jour > mois > années ?

    sep_pos = dict()
    len_date = []
    val_date = []
    for sep in date_seps:
        sep_pos[sep] = []
        for ind, line in enumerate(lines):
            list_of_pos = []
            beg = 0
            pos = line.find(sep, beg)
            while pos > 0:
                list_of_pos.append(pos)
                beg = pos +1
                pos = line.find(sep, beg)
            if list_of_pos != []:
                sep_pos[sep].append(list_of_pos)
                len_date.append(len(line))
                val_date.append(line.split(sep))
        if len(sep_pos[sep]) == 0:
            del sep_pos[sep]
    minmax_fields = [
        [min([val_date[i][j] for i in range(len(val_date))]), max([val_date[i][j] for i in xrange(len(val_date))])]
        for j in xrange(len(val_date[0]))
        ]
    # minmax_fields = [
    #     [min([val_date[i][0] for i in xrange(len(val_date))]), max([val_date[i][0] for i in xrange(len(val_date))])]
    #   , [min([val_date[i][1] for i in xrange(len(val_date))]), max([val_date[i][1] for i in xrange(len(val_date))])]
    #   , [min([val_date[i][2] for i in xrange(len(val_date))]), max([val_date[i][2] for i in xrange(len(val_date))])]
    #     ]

    print(len_date)
    print(val_date)
    print(minmax_fields)
    for key in sep_pos.iterkeys():
        print(sep_pos[key])
    return guess


if __name__ == "__main__":
    # log_init(level=logging.DEBUG)
    log_init(level=logging.INFO)
    log_write(">>>>>>>>>>>>>>>>>>>> test lecture fichier et détection format de date <<<<<<<<<<<<<<<<<<<<")
    path_root = br"C:\Users\emmanuel_barillot\Documents\Work\TEMP"
    path_src = path_root
    path_dest = path_root
    # pattern pour les noms de fichiers à rechercher (syntaxe analogue au ls du shell Unix)
    nlines = 10
    file_test = br"fichier_date_test_{}.txt".format(nlines)

    create_file(os.path.join(path_dest,file_test), DEFAULT_DATA_ENCODING, nlines)
    process_data_file(os.path.join(path_dest,file_test), DEFAULT_DATA_ENCODING)

    log_exit()
