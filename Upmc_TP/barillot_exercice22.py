# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np
import matplotlib.dates as md
import pylab as plt
import math as m
import platform


jours_semaine = {0:"lundi",1:"mardi",2:"mercredi",3:"jeudi",4:"vendredi"}

def lire_donnes(nom_fichier):
    """
    Lecture du fichier <nom_fichier> et construction
    des tableaux utiles
    """
    #EXTRACTION DES DONNEES ET CREATION DE TABLEAUX NUMPY
    date_d, open_d, high_d, low_d, close_d, volume_d = np.loadtxt(
        nom_de_fichier, \
        delimiter  = ',', \
        converters = {0:md.datestr2num}, \
        usecols    = [0,1,2,3,4,5], \
        skiprows   = 1, \
        unpack     = True)
    maxl = len(date_d)
    return maxl, date_d, open_d, high_d, low_d, close_d, volume_d


def reord(date_d, open_d, high_d, low_d, close_d, volume_d):
    """
    Réordonne les valeurs dans l'ordre croissant des dates
    date_d : le tableau des dates
    open_d, high_d, low_d, close_d, volume_d : les tableaux de valeurs
    """
    import operator
    ind = range(len(date_d))
    dt = dict(zip(ind,date_d))
    ds = sorted(dt.iteritems(), key=operator.itemgetter(1))
    date_out, open_out, high_out, low_out, close_out, volume_out = \
        [], [], [], [], [], []
    for d in ds:
        date_out.append(d[1])
        open_out.append(open_d[d[0]])
        high_out.append(high_d[d[0]])
        low_out.append(low_d[d[0]])
        close_out.append(close_d[d[0]])
        volume_out.append(volume_d[d[0]])
    return date_out, open_out, high_out, low_out, close_out, volume_out


def lesplus(tb):
    """
    Cours le plus élevé et le plus bas de l'année
    """
    return min(tb), max(tb)


def moy(tb):
    """
    Moyenne des valeurs du tableau tb
    """
    mo = sum(tb)/len(tb)
    return mo


def moyp(tb,vo):
    """
    Moyenne pondérée des valeurs
    tb : tableau des valeurs
    vo : tableau des volumes
    Les tableaux doivent avoir la même longueur
    """
    pt = sum(vo)
    return reduce(lambda x,y:x+y,map(lambda x:(x[0]*x[1])/pt, zip(tb,vo)))


def med(tb):
    """
    Mediane
    tb : tableau des valeurs
    """
    # la fonction ceil n'apporte rien dans ce contexte,
    # car sorted(tb)[len(tb)/2] marche très bien
    # mais puisqu'il faut l'utiliser ...
    return sorted(tb)[int(m.ceil(len(tb)/2))]


def moydiff(ta,tb):
    """
    Retourne la moyenne de la différence entre une valeur de ta et la valeur
    de même indice dans tb
    ta : 1er tableau de valeurs
    tb : 2eme tableau de valeurs
    """
    return moy(map(lambda x:x[0]-x[1], zip(ta,tb)))


def ecart(tb):
    """
    Retourne l'écart type
    de même indice dans tb
    tb : tableau de valeurs
    """
    mo = moy(tb)
    return m.sqrt(sum(map(lambda x:(x-mo)**2, tb))/(len(tb)-1))


def jourplus(tb,dt):
    """
    Retourne le jour de la semaine où le cours de cloture
    est le plus élevé en moyenne sur une année
    tb : tableau de valeurs (ordonné selon les dates)
    dt : le tableau des dates ordonnées (croissantes)
    """
    # détecter les débuts de semaines
    # une semaine = une suite contigue de 5 jours
    jsem = []
    i = 0
    while i+4 < len(dt):
        #print ("i={} {},{},{},{},{}".format(i,dt[i],dt[i+1],dt[i+2],dt[i+3],dt[i+4]))
        if  int(dt[i+1]-dt[i])   == 1 \
        and int(dt[i+2]-dt[i+1]) == 1 \
        and int(dt[i+3]-dt[i+2]) == 1 \
        and int(dt[i+4]-dt[i+3]) == 1:
            # détecter le jour de la semaine où le cours est le plus élevé
            tbsem = [tb[i+it] for it in range(5)]
            maxsem = max(tbsem)
            jmaxsem = [ind for ind, val in enumerate(tbsem) if val == maxsem]
            #print (jmaxsem)
            jsem.append(jmaxsem)
            i = i+5
        else:
            i = i+1
    #print ("Nb semaines = {}".format(len(jsem)))
    #print (jsem)
    # jsem est une liste de listes, qu'on concatène avant de calculer la moyenne
    return moy(sum(jsem,[]))


