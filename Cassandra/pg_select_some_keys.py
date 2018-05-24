# coding=utf-8

from __future__ import print_function, unicode_literals
import os
import time
from cassandra.cluster import Cluster
from cassandra.query import dict_factory, named_tuple_factory, ordered_dict_factory, tuple_factory
from snippets_metadata_class import ClusterInfo
from lib_timing import TMOD
from lib_read_write import write_rows_tuples, write_rows_tuples_csv


# il faut se connecter au bon cluster/DC pour ne pas avoir une erreur du type:
# Unavailable: Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level LOCAL_ONE"
# car le ks_view_search est sur tstdar05 et tstdar06
TAG = '>>> '
USER_NAME = 'tstdar05'
CLUSTER_NAME = 'ks_view_search'
TABLE_NAME = 'solr_entreprise'
NB_KEYS = 200000


def get_some_keys(a_session, cluster_name, table_name, col_names, limit=5, get_json=False):
    a_session.execute(' '.join(['USE', cluster_name]))
    cqjson = ['json'] if get_json else ['']
    cquery = ' '.join(['select'] + cqjson + [', '.join(col_names)] + ['from', table_name, 'limit', '{}'.format(limit)])
    print('query: {}'.format(cquery))
    rows = a_session.execute(cquery)
    return rows


#
#
if __name__ == "__main__":

    # csv.register_dialect('csvdefault', delimiter=_delimiter, quoting=csv.QUOTE_NONE, lineterminator='\n')

    # mesure de temps
    # chaque entree est
    # - soit une durée
    # - soit un OrderedDict() qui dont chaque entrée contient une durée
    tm = TMOD()

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
    tm['write_rows_tuples'] = TMOD()
    tm['write_rows_tuples'][TMOD.TOTAL] = time.clock()
    write_rows_tuples(''.join([TABLE_NAME, '_keys', '.csv']), rows, tm=tm['write_rows_tuples'])
    # write_rows_tuples_csv(''.join([TABLE_NAME, '_keys', '.csv']), _delimiter, rows)
    tm['write_rows_tuples'][TMOD.TOTAL] = time.clock() - tm['write_rows_tuples'][TMOD.TOTAL]

    cluster.shutdown()

    tm.human_readable()
