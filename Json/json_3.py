# coding=utf-8

import json
from abc import abstractmethod
from json import JSONEncoder

__author__ = 'Emmanuel Barillot'
"""
Sérialisation avec un sérialiseur particulier qui fait appel à la méthode to_json de chaque objet
qui doit donc l'implémenter.
Ca marche, mais, comme chaque classe ne dérive plus d'un dict ou d'une list, il faut explicitement
implémenter les méthodes __setitem__ et get_item__
"""

# definition d'une interface pour tous les objets qui doivent être sérialisés en Json
class JsonSerializable(object):
    @abstractmethod
    def to_json(self):
        raise NotImplementedError('subclasses must override to_json()!')


class Maclasse1(JsonSerializable):

    def __init__(self, dict_name):
        self._dict_name = dict_name
        self._dict = dict()

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def to_json(self):
        return {self._dict_name: self._dict}


class Maclasse2(JsonSerializable):

    def __init__(self, dict_name):
        self._dict_name = dict_name
        self._dict = dict()

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def to_json(self):
        return {self._dict_name: self._dict}


class JsonSerializer(JSONEncoder):
    """
    Classe pour sérialiser
    """
    def default(self, obj):
        if isinstance(obj, JsonSerializable):
            return obj.to_json()
        JSONEncoder.default(self, obj)


def json_serializer(obj):
    """
    Une simple fonction pour sérialiser qui fait le même travail que la méthode default()
    de la classe JsonSerializer
    """
    if isinstance(obj,JsonSerializable):
        return obj.to_json()
    return TypeError('obj: {} is not JsonSerializable'.format(obj))


maclasse1 = Maclasse1("dict_1")
maclasse1['info 1'] = 11
maclasse2 = Maclasse2("dict_2")
maclasse2['info 2'] = 12
maclasse1['info 1'] = maclasse2
print(maclasse1)

# sérialisation avec la classe
# print(json.dumps(maclasse1, indent=2, separators=(',', ': '), cls=JsonSerializer))

# sérialisation avec la fonction
print(json.dumps(maclasse1, indent=2, separators=(',', ': '), default=json_serializer))
