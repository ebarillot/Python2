#!/usr/bin/python
# coding: utf-8
from __future__ import unicode_literals, print_function

__author__ = 'Emmanuel Barillot'

import csv
import datetime
import logging
from os import sys

csv_default_codec = "utf-8"
csv_delimiter = b";"
csv.register_dialect('csvdefault'
                     , delimiter=csv_delimiter
                     , quotechar=b'"'
                     , quoting=csv.QUOTE_MINIMAL
                     , lineterminator='\n'
                     , escapechar=b'\\'
                     )

# caractère pour séparer les éléments d'un chemin en fonction des 3 premiers
# caractères de la plateforme
path_separator = {"win": "\\", "lin": "/"}[sys.platform[0:3]]


def csv_from_excel(excel_file_name, sheet_name=None, codec="utf-8"):
    """
    Conversion de chaque d'un fichier Excel xlsx en un fichier csv
    en utilisant la lib xlrd
    """
    if "xlrd" not in globals().keys():
        import xlrd
    out_csv_file_names = []
    workbook = xlrd.open_workbook(excel_file_name)
    all_worksheets = workbook.sheet_names() if sheet_name is None else [sheet_name]
    for worksheet_name in all_worksheets:
        worksheet = workbook.sheet_by_name(worksheet_name)
        out_csv_file_name = change_file_name_extension(add_suffix_to_file_name(excel_file_name, "_" + worksheet_name),
                                                       "csv")
        with open(out_csv_file_name, 'wb') as out_csv_file:
            wr = csv.writer(out_csv_file, dialect='csvdefault')
            # chaque cellule de chaque ligne est transformée en un objet unicode universel
            # de façon à pouvoir être ensuite encodé avec le codec souhaité
            for rownum in xrange(worksheet.nrows):
                outputRow = []
                for colnum in xrange(worksheet.ncols):
                    if worksheet.cell_type(rownum,colnum) == xlrd.XL_CELL_DATE:
                        dt = xlrd.xldate.xldate_as_datetime(worksheet.cell_value(rownum,colnum), workbook.datemode)
                        field = unicode(dt.strftime("%Y/%m/%d")).encode(codec, errors='ignore')
                    else:
                        field = unicode(worksheet.cell_value(rownum,colnum)).encode(codec, errors='ignore')
                    outputRow.append(field)
                wr.writerow(outputRow)
                # wr.writerow([unicode(entry).encode(codec, errors='ignore') for entry in worksheet.row_values(rownum)])
        out_csv_file_names.append(out_csv_file_name)
    return out_csv_file_names


def csv_from_excel_sheets_using_pandas(excel_file_name, sheet_name=None, codec="utf-8"):
    """
    Conversion de chaque d'un fichier Excel xlsx en un fichier csv
    en utilisant la lib pandas
    """
    if "pd" not in globals().keys():
        import pandas as pd
    out_csv_file_names = []
    with pd.ExcelFile(excel_file_name) as xlsx:
        all_worksheets = xlsx.sheet_names if sheet_name is None else [sheet_name]
        for sheet_name in all_worksheets:
            data_xls = pd.read_excel(excel_file_name, sheet_name, index_col=None)
            out_csv_file_name = change_file_name_extension(add_suffix_to_file_name(excel_file_name, "_" + sheet_name)
                                                           , "csv")
            data_xls.to_csv(out_csv_file_name, sep=csv_delimiter, encoding=codec, line_terminator="\n", errors='ignore')
            out_csv_file_names.append(out_csv_file_name)
    return out_csv_file_names


def utf8_to_iso8859_15(filePathIn, filePathOut):
    """
    Conversion de d'un fichier utf-8 en un fichier iso8859-15
    en utilisant les codecs Python
    """
    import codecs
    fichierIn = codecs.open(filePathIn, "r", encoding="utf-8")
    fichierOut = codecs.open(filePathOut, "w", encoding="iso8859_15", errors="ignore")
    for line in fichierIn:
        fichierOut.write(line)
    fichierIn.close()
    fichierOut.close()


