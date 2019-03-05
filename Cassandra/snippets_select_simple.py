# coding=utf-8

from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement

cluster = Cluster(['tstdar01'])

session = cluster.connect()

# query = SimpleStatement("select ent_id from ks_view_search.solr_etablissement limit 20",
#                         consistency_level=ConsistencyLevel.QUORUM)
# query = SimpleStatement("select ent_id from ks_dev1_view_search.solr_etablissement limit 20",
#                         consistency_level=ConsistencyLevel.QUORUM)
query = SimpleStatement("select ent_id from ks_uat1_view_search.solr_etablissement limit 20",
                        consistency_level=ConsistencyLevel.QUORUM)

rows = session.execute(query)
for row in rows:
    print('{}'.format(row.ent_id))

