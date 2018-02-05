# coding=utf-8

import json
from abc import abstractmethod
from json import JSONEncoder

__author__ = 'Emmanuel Barillot'
"""
Utilisation de la sérialisation par défaut d'un json: conversion simple des dict() et list()
Pour que ça marche sur une classe personnelle, il suffit de la faire dériver d'un dict() ou d'un type déjà géré
dans la conversion.
"""

# petit test pour jouer avec la lecture et l'écriture d'un json dans un fichier
if False:
    # lecture
    with open('simple_file.json', 'r') as f:
        json_obj = json.load(f)

    print(json_obj)

    # ecriture
    with open('simple_file_out.json', 'w') as f:
        json.dump(json_obj, f, indent=2, separators=(',', ': '))


class Maclasse1(dict):

    def __init__(self, dict_name):
        dict.__init__(self)
        # ou super(self.__class__, self).__init__()
        # ou super(Maclasse1, self).__init__()
        self._dict_name = dict_name


class Maclasse2(list):

    def __init__(self, list_name):
        list.__init__(self)
        self._list_name = list_name


maclasse1 = Maclasse1("obj_1")
maclasse1['info 1'] = 11
maclasse2 = Maclasse2("obj_2")
maclasse2 += [0, 10, 20]
maclasse1['info 1'] = maclasse2
print('Print object: {}'.format(maclasse1))

print('Json dump: ' + json.dumps(maclasse1, indent=2, separators=(',', ': ')))

#
# Ca marche mais il manque les noms des objects de type Maclasse1 ou Maclasse2
# car non pris en compte par l'encodeur / serialiseur par defaut
#