def set_day_color(close_d):
    """
    Calcul de la couleur de chaque jour
    en fonction du cours à la cloture
    """
    day_color = ["black"]
    for i in range(1,len(close_d)):
        if close_d[i] > close_d[i-1]:
            day_color.append("green")
        else:
            day_color.append("red")
    return day_color


def graphique(volume_d, close_d):
    """
    Exemple de graphique
    """
    maxl = len(volume_d)
    size  = (1000,500)
    index = plt.arange(maxl)

    #ouverture d'une fenetre graphique
    #fig = plt.figure(figsize=(size[0]/100, size[1]/100))
    fig1, ax1 = plt.subplots(figsize=(size[0]/100, size[1]/100))

    # calcul de la couleur de chaque jour
    day_color = set_day_color(close_d)

    #construction du graphique des volumes
    for i in range(0,maxl):
        ax1.plot([i, i],[0,volume_d[i]],linewidth = 2.0,color=day_color[i])
    #ajout des legendes
    plt.title("Action Air Liquide")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    xlabels = ["" for i in index]
    for i in range (0,maxl,maxl/20):
        xlabels[i] = md.num2date(date_d[i]).strftime('%Y,%m,%d')
    plt.xticks(index, xlabels, fontsize ="small",rotation=20)

    #construction du graphique du cours de cloture
    ax2 = ax1.twinx()
    plt.ylim(min(close_d)*0.8, max(close_d)*1.1)
    ax2.plot(index,np.array(close_d),linewidth = 1.0,color="blue")
    for tl in ax2.get_yticklabels():
        tl.set_color('b')
    plt.ylabel("Cours en euros",color="blue")

    #pour voir le graphique
    plt.show()
    #fermer la fenetre graphique pour pouvoir reprendre la main dans l'editeur de commande
    return


#####################
# programme principal
#####################
if __name__=="__main__":
    
    pltf = platform.python_version()
    if '2.7' in pltf:
        print ("Plateforme python {} OK".format(pltf))
    else:
        print("ATTENTION : ce script a été développé et testé pour python 2.7")
        print("            Il risque de ne pas fonctionner en python {}".format(pltf))

    # lecture du fichier des données
    nom_de_fichier="airliquide.csv"
    maxl, date_r, open_r, high_r, low_r, close_r, volume_r = lire_donnes(nom_de_fichier)
    # données réordonnées suivant des dates croissantes
    date_d, open_d, high_d, low_d, close_d, volume_d \
        = reord(date_r, open_r, high_r, low_r, close_r, volume_r)
    

    # calcul de la moyenne
    bas, haut = lesplus(close_d)
    print ("Cours le plus bas = {} \nCours le plus élevé = {}".format(bas,haut))
    
    # calcul de la moyenne
    print ("moyenne = {}".format(moy(close_d)))
    
    # calcul de la moyenne pondérée
    print ("moyenne pondérée = {}".format(moyp(close_d,volume_d)))

    # calcul de la mediane
    print ("mediane = {}   np.median: {}".format(med(close_d),np.median(close_d)))

    # différence moyenne avec le max de la journée
    print ("différence moyenne avec le max de la journée = {}".format(moydiff(close_d,high_d)))
    print ("différence moyenne avec le min de la journée = {}".format(moydiff(close_d,low_d)))
    
    # calcul de l'écart type
    print ("écart type = {}".format(ecart(close_d)))

    # calcul de l'écart type
    print ("jour de la semaine où le cours est le plus élevé = {}"\
        .format(jours_semaine[jourplus(close_d,date_d)]))

    graphique(volume_d, close_d)
    
