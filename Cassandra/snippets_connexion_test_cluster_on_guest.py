# coding=utf-8

from cassandra.cluster import Cluster

cluster = Cluster(['192.168.56.33'])

session = cluster.connect()
session.execute('USE system')

rows = session.execute('SELECT cluster_name, listen_address FROM system.local')
for row in rows:
    print('{}   {}'.format(row.cluster_name, row.listen_address))

