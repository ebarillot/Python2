# coding=utf-8

from __future__ import print_function, unicode_literals
import os
from cassandra.cluster import Cluster
from cassandra.query import dict_factory, named_tuple_factory, ordered_dict_factory, tuple_factory, ConsistencyLevel
from memory_profiler import memory_usage, profile
import time

from snippets_metadata_class import ClusterInfo
from lib_timing import TMOD
from lib_read_write import write_rows_raw, read_keys_from_files

# il faut se connecter au bon cluster/DC pour ne pas avoir une erreur du type:
# Unavailable: Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency ...
# car le ks_view_search est sur tstdar05 et tstdar06
TAG = '>>> '
USER_NAME = 'tstdar05'
CLUSTER_NAME = 'ks_view_search'
TABLE_NAME = 'solr_entreprise'
keys_list = ['413387143']
col_names = ['entnum']


# @profile(precision=2)
def get_some_records_from_keys(a_session, table_name, where_col_names, keys_list=[], cluster_name=None, get_json=False):
    if not keys_list or keys_list == []:
        return []
    if cluster_name:
        a_session.execute(' '.join(['USE', cluster_name]))
    # print(col_names)
    # print(['{}=?'.format(col_name) for col_name in col_names])
    cqjson = ['json'] if get_json else ['']
    query = ' '.join(['select *'] + cqjson
                     + ['from', table_name]
                     + ['where'] + [' and '.join(['{}=?'.format(col_name) for col_name in where_col_names])])
    print('query: {}'.format(query))
    print('keys: {}'.format(keys_list))
    stmt = a_session.prepare(query)
    stmt.consistency_level = ConsistencyLevel.ONE
    rows_xtr = []
    for key in keys_list:
        rows_xtr += a_session.execute(stmt, [key])
    return rows_xtr


#
#
if __name__ == "__main__":
    # mesure de temps
    tm = TMOD()

    # infos sur le cluster
    tm['ClusterInfo'] = time.clock()
    cluInfo = ClusterInfo(USER_NAME)
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

    tm['get_some_records_from_keys'] = time.clock()
    rows = get_some_records_from_keys(session,
                                      TABLE_NAME,
                                      where_col_names = col_names,
                                      cluster_name=CLUSTER_NAME,
                                      keys_list=keys_list)
    print('Rows: {}'.format(len(rows)))
    for num, row in enumerate(rows[:10]):   # les 10 premières seulement
        print('{0:2d} : {1}'.format(num+1, row))
    tm['get_some_records_from_keys'] = time.clock() - tm['get_some_records_from_keys']

    cluster.shutdown()

    print()
    tm.human_readable()

    # mem_usage = memory_usage(-1, interval=.2, timeout=1)
    # print(mem_usage)