def init_logging():
    logger = logging.getLogger('root')
    FORMAT = "[%(asctime)s:%(levelname)-6s:%(name)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    # logging.basicConfig(filename='copyBilan.log', filemode='w', level=logging.DEBUG)
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logging.info('====================')
    logging.info('BEGIN: ' + str(datetime.datetime.today()))
    logging.info('Python plateforme  = ' + sys.version)
    logging.debug('sys.path   = ')
    for p in sys.path:
        logging.debug('    ' + p)
    logging.info('====================')


def log(msg, *args, **kwargs):
    logging.info(msg, *args, **kwargs)


def close_logging():
    logging.info('====================')
    logging.info('END: ' + str(datetime.datetime.today()))
    logging.info('====================')


def add_suffix_to_file_name(fileName, suffix):
    """Ajoute un suffixe au nom d'un fichier"""
    words = fileName.split(".")
    file_name_trunc = "".join([words[i] for i in range(0, len(words) - 1)])
    return '.'.join(["".join([file_name_trunc, suffix]), words[len(words) - 1]])


def change_file_name_extension(fileName, newExtension):
    """Change l'extension du nom du fichier passé en paramètre"""
    words = fileName.split(".")
    file_name_trunc = "".join([words[i] for i in range(0, len(words) - 1)])
    return '.'.join([file_name_trunc, newExtension])


#############################################################################
if __name__ == "__main__":
    init_logging()

    log("Programme de transformation de fichiers Excel en CSV")
    log("Chaque feuille donne lieu à un fichier CSV")
    log(sys.platform)
    dataDir = r"D:\Documents\Projets\work\Ellixium_ADECCO\2016-12"
    # inputFileListFull = [
    #     r"ADECCO_2016-09-12.xlsx"
    #     , r"ADECCO_2016-09-13.xlsx"
    #     , r"ADECCO_2016-09-14.xlsx"
    #     , r"ADECCO_2016-09-15.xlsx"
    #     , r"ADECCO_2016-09-16.xlsx"
    #     , r"ADECCO_2016-09-16_2.xlsx"
    #     , r"ADECCO_2016-09-19.xlsx"
    #     , r"ADECCO_2016-09-20.xlsx"
    # ]
    inputFileListFull = [
        r"2016-11-29-Classeur1.xlsx"
        , r"2016-11-30-Classeur2.xlsx"
        , r"2016-12-01-IMPAYES_01.12.16.xlsx"
        , r"2016-12-02-IMPAYES_02.12.16.xlsx"
        , r"2016-12-05-Classeur1.xlsx"
        , r"2016-12-06-Classeur1.xlsx"
        , r"2016-12-07-Classeur1.xlsx"
        , r"2016-12-08-Classeur3.xlsx"
    ]

    inputFileListTest = inputFileListFull       #[0:1]

    test_code = 2
    output_codec = ["iso8859_15", "utf-8"][0]  # pour choisir rapidement un encodage

    oneFileListUtf8 = []
    fullListUtf8 = []
    if test_code == 1:
        # conversion Excel -> csv en utilsant pandas
        log("conversion Excel -> csv en utilsant pandas")
        for oneFile in inputFileListTest:
            oneFileTmp = dataDir + path_separator + oneFile
            oneFileListUtf8 = csv_from_excel_sheets_using_pandas(oneFileTmp, codec=output_codec)  # "utf-8"
            log("{} => {}".format(oneFileTmp, ",".join(oneFileListUtf8)))
            fullListUtf8 += oneFileListUtf8

    elif test_code == 2:
        # conversion Excel -> csv csv en utilsant xlrd
        log("conversion Excel -> csv en utilsant xlrd")
        for oneFile in inputFileListTest:
            oneFileTmp = dataDir + path_separator + oneFile
            oneFileListUtf8 = csv_from_excel(oneFileTmp, codec=output_codec)  # "utf-8"
            log("{} => {}".format(oneFileTmp, ",".join(oneFileListUtf8)))
            fullListUtf8 += oneFileListUtf8

    # conversion éventuelle du fichier final de l'utf-8 vers un autre codec
    # si les fichiers obtenus précédemments sont toujours en utf-8
    if output_codec == "utf-8":
        for oneFileUtf8 in fullListUtf8:
            oneFileIso8859 = add_suffix_to_file_name(oneFileUtf8, "_2")
            utf8_to_iso8859_15(oneFileUtf8, oneFileIso8859)

    close_logging()
