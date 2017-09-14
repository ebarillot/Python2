# coding=utf-8

from __future__ import print_function, unicode_literals
import json

__author__ = "https://stackoverflow.com/questions/27038259/how-to-load-json-data-into-nested-classes"


class AddressClass:
    # The parameters to init needs to be the same as the json keys
    def __init__(self, House_Number, Street_Number, State):
        self.house_number = House_Number
        self.street_number = Street_Number
        self.state = State


class EmployeeClass:
    # Same here
    def __init__(self, Name, Address):
        self.name    = Name
        self.address = Address


# Map keys to classes
# C'est en quelque sorte la signature de chaque constructeur qui sert de clé
mapping = {frozenset(('House_Number',
                      'Street_Number',
                      'State'))  : AddressClass,
           frozenset(('Name',
                      'Address')): EmployeeClass}

j = '''
{
    "Name": "John",
    "Address": {
        "House_Number" : 2,
        "State"        : "MA",
        "Street_Number": 13
    }
}
'''

def class_mapper(d):
    print("mapped dict: {}".format(d))
    print("  frozenset: {}".format(frozenset(d.keys())))
    print("  mapping: {}".format(mapping[frozenset(d.keys())]))
    return mapping[frozenset(d.keys())](**d)


def class_mapper_2(d):
    '''
    Fonction de mapping qui accepte de traiter une liste partielle de paramètres pour trouver la signature
    du constructeur et donc la classe à utiliser
    Attention à gérer les paramètres facultatifs dans l'implémentation du constructeur __init__()
    :param d: le dict Python construit par le parser à partir de ce qu'il a trouvé dans le json
    :return: un objet créé par le constructeur de la classe invoquée
    '''
    print("mapped dict: {}".format(d))
    print("  frozenset: {}".format(frozenset(d.keys())))
    print("  mapping: {}".format(mapping[frozenset(d.keys())]))
    for keys, cls in mapping.items():
        if keys.issuperset(d.keys()):
            return cls(**d)
    else:
        # Raise exception instead of silently returning None
        raise ValueError('Unable to find a matching class for object: {!s}'.format(d))


employee = json.loads(j, object_hook=class_mapper_2)
print(employee.name,
      employee.address.house_number,
      employee.address.street_number,
      employee.address.state)
