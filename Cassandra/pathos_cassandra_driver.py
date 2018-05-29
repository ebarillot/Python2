# coding=utf-8

import itertools
from pathos.multiprocessing import ProcessingPool as Pool
import time

from cassandra.cluster import Cluster
from cassandra.concurrent import execute_concurrent_with_args
from cassandra.query import tuple_factory


def query_gen(n):
    for _ in xrange(n):
        yield ('local', )


class QueryManager(object):

    concurrency = 100  # chosen to match the default in execute_concurrent_with_args

    def __init__(self, cluster, process_count=None):
        self.pool = Pool(processes=process_count, initializer=self._setup, initargs=(cluster,))

    @classmethod
    def _setup(cls, cluster):
        cls.session = cluster.connect()
        cls.session.row_factory = tuple_factory
        cls.prepared = cls.session.prepare('SELECT * FROM system.local WHERE key=?')

    def close_pool(self):
        self.pool.close()
        self.pool.join()

    def get_results(self, params):
        params = list(params)
        results = self.pool.map(_multiprocess_get, (params[n:n + self.concurrency] for n in xrange(0, len(params), self.concurrency)))
        return list(itertools.chain(*results))

    @classmethod
    def _results_from_concurrent(cls, params):
        return [results[1] for results in execute_concurrent_with_args(cls.session, cls.prepared, params)]


# cette fonction est extérieure à toute classe et attachée de fait au top level (racine) du module
# de façon à être pickle-able: c'est une limite de pickle, qui ne sait pas sérialiser une méthode directement.
# Par contre, dans cette fonction, on peut appeler une méthode d'une classe. Comment pickle s'en sort ? mystère ...
def _multiprocess_get(params):
    return QueryManager._results_from_concurrent(params)


if __name__ == '__main__':
    # try:
    #     iterations = int(sys.argv[1])
    #     processes = int(sys.argv[2]) if len(sys.argv) > 2 else None
    # except (IndexError, ValueError):
    #     print("Usage: %s <num iterations> [<num processes>]" % sys.argv[0])
    #     sys.exit(1)

    iterations = 1000
    processes = 4

    cluster = Cluster(['tstdar05'])
    qm = QueryManager(cluster, processes)

    start = time.time()
    rows = qm.get_results(query_gen(iterations))
    delta = time.time() - start
    print("%d queries in %s seconds (%s/s)" % (iterations, delta, iterations / delta))

'''
Erreur avec pickle:
PicklingError("Can't pickle <class 'cassandra.io.libevreactor.SetType(VarcharType)'
'''