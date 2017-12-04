# coding=utf-8
from __future__ import print_function, unicode_literals
from typing import List, Any, Dict, Callable, FrozenSet

import pysvn
import pprint


__author__ = "Emmanuel Barillot"


client = pysvn.Client()

# pprint.pprint(client.list('http://frdevsvn01/CS_SVN/CS-Iris/userdev/projets/bfrance'))
# pprint.pprint(client.info2('http://frdevsvn01/CS_SVN/CS-Iris/userdev/projets/bfrance/trunk/c/chgInfnegsRemet'))
# pprint.pprint(client.ls('http://frdevsvn01/CS_SVN/CS-Iris/userdev/projets/bfrance/trunk/c'))

SEP = '/'
svn_root_bdd_schemas = 'http://frdevsvn01/CS_SVN/CS-BDD/schemas'
un_schema = 'FRA2'
tags_path = 'tags'
entry_list = client.ls(svn_root_bdd_schemas + SEP + un_schema + SEP + tags_path)
for entry in entry_list:
    print(entry)

print(len(entry_list))

