#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Emmanuel Barillot'

from itertools import chain
import datetime

tabnames = {'JUGEMENT':('JUGHISM')}
tabkeys = {   'JUGEMENT'    :[('JUGENTNUM','JUGENTNUMTYP','JUGSEQ')]
            , 'JUGHISM'     :[('JUGHISENTNUM','JUGHISENTNUMTYP','JUGHISJUGSEQ')]
           }
columns = {'JUGEMENT': ['JUGENTNUMTYP', 'JUGENTNUM', 'JUGSEQ', 'JUGTYPJUGCOD', 'JUGDURMOI', 'JUGCOM', 'JUGDATLIE', 'JUGLIEPRE', 'JUGSUP', 'JUGHISDATEFF', 'JUGHISORICOD', 'JUGHISSUPPORTCOD', 'JUGHISNUMSUPPORT', 'JUGHISNUMINF', 'JUGHISEFFPRE', 'JUGHISPOIDATEFF', 'JUGHISDATPUB', 'JUGHISPUBPRE', 'JUGGREFFECOD', 'JUGDATRECEPJAL', 'JUGINCRJAL', 'JUGNUMTRTJAL', 'JUGTYPCLEJAL']}

for tabname_1 in tabnames.iterkeys():
    print(tabname_1)

row_1 = (0, '428278394', 7638450, 44, None, None, None, None, 'SUP', datetime.datetime(2015, 12, 7, 0, 0), 'GREF', 'RIEN', None, None, 'J', 'EFF', None, None, 4601, None, None, None, None)
row_1_key=[row_1[columns[tabname_1].index(keylib)] for keylib in list(chain.from_iterable(tabkeys[tabname_1]))]
print(row_1_key)
