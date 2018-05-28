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

# encoding des fichiers à analyser, par defaut
UTF8_ENCODING = r'utf-8'
iso_8859_15_ENCODING = r'iso-8859-15'
DEFAULT_DATA_ENCODING = iso_8859_15_ENCODING

# /////////////////////////////////////////////////////////////////////////////
# Format CSV fourni par ADECCO (separateur ;)
# champ 8  / colonne H : Siren
# champ 12 / colonne L : montant impayé
# champ 14 / colonne N : date effet
# champ 24 / colonne X : motif
# /////////////////////////////////////////////////////////////////////////////

KEY_CSV_SEP = 'csv_sep'
KEY_ENCODING = 'encoding'
KEY_HEADER_UTIL = 'header_util'
KEY_HEADER_FULL = 'header_full'
KEY_NB_FIELDS = 'nb_fields'
KEY_COLS = 'cols'
KEY_SIREN = 'siren'
KEY_MNT = 'mnt'
KEY_DATEFF = 'dateff'
KEY_MOTIF = 'motif'
KEY_COL_NAME = 'col_name'
KEY_COL_NAME_RE = 'col_name_re'
KEY_COL_POS = 'col_pos'
KEY_COL_LTR = 'col_ltr'
KEY_COL_RE = 're'
KEY_OK = 'OK'
KEY_KO = 'KO'
KEY_LINE_NO = 'line_no'
KEY_IS_BAD = 'is_bad'
KEY_WHAT_IS_BAD = 'what_is_bad'
KEY_LINE = 'line'
# dict {'lettre colonne Excel': position}
# le décodage ASCII -> unicode est nécessaire car chr et ord fonctionnent sur un caractère en ASCII
# or en tête de fichier on souhaite travailler avec unicode_literals
# et on souhaite des clés de dictionnaires en unicode pour ne pas être limité
EXCEL_COL_NO = dict([(chr(ord('A') + i).decode(b'ASCII'), i + 1) for i in range(26)])

remet_params = \
    {
        'ADECCO':
            {
                KEY_ENCODING : iso_8859_15_ENCODING,
                KEY_CSV_SEP  : ';',
                KEY_NB_FIELDS: 24,
                KEY_COLS     :
                    {
                        KEY_SIREN :
                            {
                                KEY_COL_NAME   : 'Siren',
                                KEY_COL_NAME_RE: ' *[Ss]iren',
                                KEY_COL_LTR    : 'H',  # colonne H
                                KEY_COL_POS    : EXCEL_COL_NO['H'],
                                KEY_COL_RE     : r'^[0-9]{9}'
                                },
                        KEY_MNT   :
                            {
                                KEY_COL_NAME   : 'Montant',
                                KEY_COL_NAME_RE: ' *[Mm]ontant *$',
                                KEY_COL_LTR    : 'L',  # colonne L
                                KEY_COL_POS    : EXCEL_COL_NO['L'],
                                KEY_COL_RE     : r'^-?([0-9]{1,3} *)*[0-9]{0,3}(,[0-9]*)?'
                                },
                        KEY_DATEFF:
                            {
                                KEY_COL_NAME   : 'Echéance',
                                KEY_COL_NAME_RE: ' *[Ee]ch.ance *$',
                                KEY_COL_LTR    : 'N',  # colonne N
                                KEY_COL_POS    : EXCEL_COL_NO['N'],
                                KEY_COL_RE     : r'^[0-9]{2}/[0-9]{2}/2[0-9]{3}'
                                },
                        KEY_MOTIF :
                            {
                                KEY_COL_NAME   : 'Motif imp (motif deduction)',
                                KEY_COL_NAME_RE: ' *[Mm]otif imp',
                                KEY_COL_LTR    : 'X',  # colonne X
                                KEY_COL_POS    : EXCEL_COL_NO['X'],
                                KEY_COL_RE     : r'^[a-zA-Z]+'
                                }
                        }
                }
        }


