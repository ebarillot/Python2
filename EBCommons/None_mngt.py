#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
__author__ = 'Emmanuel Barillot'

#
# Fonctions de gestion des valeurs None, de façon à les transformer en une valeur qui n'est pas None
#

def floatOrNoneToStr(a_float, a_format):
    """
    Formattage  d'un float qui gère le fait qu'il soit None

    :param a_float: le float à formater
    :param a_format: le format attendu
    :return: le float formaté ou une chaine vide
    """
    return ("" if a_float is None else format(a_float,a_format))


def strOrNone(s):
    """
    Retourne une chaine vide si None

    :param s: la chaine de caractere à tester
    :return: une chaine vide "" ou la chaine non vide
    """
    return ("" if s is None else s)

