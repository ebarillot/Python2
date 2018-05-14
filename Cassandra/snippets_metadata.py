# coding=utf-8

from cassandra.cluster import Cluster

cluster = Cluster(['tstdar01'])
session = cluster.connect()

# tout ce qu'on peut lire dans les metadata
dir(cluster.metadata)
cluster.metadata.cluster_name
print(cluster.metadata.export_schema_as_string())
cluster.metadata.partitioner
cluster.metadata.get_replicas('ks_view_search', '775995798')

cluster.metadata.token_map.ring
cluster.metadata.token_map.token_to_host_owner
cluster.metadata.token_map.token_class

# les noeuds du cluster
cluster.metadata.all_hosts()
# les ks accessibles dans le cluster
ks_dict = cluster.metadata.keyspaces
# le dict de tous les ks
ks_dict



# colonnes d'une table particulière du ks system
ks_dict['system'].tables  # => toutes les tables
ks_dict['system'].tables['paxos'].columns
ks_dict['system'].tables['peers'].columns

for k in ks_dict['system'].tables['peers'].columns:
    print("{}\t{}".format(k, ks_dict['system'].tables['peers'].columns[k].cql_type))

rows = session.execute('select * from system.peers')
for row in rows:
    print('{}'.format(row))


# colonnes d'une table particulière d'un autre ks system: équivalent du dictionnaire Oracle
type(ks_dict['system_schema'])
print("{} {}".format('system_schema', ks_dict['system_schema']))

ks_dict['system_schema'].tables
ks_dict['system_schema'].tables['tables'].name
ks_dict['system_schema'].tables['tables'].columns
ks_dict['system_schema'].tables['tables'].primary_key


type(ks_dict['system_schema'].tables['columns'].columns)
ks_dict['system_schema'].tables['columns'].columns
for k in ks_dict['system_schema'].tables['columns'].columns:
    print("{}\t{}".format(k, ks_dict['system_schema'].tables['columns'].columns[k].cql_type))


# colonnes d'une table particulière d'un ks applicatif
ks_dict['ks_view_search'].tables  # => dict dont les 2 clés sont: solr_entreprise, solr_entreprise_darwin
ks_dict['ks_view_search'].tables['solr_entreprise'].columns
ks_dict['ks_view_search'].tables['solr_entreprise'].columns['entnum'].cql_type
ks_dict['ks_view_search'].tables['solr_entreprise'].columns['entnum'].is_static
ks_dict['ks_view_search'].tables['solr_entreprise'].columns['entnum'].is_reversed
ks_dict['ks_view_search'].tables['solr_entreprise_darwin'].columns
ks_dict['ks_view_search'].tables['solr_entreprise_darwin'].columns['entnum'].cql_type
ks_dict['ks_view_search'].tables['solr_entreprise_darwin'].columns['entnum'].is_static
ks_dict['ks_view_search'].tables['solr_entreprise_darwin'].columns['entnum'].is_reversed

# pour obtenir le script de création d'une table
ks_dict['ks_view_search'].tables['solr_entreprise'].export_as_string()
ks_dict['ks_view_search'].tables['solr_entreprise_darwin'].export_as_string()

cluster.shutdown()
