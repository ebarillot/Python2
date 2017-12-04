# coding=utf-8
from __future__ import print_function, unicode_literals
from typing import List, Any, Dict, Callable, FrozenSet

import svn.remote

__author__ = "Emmanuel Barillot"


r = svn.remote.RemoteClient('http://frdevsvn01/CS_SVN')
# info = r.info(rel_path='CS-Iris/userdev/projets/bfrance')
# print(info)

for truc in r.list(rel_path='CS-Iris/userdev/projets/bfrance'):
    print(truc)

