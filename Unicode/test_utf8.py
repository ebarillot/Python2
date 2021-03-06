﻿# -*- coding: utf-8 -*-

# Bases:
# - str et unicode sont des types, pas des encodages
# - en Python2 une str est une suite de bytes et encodée en ascii par defaut
# - en Python3 une str est unicode et est encodée en utf-8 par defaut
# - Deux fonctions essentielles:
#       - s.decode(encodage):  str -> unicode
#           transforme une str en une variable de type unicode en mémoire en décodant les bytes de la str en fonction
#           de l'encodage indiqué
#       - u.encode(encodage):  unicode -> str
#           transforme une variable de type unicode en mémoire en une chaine de caractères encodée
#           avec l'encodage indiqué
#

# u  = "réponse déjà préparée en euros (€)"
# uu = u.decode('utf8')
uu  = u"réponse déjà préparée en euros (€) : \/ ' ` ~ # ö ô"
print("uu (%%): %s" % uu)
# print("uu (utf8): {}".format(uu.encode('utf8')))
# print("uu (cp1252): {}".format(uu.encode('cp1252')))
# print("uu (iso-8859-15): {}".format(uu.encode('iso-8859-15')))

# encodages_a_tester = ['utf8', 'cp1252', 'iso-8859-15', 'iso-8859-1']
encodages_a_tester = ['utf8', 'cp1252', 'iso-8859-15']

for encoding in encodages_a_tester:
    print("uu ({}): {}".format(encoding, uu.encode(encoding)))
    output_file = 'toto_' + encoding + '.txt'
    with open(output_file,mode='w') as f:
        f.write(uu.encode(encoding))

print ("Reading encoded files ...")

for encoding in encodages_a_tester:
    input_file = 'toto_' + encoding + '.txt'
    with open(input_file,mode='r') as f:
        uu = f.read().decode(encoding)
    print("uu ({}): {}".format(encoding, uu.encode('utf8')))


# convertion d'un utf8 en 'iso-8859-15'
with open('toto_utf8.txt','r') as fin, open('toto_utf8_TO_iso-8859-15.txt','w') as fout:
    for line in fin:
        fout.write(line.decode('utf8').encode('iso-8859-15'))
