# coding=utf-8

from cassandra.cluster import Cluster

cluster = Cluster(['tstdar01'])

session = cluster.connect()
session.execute('USE ks_dev1_lake_france')

rows = session.execute('select count(*) from ac1_infos_by_ent')

rows = session.execute('SELECT name, age, email FROM users')
for user_row in rows:
    print('{}, {}, {}'.format(user_row.name, user_row.age, user_row.email))
