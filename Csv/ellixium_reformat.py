# coding=utf-8

# from __future__ import print_function, unicode_literals
import os

__author__ = "Emmanuel Barillot"


import csv

_delimiter = ';'
csv_path     = r"D:\Documents\Projets\work\Stat\2017-09\Ellixium"
csv_file_in  = r"2017-09-Ellixium_ACT.csv"
csv_file_out = r"2017-09-Ellixium_ACT_2.csv"
# csv_file_in  = r"2017-09-Ellixium_ACT_20.csv"
# csv_file_out = r"2017-09-Ellixium_ACT_20_2.csv"

csv.register_dialect('csvdefault', delimiter=_delimiter, quoting=csv.QUOTE_NONE, lineterminator='\r\n')

with open(os.path.join(csv_path,csv_file_in), "rb") as f:
    reader = csv.reader(f, 'csvdefault')
    with open(os.path.join(csv_path,csv_file_out), 'wb') as csvfile:
        for row in reader:
            row[7] = '/'.join([row[7][0:4], row[7][4:6], row[7][6:8]]) if row[7] != '' else ''
            # print(row)
            spamwriter = csv.writer(csvfile, delimiter=_delimiter, quoting=csv.QUOTE_NONE, lineterminator='\n')
            spamwriter.writerow(row)
