# coding=utf-8

from cassandra.cluster import Cluster


class ClusterInfo(object):
    # TODO: créer un autre constructeur qui utilise une connexion existante
    # mais qui ne la ferme pas à la fin
    def __init__(self, current_name):
        self._current_name = current_name
        _clu = Cluster([current_name])
        _clu.connect()
        self._cm = _clu.metadata
        self._keyspaces_dict    = self._cm.keyspaces
        self._all_hosts         = self._cm.all_hosts()
        self._internal_name     = self._cm.cluster_name
        self._partitioner       = self._cm.partitioner
        _clu.shutdown()
        del _clu

    @property
    def internal_name(self):
        return self._internal_name

    @property
    def all_hosts(self):
        return self._all_hosts

    @property
    def keyspace_names(self):
        return self._keyspaces_dict.keys()

    @property
    def keyspaces_dict(self):
        return self._keyspaces_dict

    @property
    def partitioner(self):
        return self._partitioner

    def get_keyspace_tables(self, keyspace_name):
        return self._keyspaces_dict[keyspace_name].tables.keys()

    def get_tab_columns(self, keyspace_name, table_name):
        return self._keyspaces_dict[keyspace_name].tables[table_name].columns.keys()

    def get_tab_pk(self, keyspace_name, table_name):
        return [k.name for k in self._keyspaces_dict[keyspace_name].tables[table_name].primary_key]

    def get_tab_script(self, keyspace_name, table_name):
        return self._keyspaces_dict[keyspace_name].tables[table_name].export_as_string()

    def get_tab_columns_desc(self, keyspace_name, table_name):
        cols_dict = self._keyspaces_dict[keyspace_name].tables[table_name].columns
        par_key_list = [k.name for k in self._keyspaces_dict[keyspace_name].tables[table_name].partition_key]
        clu_key_list = [k.name for k in self._keyspaces_dict[keyspace_name].tables[table_name].clustering_key]

        def _get_static(is_static):
            return 'static' if is_static else ''

        def _get_reversed(is_reversed):
            return 'reversed' if is_reversed else ''

        def _get_pk(cname):
            if cname in par_key_list:
                rv = 'par_key'
            elif cname in clu_key_list:
                rv = 'clu_key'
            else:
                rv = ''
            return rv

        return [(cname,
                 _get_pk(cname),
                 cols_dict[cname].cql_type,
                 _get_static(cols_dict[cname].is_static),
                 _get_reversed(cols_dict[cname].is_reversed))
                for cname in cols_dict.keys()]

    def get_ks_indexes(self, keyspace_name):
        tab_idx_dict = dict()
        for tab in self.get_keyspace_tables(keyspace_name):
            if self._keyspaces_dict[keyspace_name].tables[tab].indexes:
                tab_idx_dict[tab] = dict()
                for idx in self._keyspaces_dict[keyspace_name].tables[tab].indexes.keys():
                    idx_name = self._keyspaces_dict[keyspace_name].tables[tab].indexes[idx].name
                    idx_kind = self._keyspaces_dict[keyspace_name].tables[tab].indexes[idx].kind
                    idx_options = self._keyspaces_dict[keyspace_name].tables[tab].indexes[idx].index_options
                    tab_idx_dict[tab][idx_name] = dict()
                    tab_idx_dict[tab][idx_name]['kind'] = idx_kind
                    tab_idx_dict[tab][idx_name]['options'] = idx_options
        return tab_idx_dict

    def get_replicas(self, keyspace_name, key):
        return self._cm.get_replicas(keyspace_name, key)

    def print_keyspaces_tables(self):
        for ks in self.keyspace_names:
            print('{}:'.format(ks))
            for tab in self.get_keyspace_tables(ks):
                print('     - {}'.format(tab))

    def print_tab_columns(self, keyspace_name, table_name):
        print('{}.{}'.format(keyspace_name, table_name))
        filler = [' ']*100

        len_max = max(map(len, [col[0] for col in self.get_tab_columns_desc(keyspace_name, table_name)]))
        for num, (cname, pk, ctype, cstatic, creverse) \
                in enumerate(self.get_tab_columns_desc(keyspace_name, table_name)):
            if cstatic == '' and creverse == '':
                print('    {0:2d} {1:s} {2:s} {3:7s} {4:7s}'
                      .format(num + 1, cname, ''.join(filler[:len_max + 2 - len(cname)]), pk, ctype))
            else:
                print('    {0:2d} {1:s} {2:s} {3:s} {4:s} {5:s} ({6:s})'
                      .format(num + 1, cname, ''.join(filler[:len_max + 2 - len(cname)]), pk, ctype, cstatic, creverse))

    def print_ks_indexes(self, keyspace_name):
        tab_idx_dict = self.get_ks_indexes(keyspace_name)
        for tab_name in tab_idx_dict:
            print('table: {}'.format(tab_name))
            for idx_name in tab_idx_dict[tab_name]:
                print('    index: {}'.format(idx_name))
                print('        kind: {}'.format(tab_idx_dict[tab_name][idx_name]['kind']))
                print('        options:')
                for idx_option in tab_idx_dict[tab_name][idx_name]['options']:
                    print('            {}: {}'.format(idx_option, tab_idx_dict[tab_name][idx_name]['options'][idx_option]))


if __name__ == "__main__":
    # tests => à transformer en unittest
    cluInfo = ClusterInfo('tstdar01')
    print('internal_name: {}'.format(cluInfo.internal_name))
    print('all_hosts: {}'.format(cluInfo.all_hosts))
    print('partitioner: {}'.format(cluInfo.partitioner))
    print('keyspace_names: {}'.format(cluInfo.keyspace_names))
    cluInfo.print_keyspaces_tables()
    cluInfo.print_tab_columns('ks_view_search', 'solr_entreprise')
    print(cluInfo.get_tab_script('ks_view_search', 'solr_entreprise'))
    params = ('ks_view_search', '775995798')
    print('replicas of {} in {}: {}'.format(params[0], params[1], cluInfo.get_replicas(params[0], params[1])))
    cluInfo.print_ks_indexes('ks_view_search')
    print(cluInfo.get_tab_pk('ks_view_search', 'solr_entreprise'))
