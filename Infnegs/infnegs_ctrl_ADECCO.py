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


# Bases unicode:
# - str et unicode sont des types, pas des encodages
# - en Python2 une str est une suite de bytes et encodée en ascii par defaut
# - en Python3 une str est unicode et est encodée en utf-8 par defaut
# - Deux fonctions essentielles:
#       - s.decode(encodage):  str -> unicode
#           transforme une str en une variable de type unicode en mémoire en décodant les bytes de la str en fonction
#           de l'encodage indiqué
#       - u.encode(encodage):  unicode -> str
#           transforme une variable de type unicode en mémoire en une chaine de caractères encodée
#           avec l'encodage indiqué
#

# encoding des fichiers log à analyser, par defaut
# DEFAULT_DATA_ENCODING = r'utf-8'
DEFAULT_DATA_ENCODING = r'iso-8859-15'

#/////////////////////////////////////////////////////////////////////////////
# Format CSV fourni par ADECCO (separateur ;)
# champ 8  / colonne H : Siren
# champ 12 / colonne L : montant impayé
# champ 14 / colonne N : date effet
# champ 24 / colonne X : motif
#/////////////////////////////////////////////////////////////////////////////


remet_params = \
    {
        'ADECCO':
            {
                'csv_sep': ';',
                'nb_fields': 24,
                'siren':
                    {
                        'pos': 8,       # colonne H
                        're': r'^[0-9]{9}'
                        },
                'mnt':
                    {
                        'pos': 12,      # colonne L
                        're': r'^-?([0-9]{1,3} *)*[0-9]{0,3}(,[0-9]*)?'
                        },
                'dateff':
                    {
                        'pos': 14,      # colonne N
                        're': r'^[0-9]{2}/[0-9]{2}/2[0-9]{3}'
                        },
                'motif':
                    {
                        'pos': 24,      # colonne X
                        're': r'^[a-zA-Z]+'
                        }
                }
        }



def read_data_file(p_path_src, file_name_re, encoding_src=DEFAULT_DATA_ENCODING):
    # type: (unicode, unicode, unicode) -> None
    """
    """
    for file_name in filter_files_with_patterns_and_extensions(os.listdir(p_path_src),
                                                               include_patterns=(file_name_re,)):
        log_write("Lecture: {}".format(file_name))
        with open(os.path.join(p_path_src,file_name), 'r') as f:
            for linef in f:
                # print('linef: ',end=''); print(type(linef)) # type de variable linef => str en Python2
                line = linef.rstrip().decode(encoding_src)
                # print('line: ',end=''); print(type(line)) # type de variable line => unicode en Python2
                # log_write("line: {}".format(line),level=logging.DEBUG) # ne plante pas car line est de type unicode
                # print(line.encode("utf-8"))
                # log_write(line.encode("utf-8")) # plante, normal car log_write attend une unicode, pas une str encodée
                # print('line_utf8: ',end=''); print(type(line.encode("utf-8")))
                print(len(line.split(";")))
                pass


