# coding=utf-8

from __future__ import print_function, unicode_literals
import os
import codecs
from collections import OrderedDict
from cassandra.cluster import Cluster
from cassandra.concurrent import execute_concurrent_with_args
from cassandra.query import dict_factory, named_tuple_factory, ordered_dict_factory, tuple_factory, ConsistencyLevel
from memory_profiler import memory_usage, profile

from snippets_metadata_class import ClusterInfo
import time
import csv


# encoding des fichiers
UTF8_ENCODING = r'utf-8'
iso_8859_15_ENCODING = r'iso-8859-15'
DEFAULT_DATA_ENCODING = UTF8_ENCODING
CSV_DELIMITER = b';'

# csv.register_dialect('csvdefault', delimiter=_delimiter, quoting=csv.QUOTE_NONE, lineterminator='\n')

# mesure de temps
tm = OrderedDict()


# @profile(precision=2)
def read_keys_from_files(key_file_name, delimiter=CSV_DELIMITER, enc=DEFAULT_DATA_ENCODING):
    with codecs.open(key_file_name, 'rb', encoding=enc, buffering=1048576) as f:
        reader = csv.reader(f, delimiter=delimiter)
        # reader = csv.reader(f, 'csvdefault')  # avec dialect csvdefault défini plus haut
        keys = [tuple(row) for row in reader]
    return keys


# @profile(precision=2)
def get_some_records_from_keys(a_session, table_name, col_names, keys_list=[], cluster_name=None, get_json=False):
    if not keys_list or keys_list == []:
        return []
    if cluster_name:
        a_session.execute(' '.join(['USE', cluster_name]))
    # print(col_names)
    # print(['{}=?'.format(col_name) for col_name in col_names])
    cqjson = ['json'] if get_json else ['']
    query = ' '.join(['select *'] + cqjson
                      + ['from', table_name]
                      + ['where'] + [' and '.join(['{}=?'.format(col_name) for col_name in col_names])])
    print('query: {}'.format(query))
    stmt = a_session.prepare(query)
    stmt.consistency_level = ConsistencyLevel.ONE
    # print(keys_list[0])
    # print(type(keys_list[0]))
    # rows = a_session.execute(stmt, keys_list[0])
    rows = []
    for key in keys_list:
        rows += a_session.execute(stmt, list(key))
    return rows


def get_some_records_from_keys_concurrent(a_session, table_name, col_names,
                                          keys_list=[],
                                          cluster_name=None,
                                          get_json=False,
                                          concurrency=50):
    if not keys_list or keys_list == []:
        return []
    if cluster_name:
        a_session.execute(' '.join(['USE', cluster_name]))
    # print(col_names)
    # print(['{}=?'.format(col_name) for col_name in col_names])
    cqjson = ['json'] if get_json else ['']
    query = ' '.join(['select *'] + cqjson
                      + ['from', table_name]
                      + ['where'] + [' and '.join(['{}=?'.format(col_name) for col_name in col_names])])
    print('query: {}'.format(query))
    stmt = a_session.prepare(query)
    stmt.consistency_level = ConsistencyLevel.ONE
    # print(keys_list[0])
    # print(type(keys_list[0]))
    # rows = a_session.execute(stmt, keys_list[0])
    rows = []
    results = execute_concurrent_with_args(session, stmt, keys_list, concurrency=concurrency)
    for (success, result) in results:
        if not success:
            print('Failed: {}'.format(result))  # result will be an Exception
        else:
            rows += result  # result will be a list of rows
    return rows


def write_rows_tuples(file_name, rows, enc=DEFAULT_DATA_ENCODING):
    tm['all_rows'] = time.clock()
    all_rows = [';'.join(row) for row in rows]  # parcours de liste de loin l'opération la plus longue
    tm['all_rows'] = time.clock() - tm['all_rows']
    tm['buf'] = time.clock()
    buf = '\n'.join(all_rows).encode(encoding=enc)
    tm['buf'] = time.clock() - tm['buf']
    tm['write'] = time.clock()
    with open(file_name, 'wb', buffering=1048576) as f:
        f.write(buf)
    tm['write'] = time.clock() - tm['write']


def write_rows_tuples_csv(file_name, delimiter, rows, enc=DEFAULT_DATA_ENCODING):
    with codecs.open(file_name, 'wb', encoding=enc) as f:
        # ouvert en mode b pour que le lineterminator soit pris en compte si dessous, voir doc csv.writer
        csv_writer = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_NONE, lineterminator='\n')
        for row in rows:
            csv_writer.writerow(row)