def parse_file_header(remet_param, line):
    # dictionnaire 'nom col' : pos_col à partir de la ligne hedaer du fichier
    all_col_name_pos = dict([(elem, index) for (index, elem) in enumerate(line.split(remet_param[KEY_CSV_SEP]))])
    # dictionnaire 'nom col' : pos_col à partir des colonnes déclarées dans la config
    remet_col_names = [col for col in remet_param[KEY_COLS]]
    name_pos = dict()
    for col_name_util in remet_col_names:
        # recherche d'une correspondance entre un nom de colonne dans la config (= nom attendu)
        # et le nom dans le header
        # puis création de la correspondance 'nom codifié dans la cponfig' : pos_col réelle dans le fichier
        col_name_util_re = remet_param[KEY_COLS][col_name_util][KEY_COL_NAME_RE]
        col_name_util_re_comp = re.compile(col_name_util_re)
        for col_name_header in all_col_name_pos:
            if col_name_util_re_comp.match(col_name_header) is not None:
                name_pos[col_name_util] = all_col_name_pos[col_name_header]
                break
    return name_pos


def get_encoding(remets_param, remet_name):
    enc = None
    if KEY_ENCODING in remets_param[remet_name]:
        enc = remets_param[remet_name][KEY_ENCODING]
    if not enc:
        enc = DEFAULT_DATA_ENCODING
    return enc


def process_data_file(p_path_src, file_name_re, remets_param, remet_name):
    # type: (unicode, unicode, Dict, unicode, unicode) -> Dict
    """
    Analyse d'une liste de fichiers de données pour un remettant donné.
    :param p_path_src: chemin pour trouver les fichiers à traiter
    :param file_name_re: RE pour trouver les noms de fichiers
    :param remets_param: le dictionnaire des config des remettants
    :param remet_name: le nom du remettant
    :return: un dictionnaire de tous les résultats de l'analyse des fichiers
        une entrée dans le dict par nom de fichier
            sous chaque entrée, une liste d'enregistrements
                [0] contient un tuple (dict des noms de colonnes utiles, dict des noms de col dans le fichier)
                [1:] un elem de list par ligne du fichier; chaque elem est un dict dont les entrées sont les étapes \
                     de l'analyse des champs
    """
    encoding_src = get_encoding(remets_param, remet_name)
    file_names = get_files(p_path_src, file_name_re)
    file_process_result = dict()
    csv_sep = remets_param[remet_name][KEY_CSV_SEP]
    nb_fields = remets_param[remet_name][KEY_NB_FIELDS]
    # on compile les RE par avance
    field_re = dict()
    for col_cod in remets_param[remet_name][KEY_COLS]:
        field_re[col_cod] = re.compile(remets_param[remet_name][KEY_COLS][col_cod][KEY_COL_RE])

    for file_name in file_names:
        file_process_result[file_name] = dict()
        file_lines = get_file_lines(os.path.join(p_path_src, file_name), encoding_src)
        # map(lambda x: log_write("{}: {}".format(file_name, x), level=logging.DEBUG), file_lines)

        file_process_result[file_name] = []
        # TODO transformer en dict, de façon à éviter que list[0] soit particulière et contienne les haeders ?
        for (ind, line_str) in enumerate(file_lines):
            file_lines_processed = OrderedDict()
            ind += 1  # numerotation commence à 1
            line_fields = line_str.split(csv_sep)
            if ind == 1:
                # on ajoute les colonnes trouvées dans la première ligne de la liste résultat en sortie
                # l'element list[0] de la liste en sortie contiendra un dict des headers
                file_process_result[file_name] += [dict({
                    KEY_HEADER_UTIL: parse_file_header(remets_param[remet_name], line_str),
                    KEY_HEADER_FULL: line_str})]
                #     TODO controler présence de tous les champs nécessaires à la suite du traitement
            else:
                file_lines_processed[KEY_LINE_NO] = ind
                file_lines_processed[KEY_IS_BAD] = False  # pour l'instant, et pour imposer sa position
                file_lines_processed[KEY_WHAT_IS_BAD] = False  # pour l'instant, et pour imposer sa position
                # controle du nb de champs pour la forme
                for field_name in [KEY_NB_FIELDS]:
                    file_lines_processed[field_name] = \
                        ctrl_line_field_value(file_name, field_name, line_str, ind, len(line_fields), nb_fields)
                # cherche et vérifie la valeur de chaque champ présent dans la liste des colonnes
                # de la config du remettant: les champs sont cherchés en fonction du nom de la colonne
                # et non en fonction de la position supposée de la colonne
                for col_cod in remets_param[remet_name][KEY_COLS]:
                    # pour chaque valeur de champ à contrôler, la valeur du champ isolée dans les champs de la ligne
                    # du fichier en entrée, gràce au nom de la colonne et à la structure du CSV déclérée
                    # dans la config du remettant
                    field_pos_real = file_process_result[file_name][0][KEY_HEADER_UTIL][col_cod]
                    field_val = line_fields[field_pos_real]  # type: unicode
                    # supression des " dans les champs (ça arrive avec Excel)
                    field_val = field_val.translate({ord('\"'): None})  # unicode.translate(arg: mapping de caractères)
                    # field_re = remets_param[remet_name][KEY_COLS][col_cod][KEY_COL_RE]
                    file_lines_processed[col_cod] = \
                        ctrl_line_field_re(file_name, col_cod, line_str, ind, field_val,
                                           re_pattern_comp=field_re[col_cod])
                #  le nb de champ n'est plus bloquant
                file_lines_processed[KEY_IS_BAD] = reduce(lambda x, y: x or y,
                                                          [file_lines_processed[field_name][0] == KEY_KO
                                                           for field_name in remets_param[remet_name][KEY_COLS].keys()])
                file_lines_processed[KEY_WHAT_IS_BAD] = [field_name
                                                         for field_name in remets_param[remet_name][KEY_COLS].keys()
                                                         if file_lines_processed[field_name][0] == KEY_KO]
                file_lines_processed[KEY_LINE] = line_str

                file_process_result[file_name] += [file_lines_processed]

    return file_process_result


