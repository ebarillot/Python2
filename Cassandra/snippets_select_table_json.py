# coding=utf-8

from cassandra.cluster import Cluster

# il faut se connecter au bon cluster/DC pour ne pas avoir une erreur du type:
# Unavailable: Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level LOCAL_ONE"
# car le ks_view_search est sur tstdar05 et tstdar06
cluster = Cluster(['tstdar05'])
session = cluster.connect()
session.execute('USE ks_view_search')
rows = session.execute('select json * from solr_entreprise limit 5')
for row in rows:
    print('{}'.format(row.json))


cluster.shutdown()
