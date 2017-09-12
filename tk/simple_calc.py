#!/usr/bin/python
# -*- coding: utf-8 -*-

# Exercice utilisant la bibliothèque graphique Tkinter et le module math

from Tkinter import *
from math import *


# définition de l'action à effectuer si l'utilisateur actionne
# la touche "enter" alors qu'il édite le champ d'entrée :

def evaluer(event):
    chaine.configure(text="Résultat = " + str(eval(entree.get())))


# ----- Programme principal : -----
fenetre = Tk()
entree = Entry(fenetre)
entree.bind("<Return>", evaluer)
chaine = Label(fenetre)
entree.pack()
chaine.pack()

fenetre.mainloop()