def process_data_file(p_path_src,
                      file_name_re,
                      remet_param,
                      remet_name,
                      encoding_src=DEFAULT_DATA_ENCODING):
    # type: (unicode, unicode, Dict, unicode, unicode) -> Dict
    file_names = get_files(p_path_src, file_name_re)
    file_process_result = dict()
    csv_sep    = remet_param[remet_name]['csv_sep']
    nb_fields  = remet_param[remet_name]['nb_fields']

    for file_name in file_names:
        file_process_result[file_name] = dict()
        file_lines = get_file_lines(os.path.join(p_path_src,file_name), encoding_src)
        map(lambda x : log_write("{}: {}".format(file_name,x),level=logging.DEBUG), file_lines)

        file_process_result[file_name] = []
        for (ind, val) in enumerate(file_lines):        # sans la ligne header
            ind += 1    # numerotation commence à 1
            if ind == 1:
                continue

            file_lines_processed = OrderedDict()
            file_lines_processed['line'] = ind
            file_lines_processed['bad'] = False
            for field_name in ['nb_fields']:
                file_lines_processed[field_name] = \
                    ctrl_line_field_value(file_name,
                                          field_name,
                                          val,
                                          ind,
                                          len(val.split(csv_sep)),
                                          nb_fields)
            for field_name in ['siren', 'mnt', 'dateff', 'motif']:
                file_lines_processed[field_name] = \
                    ctrl_line_field_re(file_name,
                                       field_name,
                                       val,
                                       ind,
                                       val.split(csv_sep)[remet_param[remet_name][field_name]['pos'] - 1],
                                       remet_param[remet_name][field_name]['re'])
            file_lines_processed['val'] = val

            file_lines_processed['bad'] = reduce(lambda x, y: x or y,
                                                    [ file_lines_processed[field_name] is not None
                                                      for field_name in ['nb_fields','siren', 'mnt', 'dateff', 'motif']
                                                      ])

            if file_lines_processed['bad']:
                file_process_result[file_name] += [ file_lines_processed ]

        # print(file_lines_len)
        # print(file_lines_siren)
        # print(file_lines_mnt)
        # print(file_lines_dateff)
        # print(file_lines_motif)
    return file_process_result


def ctrl_line_field_value(file_name,field_name,file_line,line_num,field,value):
    if field != value:
        log_write('{},{},Bad {}: {}, {}'.format(file_name,line_num,field_name,field,file_line),level=logging.ERROR)
        return field
    else:
        log_write('{},{},Good {}: {}, {}'.format(file_name,line_num,field_name,field,file_line),level=logging.INFO)
        return None


def ctrl_line_field_re(file_name,field_name,file_line,line_num,field,re_pattern):
    regx = re.compile(re_pattern)
    ma = regx.match(field)
    if ma is None:
        log_write('{},{},Bad {}: {}, {}'.format(file_name,line_num,field_name,field,file_line),level=logging.ERROR)
        return field
    else:
        log_write('{},{},Good {}: {}, {}'.format(file_name,line_num,field_name,field,file_line),level=logging.INFO)
        return None


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


if __name__ == "__main__":
    # log_init(level=logging.DEBUG)
    log_init(level=logging.INFO)
    log_write(">>>>>>>>>>>>>>>>>>>> Controle fichiers ADECCO <<<<<<<<<<<<<<<<<<<<")
    # path_root = br"C:\Users\emmanuel_barillot\Documents\Work\Ellixium_ADECCO\2018-01"
    path_root = br"C:\Users\emmanuel_barillot\Documents\Work\Ellixium_ADECCO\2018-01"
    path_src = path_root
    path_dest = path_root
    # pattern pour les noms de fichiers à rechercher (syntaxe analogue au ls du shell Unix)
    PATTERN_INGNEGS_ADECCO = br"ADECCO_concat*.csv"
    # PATTERN_INGNEGS_ADECCO = br"ADECCO*.csv"

    # read_data_file(p_path_src=path_src, file_name_re=PATTERN_INGNEGS_ADECCO)
    result = process_data_file(p_path_src=path_src,
                               file_name_re=PATTERN_INGNEGS_ADECCO,
                               remet_param=remet_params,
                               remet_name='ADECCO'
                               )

    INDENT='    '
    for file_name, list_of_OD in result.iteritems():
        log_write('{}'.format(file_name))
        for one_OD in list_of_OD:
            log_write(INDENT+'{}'.format([field for field in one_OD.items()]))

    with open(os.path.join(path_dest,'result.txt'),'w') as fout:
        for file_name, list_of_OD in result.iteritems():
            print('{}'.format(file_name),file=fout)
            for one_OD in list_of_OD:
                log_write()
                print(INDENT + '{}'.format([field for field in one_OD.items() if field[1] is not None]),file=fout)

    log_exit()
