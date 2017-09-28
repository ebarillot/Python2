# coding=utf-8

import json
from collections import OrderedDict

__author__ = 'Emmanuel Barillot'
"""
Utilisation de OrderedDict à la place de simples dict
Ca marche très bien et les entrées (clé+valeur) d'un dictionnaire sont bien dans
l'ordre dans lequel ils ont été insérés

"""


class Maclasse1(OrderedDict):

    def __init__(self, dict_name):
        OrderedDict.__init__(self)
        self['dict_name'] = dict_name


class Maclasse2(OrderedDict):

    def __init__(self, dict_name):
        OrderedDict.__init__(self)
        self['dict_name'] = dict_name


class Maclasse3(list):

    def __init__(self):
        list.__init__(self)


maclasse1 = Maclasse1("dict_1")
maclasse1['info 1'] = 11
maclasse2 = Maclasse2("dict_2")
maclasse2['info 2'] = 12
maclasse1['info 1'] = maclasse2
maclasse3 = Maclasse3()
maclasse3 += [1,2,3]
maclasse1['list 3'] = maclasse3

print(maclasse1)

print(json.dumps(maclasse1, indent=2, separators=(',', ': ')))
