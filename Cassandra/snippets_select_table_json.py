# coding=utf-8

import os
from cassandra.cluster import Cluster
from cassandra.query import dict_factory, named_tuple_factory
from snippets_metadata_class import ClusterInfo

# TODO: si col_names est None, aller chercher la pk de la table


def get_some_keys(a_session, cluster_name, table_name, col_names, limit=5, get_json=False):
    a_session.execute(' '.join(['USE', cluster_name]))
    cqjson = ['json'] if get_json else ['']
    cquery = ' '.join(['select'] + cqjson + [', '.join(col_names)] + ['from', table_name, 'limit', '{}'.format(limit)])
    print('query: {}'.format(cquery))
    rows = a_session.execute(cquery)
    return rows


#
#
if __name__ == "__main__":
    # il faut se connecter au bon cluster/DC pour ne pas avoir une erreur du type:
    # Unavailable: Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level LOCAL_ONE"
    # car le ks_view_search est sur tstdar05 et tstdar06
    TAG = '>>> '
    USER_NAME = 'tstdar05'
    CLUSTER_NAME = 'ks_view_search'
    TABLE_NAME = 'solr_entreprise'
    COL_NAMES = ['entnum']
    # infos sur le cluster
    cluInfo = ClusterInfo(USER_NAME)
    tab_pk = cluInfo.get_tab_pk(CLUSTER_NAME, TABLE_NAME)
    # travail sur le cluster
    cluster = Cluster([USER_NAME])
    session = cluster.connect()
    session.execute('USE ks_view_search')

    print('Working DIR: {}'.format(os.getcwd()))
    PATH_ROOT = os.getcwd()
    if os.path.basename(os.getcwd()) != PATH_ROOT:
        os.chdir(PATH_ROOT)

    print(TAG + 'Select des pk de quelques lignes')
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, tab_pk)
    for row in rows:
        print('{}'.format(row))

    print(TAG + 'Select des colonnes choisies de quelques lignes')
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, COL_NAMES)
    for row in rows:
        print('{}'.format(row))

    # retour en json : chaque row est une string qui contient un json
    print(TAG + 'Select des pk de quelques lignes, retour en json')
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, tab_pk, get_json=True)
    for num, row in enumerate(rows):
        print('{0:3d} {1:s}'.format(num, row.json))

    # retour en dict
    print(TAG + 'Select des pk de quelques lignes, retour en dict')
    session.row_factory = dict_factory
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, tab_pk)
    for num, row in enumerate(rows):
        print('{0:3d} {1:s}'.format(num, row))

    # retour en named_tuple
    print(TAG + 'Select des pk de quelques lignes, retour en named_tuple')
    session.row_factory = named_tuple_factory
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, tab_pk)
    for num, row in enumerate(rows):
        print('{0:3d} {1:s} {2:s}'.format(num, row.entnum, row.nic))

    # retour en named_tuple et écriture dans un fichier
    print(TAG + 'Select des pk de quelques lignes, retour dans un fichier')
    session.row_factory = named_tuple_factory
    with open(''.join([TABLE_NAME,'_keys','.csv']),'w+') as f:
        rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, tab_pk)
        for row in rows:
            f.write('{};{}\n'.format(row.entnum, row.nic))

    cluster.shutdown()
