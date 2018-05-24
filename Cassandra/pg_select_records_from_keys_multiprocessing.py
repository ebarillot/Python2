# coding=utf-8

from __future__ import print_function, unicode_literals

import itertools
from multiprocessing import Pool
import os
import time

from cassandra.cluster import Cluster
from cassandra.concurrent import execute_concurrent_with_args
from cassandra.query import tuple_factory

from snippets_metadata_class import ClusterInfo
from lib_timing import TMOD
from lib_read_write import read_keys_from_files


USER_NAME = 'tstdar05'
CLUSTER_NAME = 'ks_view_search'
TABLE_NAME = 'solr_entreprise'


class QueryManager(object):

    concurrency = 100  # chosen to match the default in execute_concurrent_with_args

    def __init__(self, initargs, process_count=None):
        self.pool = Pool(processes=process_count, initializer=self._setup, initargs=initargs)

    @classmethod
    def _setup(cls, cluster, table_name, col_names, cluster_name=None, get_json=False):
        cls.session = cluster.connect()
        cls.session.row_factory = tuple_factory
        cqjson = ['json'] if get_json else ['']
        query = ' '.join(['select *'] + cqjson
                         + ['from', table_name]
                         + ['where'] + [' and '.join(['{}=?'.format(col_name) for col_name in col_names])])
        print('query: {}'.format(query))
        if cluster_name:
            cls.session.execute(' '.join(['USE', cluster_name]))
        cls.prepared = cls.session.prepare(query)

    def close_pool(self):
        self.pool.close()
        self.pool.join()

    def get_results(self, params):
        params = list(params)
        results = self.pool.map(_multiprocess_get,
                                (params[n:n + self.concurrency] for n in range(0, len(params), self.concurrency)))
        return list(itertools.chain(*results))

    @classmethod
    def _results_from_concurrent(cls, params):
        return [results[1] for results in execute_concurrent_with_args(cls.session, cls.prepared, params)]


# TODO: pourquoi n'est pas une methode de classe ?
def _multiprocess_get(params):
    return QueryManager._results_from_concurrent(params)


if __name__ == '__main__':
    # mesure de temps
    tm = TMOD()

    processes = 4
    nb_queries = 200

    print('Working DIR: {}'.format(os.getcwd()))
    PATH_ROOT = os.getcwd()
    if os.path.basename(os.getcwd()) != 'Cassandra':
        os.chdir(PATH_ROOT)

    # infos sur le cluster
    tm['ClusterInfo'] = time.clock()
    cluInfo = ClusterInfo(USER_NAME)
    tab_pk = cluInfo.get_tab_pk(CLUSTER_NAME, TABLE_NAME)
    tm['ClusterInfo'] = time.clock() - tm['ClusterInfo']

    tm['read_keys_from_files'] = time.clock()
    keys_list = read_keys_from_files(''.join([TABLE_NAME, '_keys', '.csv']))
    print('keys read: {}'.format(len(keys_list)))
    tm['read_keys_from_files'] = time.clock() - tm['read_keys_from_files']

    cluster = Cluster([USER_NAME])
    qm = QueryManager(initargs=(cluster, TABLE_NAME, tab_pk, CLUSTER_NAME, False), process_count=processes)

    start = time.time()
    rows = qm.get_results(keys_list[:200])
    delta = time.time() - start
    print("%d queries in %s seconds (%s/s)" % (nb_queries, delta, nb_queries / delta))
    qm.close_pool()
    cluster.shutdown()
    tm.human_readable()
