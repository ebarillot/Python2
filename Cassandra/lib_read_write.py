# coding=utf-8
from __future__ import print_function, unicode_literals
import codecs
import time
import csv
from memory_profiler import memory_usage, profile

# encoding des fichiers
UTF8_ENCODING = r'utf-8'
iso_8859_15_ENCODING = r'iso-8859-15'
DEFAULT_DATA_ENCODING = UTF8_ENCODING
CSV_DELIMITER = b';'


# @profile(precision=2)
def read_keys_from_files(key_file_name, delimiter=CSV_DELIMITER, enc=DEFAULT_DATA_ENCODING):
    with codecs.open(key_file_name, 'rb', encoding=enc, buffering=1048576) as f:
        reader = csv.reader(f, delimiter=delimiter)
        # reader = csv.reader(f, 'csvdefault')  # avec dialect csvdefault défini plus haut
        keys = [tuple(row) for row in reader]
    return keys


# @profile(precision=2)
def write_rows_raw(file_name, rows, enc=DEFAULT_DATA_ENCODING):
    with open(file_name, 'wb', buffering=1048576) as f:
        for row in rows:
            f.write(('{}'.format(row)+'\n').encode(enc))


# @profile(precision=2)
def write_rows_tuples(file_name, rows, tm, enc=DEFAULT_DATA_ENCODING):
    tm['resultset tuple to csv rows'] = time.clock()
    all_rows = [';'.join(map(lambda x: '' if x is None else x, row))
                for row in rows]  # parcours de liste de loin l'opération la plus longue
    tm['resultset tuple to csv rows'] = time.clock() - tm['resultset tuple to csv rows']
    tm['encoding'] = time.clock()
    buf = '\n'.join(all_rows).encode(encoding=enc)
    tm['encoding'] = time.clock() - tm['encoding']
    tm['write'] = time.clock()
    with open(file_name, 'wb', buffering=1048576) as f:
        f.write(buf)
    tm['write'] = time.clock() - tm['write']
    # autres tentatives, ni plus lentes ni plus rapides
    # with open(file_name, 'wb', buffering=1048576) as f:
    #     for row in rows:
    #         f.write(row[0]+';'+row[1]+'\n')
    # with open(file_name, 'wb', buffering=1048576) as f:
    #     for row in rows:
    #         f.write(row[0]+';'+row[1]+'\n')
    # with codecs.open(file_name, 'wb', encoding=enc) as f:
    #     for row in rows:
    #         f.write(';'.join(row))
    #         f.write('\n')


def write_rows_tuples_csv(file_name, delimiter, rows, enc=DEFAULT_DATA_ENCODING):
    with codecs.open(file_name, 'wb', encoding=enc) as f:
        # ouvert en mode b pour que le lineterminator soit pris en compte si dessous, voir doc csv.writer
        csv_writer = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_NONE, lineterminator='\n')
        for row in rows:
            csv_writer.writerow(row)

