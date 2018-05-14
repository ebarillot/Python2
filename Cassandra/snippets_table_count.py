# coding=utf-8

from cassandra.cluster import Cluster

cluster = Cluster(['tstdar01'])
session = cluster.connect()
session.execute('USE ks_view_search')
# session.execute('CONSISTENCY ONE')
rows = session.execute('select count(*) from solr_entreprise')
for row in rows:
    print('{} {}'.format(row.keyspace_name, row.table_name))


cluster.shutdown()

