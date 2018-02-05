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


def get_files(p_path_src, file_name_re):
    # type: (unicode, unicode) -> List
    return filter_files_with_patterns_and_extensions(os.listdir(p_path_src), include_patterns=(file_name_re,))


def get_file_lines(file_name, encoding_src):
    # type: (unicode, unicode) -> List
    flines = []
    with open(file_name, 'r') as f:
        for linef in f:
            flines.append(linef.rstrip().decode(encoding_src))
            # yield linef.rstrip().decode(encoding_src)
    return flines


def process_data_file(p_path_src, p_path_dest, file_name_re, encoding_src=DEFAULT_DATA_ENCODING):
    # type: (unicode, unicode, unicode, unicode) -> None
    file_names_src = get_files(p_path_src, file_name_re)

    for file_name_src in file_names_src:
        file_name_dest_split = os.path.splitext(file_name_src)
        file_name_dest = file_name_dest_split[0] +'_corr' + file_name_dest_split[1]
        file_lines_dest = []
        file_lines_src = get_file_lines(os.path.join(p_path_src,file_name_src), encoding_src)
        # map(lambda x : log_write("{}: {}".format(file_name_src,x),level=logging.DEBUG), file_lines_src)

        for (ind, val) in enumerate(file_lines_src):
            if ind == 0:
                file_lines_dest.append(val)
            else:
                fields = val.split(csv_sep)
                # correction de la date
                field_date = fields[2].split('/')
                field_date_corr = field_date[2]+field_date[1]+field_date[0]
                line_dest = csv_sep.join([fields[0], fields[1], ''.join(field_date_corr)] + fields[3:])
                file_lines_dest.append(line_dest)

        with open(os.path.join(p_path_dest,file_name_dest), r'w') as fout:
            for val in file_lines_dest:
                print('{}'.format(val).encode(DEFAULT_DATA_ENCODING),file=fout)
    return


if __name__ == "__main__":
    # log_init(level=logging.DEBUG)
    log_init(level=logging.INFO)
    log_write(">>>>>>>>>>>>>>>>>>>> Correction fichiers CODINF <<<<<<<<<<<<<<<<<<<<")
    path_root = br"C:\Users\emmanuel_barillot\Documents\Work\Ellixium_CODINF"
    path_src = path_root
    path_dest = path_root
    # pattern pour les noms de fichiers à rechercher (syntaxe analogue au ls du shell Unix)
    PATTERN_INGNEGS_ADECCO = br"CODINF_IMPAYES_20180118.csv"

    # read_data_file(p_path_src=path_src, file_name_re=PATTERN_INGNEGS_ADECCO)
    process_data_file(p_path_src=path_src,
                      p_path_dest=path_src,
                      file_name_re=PATTERN_INGNEGS_ADECCO)

    log_exit()