def human_readable_tm(tm):
    filler = ['.'] * 100
    len_max = max([len(tm_name) for tm_name in tm])
    tm_total = sum([tm[tm_name] for tm_name in tm])
    print('Execution times:')
    for num, tm_name in enumerate(tm):
        print('{0:2d} {1:s} {2:s} : {3:6.3f}s  {4:3.1f}%'
              .format(num + 1,
                      tm_name,
                      ''.join(filler[:len_max + 2 - len(tm_name)]),
                      tm[tm_name],
                      100. * tm[tm_name] / tm_total))
    print('{0:2s} {1:s} {2:s} : {3:6.3f}s'
          .format('', 'Total', ''.join(filler[:len_max + 2 - len('Total')]), tm_total))


#
#
if __name__ == "__main__":

    # il faut se connecter au bon cluster/DC pour ne pas avoir une erreur du type:
    # Unavailable: Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency ...
    # car le ks_view_search est sur tstdar05 et tstdar06
    TAG = '>>> '
    USER_NAME = 'tstdar05'
    CLUSTER_NAME = 'ks_view_search'
    TABLE_NAME = 'solr_entreprise'
    NB_KEYS = 100000

    # infos sur le cluster
    tm['ClusterInfo'] = time.clock()
    cluInfo = ClusterInfo(USER_NAME)
    tab_pk = cluInfo.get_tab_pk(CLUSTER_NAME, TABLE_NAME)
    tm['ClusterInfo'] = time.clock() - tm['ClusterInfo']

    # travail sur le cluster
    tm['Cluster'] = time.clock()
    cluster = Cluster([USER_NAME])
    tm['Cluster'] = time.clock() - tm['Cluster']
    tm['cluster.connect'] = time.clock()
    session = cluster.connect()
    tm['cluster.connect'] = time.clock() - tm['cluster.connect']

    print('Working DIR: {}'.format(os.getcwd()))
    PATH_ROOT = os.getcwd()
    if os.path.basename(os.getcwd()) != 'Cassandra':
        os.chdir(PATH_ROOT)

    # retour en named_tuple et écriture dans un fichier
    session.row_factory = tuple_factory # le plus simple
    print(TAG + 'Select des pk de quelques lignes, retour dans un fichier')

    tm['USE ks_view_search'] = time.clock()
    session.execute('USE ks_view_search')
    tm['USE ks_view_search'] = time.clock() - tm['USE ks_view_search']

    tm['read_keys_from_files'] = time.clock()
    keys_list = read_keys_from_files(''.join([TABLE_NAME, '_keys', '.csv']))
    print('keys read: {}'.format(len(keys_list)))
    # print('type(keys_list) : {}'.format(type(keys_list)))
    # print('type(keys_list[0]) : {}'.format(type(keys_list[0])))
    tm['read_keys_from_files'] = time.clock() - tm['read_keys_from_files']

    tm['get_some_records_from_keys'] = time.clock()
    rows = get_some_records_from_keys(session, TABLE_NAME, tab_pk, cluster_name=CLUSTER_NAME, keys_list=keys_list[:50])
    print('Rows: {}'.format(len(rows)))
    print('10 first rows:')
    for num, row in enumerate(rows[:10]):   # les 10 premières seulement
        print('{0:2d} : {1}'.format(num+1, row))
    tm['get_some_records_from_keys'] = time.clock() - tm['get_some_records_from_keys']

    tm['get_some_records_from_keys_concurrent'] = time.clock()
    rows = get_some_records_from_keys_concurrent(session, TABLE_NAME, tab_pk,
                                                 cluster_name=CLUSTER_NAME,
                                                 keys_list=keys_list[:2000],
                                                 concurrency=100)   # semble optimal, mieux que 50 ou 200
    print('Rows: {}'.format(len(rows)))
    print('10 first rows:')
    for num, row in enumerate(rows[:10]):   # les 10 premières seulement
        print('{0:2d} : {1}'.format(num+1, row))
    tm['get_some_records_from_keys_concurrent'] = time.clock() - tm['get_some_records_from_keys_concurrent']

    # sortie fichier
    # tm['write_rows_tuples'] = time.clock()
    # # write_rows_tuples(''.join([TABLE_NAME, '_keys', '.csv']), rows)
    # write_rows_tuples_csv(''.join([TABLE_NAME, '_keys', '.csv']), CSV_DELIMITER, rows)
    # tm['write_rows_tuples'] = time.clock() - tm['write_rows_tuples']

    cluster.shutdown()

    human_readable_tm(tm)

    # mem_usage = memory_usage(-1, interval=.2, timeout=1)
    # print(mem_usage)
