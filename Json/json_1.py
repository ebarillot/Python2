# coding=utf-8

from __future__ import print_function, unicode_literals
import json
from EBCommons.json_helper import DictToObj

__author__ = "Emmanuel Barillot"

if False:
    # parsing d'un buffer et affichage de la hiérarchie de conteneurs obtenus
    dict_json = json.loads(r'''{"compteurs autorisés": {"Lignes fichier": 1, "Fichier en entrée": 2}}''')
    print('json: ' + str(dict_json))
    print('json: ' + str(dict_json["compteurs autorisés"]))
    print('json: ' + str(dict_json["compteurs autorisés"]["Lignes fichier"]))


class CompteursDictClass(object):
    def __init__(self, compteurs_dict):
        self._compteurs_dict = compteurs_dict

    def get_data(self, compteurs_name):
        return self._compteurs_dict[compteurs_name] if compteurs_name in self._compteurs_dict else None

    def get_dict(self):
        return self._compteurs_dict


class CompteursGroupClass(object):
    def __init__(self, group_dict):
        self._groups = {}
        for group_name, compteurs_dict in group_dict.iteritems():
            self._groups[group_name] = CompteursDictClass(compteurs_dict)

    def get_groups(self):
        #  type: (unicode) -> dict
        return self._groups

    def get_compteurs_dict(self, group_name):
        #  type: (unicode) -> CompteursDictClass
        return self._groups[group_name] if group_name in self._groups else None


if True:
# if False:
    # parsing d'un buffer AVEC utilisation d'un objet_hook dans json.load()

    # Map set of keys to classes: tous les objets json pointés par les clés suivantes
    # seront transformées en objet Python par le constructeur qui leur est associé dans le mapping_sugnature
    json_keys_to_CompteursGroup = {u"compteurs autorisés", u"compteurs correspondances"}
    mapping_signature = {frozenset(json_keys_to_CompteursGroup): CompteursGroupClass}

    mapping_json = DictToObj(mapping_signature)

    with open('compteurs_names.json') as f:
        compteurs_group = json.load(f, encoding='utf-8', object_hook=mapping_json.dict_to_obj)
        for group_name, compteur_dict in compteurs_group.get_groups().iteritems():
            print('Groupe de compteurs: ' + group_name)
            for compteur_name, compteur_lib in compteur_dict.get_dict().iteritems():
                print('  {} : {}'.format(compteur_name, compteur_lib))


# if True:
if False:
    # parsing d'un buffer json SANS utilisation d'un objet_hook dans json.load()
    # mais utilisation d'une fonction générique de construction d'objets (instances)
    #  en fonction des éléments rencontrés dans le json
    #  nécessite un mapping entre clé json et classe à instancier

    # Map set of keys to classes
    json_keys_to_CompteursNames = {u"compteurs autorisés", u"compteurs correspondances"}
    mapping = {frozenset(json_keys_to_CompteursNames): CompteursDictClass}

    def as_CompteursNames(dct):
        compteurs_dict = {}
        if isinstance(dct, dict):
            for key in dct.keys():
                for mapping_key in mapping.keys():
                    if frozenset([key]).issubset(mapping_key):
                        compteurs_dict[key] = mapping[mapping_key]((dct[key]))
        return compteurs_dict

    with open('compteurs_names.json') as f:
        dict_json = json.load(f, encoding='UTF-8')
        print('object: ' + str(dict_json))
        compteurs = as_CompteursNames(dict_json)
        for d1 in compteurs.keys():
            print('Liste de compteurs: {}'.format(d1))
            for (key, value) in compteurs[d1].get_dict().iteritems():
                print('  {}: {}'.format(key, value))

