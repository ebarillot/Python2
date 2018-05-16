# coding=utf-8

from __future__ import print_function, unicode_literals
import codecs
import os
from collections import namedtuple

# encoding des fichiers
UTF8_ENCODING = r'utf-8'
iso_8859_15_ENCODING = r'iso-8859-15'
DEFAULT_DATA_ENCODING = iso_8859_15_ENCODING

fields = ['entnum', 'nic']
Row = namedtuple('Row', fields)
Row._fields
rows = [Row('775995798', '00011'),
        Row('301317665', '00026'),
        Row('340082932', '00013'),
        Row('508697323', '00014'),
        Row('345349948', '00017')
        ]

print('Working DIR: {}'.format(os.getcwd()))
print('  -> basename(Working DIR): {}'.format(os.path.basename(os.getcwd())))
PATH_ROOT = os.getcwd()
if os.path.basename(os.getcwd()) != 'Unicode':
    os.chdir(PATH_ROOT)

with codecs.open(''.join(['output', '.csv']), 'w', encoding=iso_8859_15_ENCODING) as f:
    for row in rows:
        # print('{};{}'.format(row.entnum, row.nic), file=f)
        f.write('{};{}\n'.format(row.entnum, row.nic))
