# -*- coding: utf-8 -*-

# Différence avec le script test_utf8.py :
from __future__ import unicode_literals

# Remarque les fonctions print() et sys.stdout.write() sont sensibles à
# cet environnement tout utf8.
# Contrairement au premier script, il n'est pas possible de faire un
# print(uu.encode('utf8'))
# Il faut faire un print(uu) simplement.
# Du coup, on peut pas jouer avec l'encodage des caractères sur la sortie standard.

# u  = "réponse déjà préparée en euros (€)"
# uu = u.decode('utf8')
from sys import stdout

uu  = u"réponse déjà préparée en euros (€) : \/ ' ` ~ # ö ô"
print("uu (unicode): %s" % uu)
# print("uu (utf8): {}".format(uu.encode('utf8')))
# print("uu (cp1252): {}".format(uu.encode('cp1252')))
# print("uu (iso-8859-15): {}".format(uu.encode('iso-8859-15')))

# encodages_a_tester = ['utf8', 'cp1252', 'iso-8859-15', 'iso-8859-1']
encodages_a_tester = ['utf8', 'cp1252', 'iso-8859-15']

# on crée un fichier de sortie par encodage à tester
for encoding in encodages_a_tester:
    output_file = 'toto_' + encoding + '.txt'
    with open(output_file,mode='w') as f:
        f.write(uu.encode(encoding))    # on encode vers l'encodage voulu pour le fichier de sortie

print ("Reading encoded files ...")

# on relit les fichiers dans les encodages à tester
for encoding in encodages_a_tester:
    input_file = 'toto_' + encoding + '.txt'
    with open(input_file,mode='r') as f:
        uu = f.read().decode(encoding)
    print("uu (from {}): {}".format(encoding, uu))


# convertion d'un fichier en utf8 en 'iso-8859-15'
with open('toto_utf8.txt','r') as fin, open('toto_utf8_TO_iso-8859-15.txt','w') as fout:
    for line in fin:
        fout.write(line.decode('utf8').encode('iso-8859-15'))
