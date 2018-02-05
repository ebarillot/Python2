# coding=utf-8

import json

__author__ = 'Emmanuel Barillot'
"""
Alternative à la méthode json_4.py

Chaque classe à sérialiser dérive d'une classe standard sérialisable mais on s'arrange pour ajouter 
les champs supplémentaires dans un dictionnaire par exemple, qui sera ainsi facilement sérialisé.

"""


class Maclasse1(dict):

    def __init__(self, dict_name):
        dict.__init__(self)
        self['dict_name'] = dict_name


class Maclasse2(dict):

    def __init__(self, dict_name):
        dict.__init__(self)
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
