# coding=utf-8

from __future__ import print_function, unicode_literals
import os
import codecs
from collections import OrderedDict
from cassandra.cluster import Cluster
from cassandra.query import dict_factory, named_tuple_factory, ordered_dict_factory, tuple_factory
from snippets_metadata_class import ClusterInfo
import time
import csv

# encoding des fichiers
UTF8_ENCODING = r'utf-8'
iso_8859_15_ENCODING = r'iso-8859-15'
DEFAULT_DATA_ENCODING = UTF8_ENCODING

_delimiter = b';'
# csv.register_dialect('csvdefault', delimiter=_delimiter, quoting=csv.QUOTE_NONE, lineterminator='\n')

# mesure de temps
tm = OrderedDict()


def get_some_keys(a_session, cluster_name, table_name, col_names, limit=5, get_json=False):
    a_session.execute(' '.join(['USE', cluster_name]))
    cqjson = ['json'] if get_json else ['']
    cquery = ' '.join(['select'] + cqjson + [', '.join(col_names)] + ['from', table_name, 'limit', '{}'.format(limit)])
    print('query: {}'.format(cquery))
    rows = a_session.execute(cquery)
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
    # tm['write'] = time.clock()
    with codecs.open(file_name, 'wb', encoding=enc) as f:
        # ouvert en mode b pour que le lineterminator soit pris en compte si dessous, voir doc csv.writer
        csv_writer = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_NONE, lineterminator='\n')
        for row in rows:
            csv_writer.writerow(row)
    # tm['write'] = time.clock() - tm['write']


def human_readable_tm(tm):
    filler = ['.'] * 100
    len_max = max([len(tm_name) for tm_name in tm])
    tm_total = sum([tm[tm_name] for tm_name in tm])
    for num, tm_name in enumerate(tm):
        print('{0:2d} {1:s} {2:s} : {3:6.3f}s  {4:3.1f}%'
              .format(num + 1,
                      tm_name,
                      ''.join(filler[:len_max + 2 - len(tm_name)]),
                      tm[tm_name],
                      100.*tm[tm_name] / tm_total))
    print('{0:2s} {1:s} {2:s} : {3:6.3f}s'
          .format('', 'Total', ''.join(filler[:len_max + 2 - len('Total')]), tm_total))


#
#
if __name__ == "__main__":

    # il faut se connecter au bon cluster/DC pour ne pas avoir une erreur du type:
    # Unavailable: Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level LOCAL_ONE"
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
    print(TAG + 'Select des pk de quelques lignes, retour dans un fichier')
    tm['USE ks_view_search'] = time.clock()
    session.execute('USE ks_view_search')
    tm['USE ks_view_search'] = time.clock() - tm['USE ks_view_search']
    session.row_factory = tuple_factory
    tm['get_some_keys'] = time.clock()
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, tab_pk, limit=NB_KEYS)
    tm['get_some_keys'] = time.clock() - tm['get_some_keys']
    # sortie fichier
    tm['write_rows_tuples'] = time.clock()
    # write_rows_tuples(''.join([TABLE_NAME, '_keys', '.csv']), rows)
    write_rows_tuples_csv(''.join([TABLE_NAME, '_keys', '.csv']), _delimiter, rows)
    tm['write_rows_tuples'] = time.clock() - tm['write_rows_tuples']

    cluster.shutdown()

    human_readable_tm(tm)
