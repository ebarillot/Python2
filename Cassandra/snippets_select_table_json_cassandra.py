# coding=utf-8

from __future__ import print_function, unicode_literals
import os
import codecs
from itertools import izip

from cassandra.cluster import Cluster
from cassandra.query import dict_factory, named_tuple_factory, ordered_dict_factory
from snippets_metadata_class import ClusterInfo


# encoding des fichiers
UTF8_ENCODING = r'utf-8'
iso_8859_15_ENCODING = r'iso-8859-15'
DEFAULT_DATA_ENCODING = UTF8_ENCODING


def get_some_keys(a_session, cluster_name, table_name, col_names, limit=5, get_json=False):
    a_session.execute(' '.join(['USE', cluster_name]))
    cqjson = ['json'] if get_json else ['']
    cquery = ' '.join(['select'] + cqjson + [', '.join(col_names)] + ['from', table_name, 'limit', '{}'.format(limit)])
    print('query: {}'.format(cquery))
    rows = a_session.execute(cquery)
    return rows


def write_rows_tuples(file_name, rows, enc=DEFAULT_DATA_ENCODING):
    with codecs.open(file_name,'w', encoding=enc) as f:
        for row in rows:
            f.write(';'.join(row))
            f.write('\n')


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

    # Par defaut, une row est un named_tuple
    # et rows est une liste de named_tuple
    print(TAG + 'Select des pk de quelques lignes')
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, col_names=tab_pk)
    print('rows type: {}'.format(type(rows))) # => <class 'cassandra.cluster.ResultSet'>
    for row in rows:
        print('{}'.format(row))

    # Par defaut, une row est un named_tuple
    # et rows est une liste de named_tuple
    print(TAG + 'Select des pk de quelques lignes, avec gestion explicite de l\'affichage du nom des champs')
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, col_names=tab_pk)
    print('rows type: {}'.format(type(rows))) # => <class 'cassandra.cluster.ResultSet'>
    for row in rows:
        row_p = ['{}: {}'.format(field_name, val) for field_name, val in izip(row._fields, row)]
        print(', '.join(row_p))

    print(TAG + 'Select des colonnes choisies de quelques lignes')
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, col_names=COL_NAMES)
    for row in rows:
        print('{}'.format(row))

    # retour en json : chaque row est une string qui contient un json
    print(TAG + 'Select des pk de quelques lignes, retour en json')
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, tab_pk, get_json=True)
    for num, row in enumerate(rows):
        print('{0:3d} {1:s}'.format(num, row.json))

    # retour en dict: plus performant que named_tuple
    # voir https://rhye.org/post/python-cassandra-namedtuple-performance/
    # explication:
    # un namedtuple est a priori coûteux à créer, voir https://lwn.net/Articles/730915/
    # Dans le driver Cassandra en Python, un namedtuple est créé pour chaque requête.
    # Si bcp de petites requêtes sont crées, bcp de temps est perdu.
    # Par contre, ce temps de création est peu visible sur une requête qui ramène bcp de lignes.
    print(TAG + 'Select des pk de quelques lignes, retour en dict')
    session.row_factory = dict_factory
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, tab_pk)
    for num, row in enumerate(rows):
        print('{0:3d} {1:s}'.format(num, row))

    print(TAG + 'Select des pk de quelques lignes, retour en ordered_dict, 2eme version d\'affichage')
    session.row_factory = ordered_dict_factory
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, tab_pk)
    for num, row in enumerate(rows):
        row_p = ['{}: {}'.format(field_name, row[field_name]) for field_name in row]
        print('{} {}'.format(num, ', '.join(row_p)))

    # retour en named_tuple
    print(TAG + 'Select des pk de quelques lignes, retour en named_tuple')
    session.row_factory = named_tuple_factory
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, tab_pk)
    for num, row in enumerate(rows):
        print('{0:3d} {1:s} {2:s}'.format(num, row.entnum, row.nic))

    # retour en named_tuple et écriture dans un fichier
    print(TAG + 'Select des pk de quelques lignes, retour dans un fichier')
    session.row_factory = named_tuple_factory
    rows = get_some_keys(session, CLUSTER_NAME, TABLE_NAME, tab_pk)
    write_rows_tuples(''.join([TABLE_NAME, '_keys', '.csv']), rows)

    cluster.shutdown()
