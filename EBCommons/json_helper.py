# coding=utf-8
# module EBCommons

from __future__ import print_function, unicode_literals
from typing import List, Any, Dict, Callable, FrozenSet

__author__ = "Emmanuel Barillot"


class DictToObj(object):
    """
    Objet-outil qui permet de transformer un dict ou plusieurs types de dict en un objet à
    partir d'un mapping entre un ensemble de clés de dictionnaires et un nom de classe (constructeur en fait)
    """
    def __init__(self, json_keys_mapping):
        # type: (Dict[FrozenSet[unicode], Callable]) -> DictToObj
        """
        :param json_keys_mapping: attention à la structure un peu complexe; ce dictionnaire permet
        d'associer plusieurs clés à une classe (à son constructeur en fait).
        Pour avoir plusieurs clés, l'astuce consiste à les regrouper au sein d'un frozenset, qui est hashable
        car immutable. Un set ne convient pas car mutable.
        """
        self._json_keys_mapping = json_keys_mapping

    def dict_to_obj(self, dct):
        # type: (Dict) -> Any
        """
        Transforme un dict Python en un objet: le constructeur de l'objet est déterminé en fonction
        de la liste de ses paramètres.
        Lors de la construction de l'objet DictToObjClass, chaque clé du dictionnaire à transformer est associée
        à une classe (donc à son constructeur).
        Cette méthode transforme donc chaque valeur d'une entrée du dictionnaire en un objet
        construit avec le constructeur associé à la même clé dans le json_keys_mapping.
        :param dct: dictionnaire Python
        :return: un objet ou un dict intact si pas de quoi transformer
        """
        if isinstance(dct, dict):
            for keys, cls in self._json_keys_mapping.items():
                if keys.issuperset(dct.keys()):
                    return cls(dct)
            else:   # le else est bien lié au for et n'est exécuté que si la boucle se termine
                return dct  # retourne inchangé dans l'arbre json


#  pour un test de la classe DictToObj, voir ../Json/json_1.py


def json_navigate(jsobj, jspath):
    # type: (Any, List) -> Any
    """
    Navigation dans un objet json ou par extension dans tout objet Python qui une
    hiérarchie de dictionnaires et de listes, car selon la doc officielle
    https://docs.python.org/2.7/library/json.html#json-to-py-table
    on a les conversions suivantes:
            JSON       Python
            objet ->   dict
            array ->   list

    :param jsobj: l'objet json tel que retourné par json.load()
    :param jspath: le chemin vers la valeur qu'on souhaite obtenir.
    Le chemin est fourni sous la forme d'une liste de noms (clé d'un dictionnaire json)
     ou indices (d'un tableau json).
    :return: objet json trouvé au bout du chemin.
    """
    if not jspath:
        return jsobj
    head, tail = jspath[0], jspath[1:]
    return json_navigate(jsobj[int(head) if head.isdigit() else head], tail)
