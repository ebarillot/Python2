# coding=utf-8

import json
from abc import abstractmethod
from json import JSONEncoder

__author__ = 'Emmanuel Barillot'
"""
Sérialisation avec un sérialiseur particulier qui fait appel à la méthode to_json de chaque objet
qui doit donc l'implémenter.
Chaque classe à sérialiser dérive d'un dict et de l'interface JsonSerializable.
Cependant, la fonction json.dump() ne passe même pas par le sérialiseur.
Il semble que la sérialisation se fasse avec les méthodes de la classe dict.
Comment forcer le passage par les fonctions to_json de chaque instance, tout en conservant l'héritage de dict ?

"""


# definition d'une interface pour tous les objets qui doivent être sérialisés en Json
class JsonSerializable(object):
    @abstractmethod
    def to_json(self):
        raise NotImplementedError('subclasses must override to_json()!')


class Maclasse1(dict, JsonSerializable):

    def __init__(self, dict_name):
        dict.__init__(self)
        self._dict_name = dict_name

    def to_json(self):
        return {self._dict_name: self}


class Maclasse2(dict, JsonSerializable):

    def __init__(self, dict_name):
        dict.__init__(self)
        self._dict_name = dict_name

    def to_json(self):
        return {self._dict_name: self}


class JsonSerializer(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JsonSerializable):
            return obj.to_json()
        JSONEncoder.default(self, obj)


def json_serializer(obj):
    if isinstance(obj,JsonSerializable):
        return obj.to_json()
    return TypeError('obj: {} is not JsonSerializable'.format(obj))


maclasse1 = Maclasse1("dict_1")
maclasse1['info 1'] = 11
maclasse2 = Maclasse2("dict_2")
maclasse2['info 2'] = 12
maclasse1['info 1'] = maclasse2
print(maclasse1)

print(json.dumps(maclasse1, indent=2, separators=(',', ': '), cls=JsonSerializer))
# print(json.dumps(maclasse1, indent=2, separators=(',', ': '), default=json_serializer))
