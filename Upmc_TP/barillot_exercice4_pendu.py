# -*- coding: utf-8 -*-

"""
 Le jeu du pendu
"""
from __future__ import unicode_literals
import platform
from random import randrange


minuscules = "abcdefghijklmnopqrstuvwxyz"
mots = ["python", "anaconda", "zozo", "machiavel","algorithme",
        "voiture","abandon","mexicain","maximum","moustache",
        "reduction","pendu","litterature","musique","television"]
max_erreurs = 10

def lire_lettre(propositions):
    """
     Demande une lettre à l'utilisateur en s'assurant qu'elle n'a pas déjà
     été proposée, puis ajoute cette lettre à la liste des lettres déjà
     proposées.

     >>> liste=['a', 'b', 'c']
     >>> lire_lettre(liste)
     Entrez une proposition de lettre : A
     Une seule lettre en minuscule, s'il vous plait.
     Entrez une proposition de lettre : a
     Cette lettre a déjà été proposée.
     Entrez une proposition de lettre : qsdf
     Une seule lettre en minuscule, s'il vous plait.
     Entrez une proposition de lettre : e
     'e'
     >>> print(liste)
     ['a', 'b', 'c', 'e']
    """
    while True:
        lettre = raw_input("Proposition de lettre : ")

        if lettre in propositions:
            print("Cette lettre a déjà été proposée.")
        elif lettre not in minuscules or len(lettre) != 1:
            print("Une seule lettre autorisée en minuscule.")
        else:
            break;

    propositions.append(lettre)
    return lettre

def mot_avec_tirets1(mot, propositions):
    """
     Renvoie un mot dont les lettres inconnues sont remplacées par des tirets
     >>> mot_avec_tirets('voiture', ['v', 'i'])
     'v-i----'
    """
    m = ''
    for lettre in mot:
        if lettre in propositions:
            m = m + lettre
        else:
            m = m + '-'
    return m

def mot_avec_tirets(mot, propositions):
    """
     Renvoie un mot dont les lettres inconnues sont remplacées par des tirets
     >>> mot_avec_tirets('tirets', ['t', 'i'])
     'ti--t-'
    """
#    lettres = [mot[i] for i in range(len(mot))]
#    m = ['-']*len(lettres)
#    m = [lettre for lettre in propositions if lettre == lettres[i]]
    m = ''
    for lettre in mot:
        if lettre in propositions:
            m = m + lettre
        else:
            m = m + '-'
    return m

def partie():
    """
     Joue une partie de pendu
     retourne True si gagné, False si perdu
    """
    erreurs = 0
    mot = mots[randrange(len(mots))]
    propositions = []

    #
    # Boucle d'interrogation de l'utilisateur
    #
    print("Erreurs : {}".format(erreurs))

    while True:
        print("Lettres déjà proposées : {}".format(propositions))
        print("Réponse courante : {}".format(mot_avec_tirets(mot, propositions)))

        lettre = lire_lettre(propositions)

        if lettre in mot:
            if mot_avec_tirets(mot, propositions) == mot:
                print("Gagné ! Le mot était : {}".format(mot))
                print("Nombre d'erreurs: {}".format(erreurs))
                return True
        else:
            erreurs = erreurs + 1
            print("Erreurs : {}".format(erreurs))
            if erreurs >= max_erreurs:
                print("Pendu haut et court ! le mot était : {}".format(mot))
                return False


#############################################################################
# Programme principal
if __name__ == "__main__":
    pltf = platform.python_version()
    if '2.7' in pltf:
        print ("Plateforme python {} OK".format(pltf))
    else:
        print("ATTENTION : ce script a été développé et testé pour python 2.7")
        print("            Il risque de ne pas fonctionner en python {}".format(pltf))

    print("Jeu du pendu")
    parties = 0
    victoires = 0

    while True:
        parties = parties + 1
        if partie():
            victoires = victoires + 1

        while True:
            cont = raw_input("c pour continuer, a pour arreter : ")
            if cont == 'c' or cont == 'a':
                break;

        if cont == 'a':
            break;

    print("Vous avez joué {} partie(s)".format(parties))
    print("Vous en avez gagné {}".format(victoires))
    print("Bye")
