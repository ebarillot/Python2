#!/usr/bin/python
# -*- coding: utf-8 -*-


import csv

csv.register_dialect('csvdefault', delimiter=';', quoting=csv.QUOTE_NONE, lineterminator='\n')

with open('eggs.csv', 'rb') as f:
    reader = csv.reader(f, 'csvdefault')
    for row in reader:
        print row

for row in csv.reader(['one,two,three']):
    print row

# with open('eggs.csv', 'wb') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=' ',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
#     spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

# with open('eggs.csv', 'rb') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print ', '.join(row)
#

with open('names.csv', 'w') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='csvdefault')

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
