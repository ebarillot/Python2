# coding=utf-8

from cassandra.cluster import Cluster

cluster = Cluster(['tstdar01'])

session = cluster.connect()
session.execute('USE ks_dev1_lake_france')

rows = session.execute('select ac1seq from ac1_infos_by_ent limit 20')
for row in rows:
    print('{}'.format(row.ac1seq))

