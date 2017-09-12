#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'MOOC Python'

# exemples d'aplatissement d'une hiérarchies de conteneurs
# tiré du MOOC Python

def aplatir(conteneurs):
    """
    Transforme un conteneur de conteneurs d'éléments en un conteneur d'éléments

    aplatir([[1,2,3],[a,b,c]]) -> [1,2,3,a,b,c]

    :param conteneurs:
    :return:
    """
    return [item for liste in conteneurs for item in liste]


def alternat(c1,c2):
    """
    Retourne une liste constituée d'une alternance entre les éléments des conteneurs 1 et 2

    alternat([1,2,3], [a,b,c]) -> [1,a,2,d,3,c]

    :param c1: conteneur 1
    :param c2: conteneur 2
    :return:
    """
    return aplatir(zip([item for item in c1],[item for item in c2]))

