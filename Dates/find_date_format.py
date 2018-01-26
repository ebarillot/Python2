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
csv_sep = ';'


def create_file(file_name, encoding_src, nlines):
    # type: (unicode, unicode, int) -> None
    with open(file_name, 'w') as f:
        for i in xrange(nlines):
            f.write('{0:02}/{1:02}/{2:4}\n'.format(i%27+1,(i*i)%11+1,2010+((i*i*i)%7)))
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

    file_name_dest_split = os.path.splitext(file_name_src)
    file_lines_src = get_file_lines(file_name_src, encoding_src)
    # map(lambda x : log_write("{}: {}".format(file_name_src,x),level=logging.DEBUG), file_lines_src)

    for (ind, val) in enumerate(file_lines_src):
        log_write(val)
    return


def guess_date_format(sample):
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
    return guess


if __name__ == "__main__":
    # log_init(level=logging.DEBUG)
    log_init(level=logging.INFO)
    log_write(">>>>>>>>>>>>>>>>>>>> test lecture fichier et détection format de date <<<<<<<<<<<<<<<<<<<<")
    path_root = br"C:\Users\emmanuel_barillot\Documents\Work\TEMP"
    path_src = path_root
    path_dest = path_root
    # pattern pour les noms de fichiers à rechercher (syntaxe analogue au ls du shell Unix)
    nlines = 100
    file_test = br"fichier_date_test_{}.txt".format(nlines)

    create_file(os.path.join(path_dest,file_test), DEFAULT_DATA_ENCODING, nlines)
    process_data_file(os.path.join(path_dest,file_test), DEFAULT_DATA_ENCODING)

    log_exit()
