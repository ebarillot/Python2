#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Emmanuel Barillot'


# exemple pris ici : http://stackoverflow.com/questions/9001509/how-can-i-sort-a-dictionary-by-key

import collections

my_dict = {'carl': 40,
          'alan': 2,
          'bob': 1,
          'danny': 3}

my_items = my_dict.items()
my_sorted_dict = sorted(my_items, key=lambda t : t[0])
od = collections.OrderedDict(my_sorted_dict)

#od = collections.OrderedDict(sorted(my_dict.items()))

print(">>> mydict:")
for key,val in my_dict.items():
    print("%s: %s" % (key, val))

print("")

print(">>> od:")
for key,val in od.items():
    print("%s: %s" % (key, val))


od2 = collections.OrderedDict((('abc',10),('bcd',2)))
print(">>> od2:")
for key,val in od2.items():
    print("%s: %s" % (key, val))