def ctrl_line_field_value(file_name, field_name, file_line, line_num, field, value):
    if field != value:
        log_write('{},{},Bad {}: {}, {}'.format(file_name, line_num, field_name, field, file_line), level=logging.ERROR)
        return KEY_KO, field
    else:
        log_write('{},{},Good {}: {}, {}'.format(file_name, line_num, field_name, field, file_line),
                  level=logging.DEBUG)
        return KEY_OK, field


def ctrl_line_field_re(file_name, field_name, file_line, line_num, field, re_pattern='.*', re_pattern_comp=None):
    """
    contrôle la validité d'une valeur en fonction d'une RE
    re_pattern ou re_pattern_comp doit être fourni
    :param file_name: nom du fichier d'où provient le champ
    :param field_name: nom du champ analysé
    :param file_line: ligne d'où provient le champ
    :param line_num: no de ligne
    :param field: valeur du champ
    :param re_pattern: motif sous forme de chaine de caractères
    :param re_pattern_comp: motif compilé avec re.compile()
    :return: tuple (état OK/KO, valeur du champ)
    """
    if re_pattern_comp:
        ma = re_pattern_comp.match(field)
    else:
        ma = re.compile(re_pattern).match(field)
    if ma is None:
        log_write('{},{},Bad {}: {}, {}'.format(file_name, line_num, field_name, field, file_line), level=logging.ERROR)
        return KEY_KO, field
    else:
        log_write('{},{},Good {}: {}, {}'.format(file_name, line_num, field_name, field, file_line),
                  level=logging.DEBUG)
        return KEY_OK, field


def get_files(p_path_src, file_name_re):
    # type: (unicode, unicode) -> List
    return filter_files_with_patterns_and_extensions(os.listdir(p_path_src), include_patterns=(file_name_re,))


