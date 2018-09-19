# coding=utf-8

from cassandra.cluster import Cluster

# cluster = Cluster(['192.168.56.33'])
# cluster = Cluster(['192.168.56.34'])
cluster = Cluster(['192.168.60.35'])
# cluster = Cluster(['192.168.60.100'])
# cluster = Cluster(['192.168.60.101'])
# cluster = Cluster(['192.168.60.102'])

session = cluster.connect()
session.execute('USE system')

rows = session.execute('SELECT cluster_name, listen_address FROM system.local')
for row in rows:
    print('{}   {}'.format(row.cluster_name, row.listen_address))

