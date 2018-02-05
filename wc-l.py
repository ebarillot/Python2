# -*- coding: utf-8 -*-

# FONCTION RENVOYANT LE NOMBRE DE LIGNES D'UN FICHIER TEXTE
def countLigne(fichier):
    Liste=file(fichier,'r')
    i=1
    Ligne=Liste.readline()
    # "Tant que la ligne n'est pas égale à "" "
    # ==> tant qu'on est pas arrivé à la fin
    while Ligne!="":
      #on lit une ligne
      Ligne=Liste.readline()
      #on ajoute 1 à notre compteur
      i+=1
    # on retourne le compteur
    return i
    # on note que sous windows le symbole "\" doit etre doublé quand il y a certains caractères

countLigne("toto")
