#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Emmanuel Barillot'

# def flatten(l, ltypes=(list, tuple)):
#     ltype = type(l)
#     l = list(l)
#     i = 0
#     while i < len(l):
#         while isinstance(l[i], ltypes):
#             if not l[i]:
#                 l.pop(i)
#                 i -= 1
#                 break
#             else:
#                 l[i:i + 1] = l[i]
#         i += 1
#     return ltype(l)
#
#
# def flatten(bla):
#     output = []
#     for item in bla:
#         output += flatten(item) if hasattr (item, "__iter__") or hasattr (item, "__len__") else [item]
#     return output


def flatten(list_of_tuple):
    """
    Pour aplatir une liste de liste ou une liste de tuples dans une liste de valeurs simples
    :param list_of_tuple: la liste de tuples à aplatir
    :return: la liste aplatie
    """
    from itertools import chain
    return list(chain.from_iterable(list_of_tuple))


def flattenR(lst):
    """
    Pour aplatir une liste d'objets iterables imbriqués, de profondeur arbitraire
    :param lst: la liste d'objets imbriqués
    :return: la liste aplatie
    """
    result = []
    for element in lst:
        if hasattr(element, '__iter__'):
            result.extend(flattenR(element))
        else:
            result.append(element)
    return result

print (flatten([(12.2817, 12.2817), (0, 0), (8.52, 8.52)]))
print (flattenR([(12.2817, 12.2817), (('a',['b','c']), 0), (8.52, 8.52)]))