def get_file_lines(file_name, encoding_src):
    # type: (unicode, unicode) -> List
    flines = []
    with open(file_name, 'rU') as f:     # le mode 'U' gère tous les types de fin de ligne
        for cnt, linef in enumerate(f):
            # print("Line {}: {}".format(cnt, linef.rstrip().decode(encoding_src)))
            flines.append(linef.rstrip().decode(encoding_src))
            # yield linef.rstrip().decode(encoding_src)
    return flines


def result_output(p_result, p_path_dest, remets_param, remet_name):
    encoding_remet = get_encoding(remets_param, remet_name)
    csv_sep = remets_param[remet_name][KEY_CSV_SEP]
    file_name_good_all = remet_name + '_good_all_files.csv'
    header_in_good_all = False
    with open(os.path.join(p_path_dest, file_name_good_all), 'w') as fgood_all:
        for file_name in p_result:
            file_name_bad = ''.join(file_name.split('.')[:-1] + ['_bad.csv'])
            file_name_good = ''.join(file_name.split('.')[:-1] + ['_good.csv'])
            with open(os.path.join(p_path_dest, file_name_good), 'w') as fgood, \
                    open(os.path.join(p_path_dest, file_name_bad), 'w') as fbad:
                headers = p_result[file_name][0]
                outstr = (headers[KEY_HEADER_FULL])
                print('{}'.format(outstr).encode(encoding_remet), file=fgood)
                print('{}'.format(outstr).encode(encoding_remet), file=fbad)
                if not header_in_good_all:
                    header_in_good_all = True
                    print('{}'.format(outstr).encode(encoding_remet), file=fgood_all)
                #  variante qui marche aussi
                # fbad.write('{}'.format(outstr).encode(encoding_remet))
                # fgood.write('{}'.format(outstr).encode(encoding_remet))
                file_out = {True: fbad, False: fgood}
                for line in p_result[file_name][1:]:
                    if line[KEY_IS_BAD]:
                        print('{}{}{}:{}'.format(line[KEY_LINE], csv_sep, KEY_WHAT_IS_BAD,
                                                 ','.join(line[KEY_WHAT_IS_BAD])).encode(encoding_remet), file=fbad)
                    else:
                        # print('{}'.format(line[KEY_LINE]).encode(encoding_remet), file=fgood)
                        # liste des champs utiles et bien renseignés, à metter en sortie
                        pos_utils = [remet_params['ADECCO'][KEY_COLS][k][KEY_COL_POS]
                                     for k in remet_params['ADECCO'][KEY_COLS]]
                        # correspondance entre position attendue du champ en sortie
                        # et nom de la clé du champ dans le résultat
                        map_pos_key = dict([(remet_params['ADECCO'][KEY_COLS][k][KEY_COL_POS], k)
                                            for k in remet_params['ADECCO'][KEY_COLS]])
                        new_line = list()
                        for ifield in range(1, remet_params['ADECCO'][KEY_NB_FIELDS] + 1):
                            if ifield in pos_utils:
                                # line[map_pos_key[ifield]] est un tuple (OK/KO, valeur)
                                # le [0] correspond à l'atet OK/KO
                                # le [1] est pour prendre la valeur
                                new_line += [line[map_pos_key[ifield]][1]]
                            else:
                                new_line += ['']
                        print('{}'.format(csv_sep.join(new_line)).encode(encoding_remet), file=fgood)
                        print('{}'.format(csv_sep.join(new_line)).encode(encoding_remet), file=fgood_all)


def result_output_2(p_result, p_path_dest, remets_param, remet_name):
    """
    Même objectif, mais avec utilisation du package codecs et de l'encodage au niveau du fichier
    donc fait au moment d'écrire, sans avoir besoin de convertir chaque string unicode
    """
    encoding_remet = get_encoding(remets_param, remet_name)
    import codecs
    with codecs.open(os.path.join(p_path_dest, 'result_good.csv'), 'w', encoding=encoding_remet) as fgood, \
            codecs.open(os.path.join(p_path_dest, 'result_bad.csv'), 'w', encoding=encoding_remet) as fbad:
        for file_name in p_result:
            headers = p_result[file_name][0]
            outstr = (headers[KEY_HEADER_FULL])
            fbad.write('{}'.format(outstr))
            fgood.write('{}'.format(outstr))
            # print('{}'.format(outstr), file=fgood)
            # print('{}'.format(outstr), file=fbad)
            for line in p_result[file_name][1:]:
                if line[KEY_IS_BAD]:
                    print('{}'.format(line[KEY_LINE]), file=fbad)
                else:
                    print('{}'.format(line[KEY_LINE]), file=fgood)


