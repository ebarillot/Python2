# coding=utf-8

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd


def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)


cluster = Cluster(
    contact_points=['tstdar01'],
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
)
session = cluster.connect()
session.execute('USE ks_dev1_lake_france')
session.row_factory = pandas_factory
session.default_fetch_size = 10000000 #needed for large queries, otherwise driver will do pagination. Default is 50000.

rows = session.execute("""select count(*) from ac1_infos_by_ent""")
df = rows._current_rows
print df.head()

