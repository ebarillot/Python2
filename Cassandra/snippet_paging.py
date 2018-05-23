# coding=utf-8

from cassandra.cluster import Cluster

USER_NAME = 'tstdar05'
cluster = Cluster([USER_NAME])
print('protocol_version: {}'.format(cluster.protocol_version))