def result_display_counts(p_result):
    """
    Affichage de compteurs de bons et de rejets, par fichier
    """
    for file_name in p_result:
        # headers = p_result[file_name][0]
        nb_good = 0
        nb_bad = 0
        nb_what_is_bad = dict()
        for line in p_result[file_name][1:]:
            if line[KEY_IS_BAD]:
                nb_bad += 1
                try:
                    nb_what_is_bad[','.join(line[KEY_WHAT_IS_BAD])] += 1
                except KeyError:
                    nb_what_is_bad[','.join(line[KEY_WHAT_IS_BAD])] = 1

            else:
                nb_good += 1

        print('\'{}\', {} = {}\t{} = {}'.format(file_name, 'goods', nb_good, 'bads', nb_bad))
        for what_is_bad in nb_what_is_bad:
            print('\t\'{}\' = {}'.format(what_is_bad, nb_what_is_bad[what_is_bad]))


if __name__ == "__main__":
    # log_init(level=logging.DEBUG)
    log_init(level=logging.INFO)
    log_write(">>>>>>>>>>>>>>>>>>>> Controle fichiers ADECCO <<<<<<<<<<<<<<<<<<<<")
    # path_root = br"C:\Users\emmanuel_barillot\Documents\Work\Ellixium_ADECCO\2018-01"
    path_root = br"C:\Users\emmanuel_barillot\Documents\Work\Ellixium_ADECCO\2018-05-28"
    path_src = os.path.join(path_root, 'originaux')
    path_dest = os.path.join(path_root, 'corriges')
    # pattern pour les noms de fichiers à rechercher (syntaxe analogue au ls du shell Unix)
    # PATTERN_INGNEGS_ADECCO = br"ADECCO_concat*.csv"
    # PATTERN_FILENAME_INGNEGS_ADECCO = br"ADECCO_2018_02_02.csv"
    # PATTERN_FILENAME_INGNEGS_ADECCO = br"ADECCO_2018_*.csv"
    # PATTERN_FILENAME_INGNEGS_ADECCO = br"IMPAYE DU 19 03 2018.csv"
    # PATTERN_FILENAME_INGNEGS_ADECCO = br"MAIL IMPAYE*.csv"
    PATTERN_FILENAME_INGNEGS_ADECCO = br"*.csv"

    # read_data_file(p_path_src=path_src, file_name_re=PATTERN_INGNEGS_ADECCO)
    result = process_data_file(p_path_src=path_src,
                               file_name_re=PATTERN_FILENAME_INGNEGS_ADECCO,
                               remets_param=remet_params,
                               remet_name='ADECCO'
                               )

    result_output(result, p_path_dest=path_dest, remets_param=remet_params, remet_name='ADECCO')

    # sortie très importante pour bien comprendre la structure de result
    # et pour comprendre comment travailler avec
    INDENT = '    '
    with open(os.path.join(path_dest, 'result.txt'), 'w') as fout:
        for file_name, list_of_OD in result.items():
            log_write('{}'.format(file_name))
            print('{}'.format(file_name), file=fout)
            for one_OD in list_of_OD:
                log_write(INDENT + '{}'.format([field for field in one_OD.items()]))
                print(INDENT + '{}'.format([field for field in one_OD.items() if field[1] is not None]), file=fout)

    # compteurs des bons et rejets, par fichier
    from time import sleep
    sleep(0.5)
    result_display_counts(result)

    log_exit()
