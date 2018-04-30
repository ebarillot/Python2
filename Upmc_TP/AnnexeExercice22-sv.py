# -*- coding: utf-8 -*-
#TELECHARGEMENT ET SAUVEGARDE DES DONNEES
def telecharge_et_sauve(nom_de_fichier):
        """
        ENTREE :
        nom_de_fichier, chaine de caracteres : nom de fichier a choisir par l'utilisateur
        SORTIE :
        telechargement des donnees et sauvegarde des donnees dans le fichier nomme nom_de_fichier
        """
        import datetime
        import os
        import urllib
        code='AI.PA'
        year=datetime.date(2015,1,1)-datetime.date(2014,1,1)
        today=datetime.date.today()
        lyear=today - year
        if os.path.exists(nom_de_fichier):
                print "Le fichier ",nom_de_fichier," existe deja"
                return
        else:
                root = "http://real-chart.finance.yahoo.com/table.csv?s=%s&a=%02d&b=%d&c=%d" \
                        "&d=%02d&e=%d&f=%d&g=d&ignore=.csv" % \
                (code, lyear.month-1, lyear.day, lyear.year, today.month-1, today.day, today.year)
                urllib.urlretrieve(root,nom_de_fichier)
                print "Le fichier ",nom_de_fichier," est ecrit"
                return

#EXTRACTION DES DONNEES ET CREATION DE TABLEAUX NUMPY
import numpy as np
import matplotlib.dates as md
date_d,open_d,high_d,low_d,close_d,volume_d=np.loadtxt(nom_de_fichier,delimiter=',',\
converters={0:md.datestr2num},usecols=[0,1,2,3,4,5],skiprows=1,unpack=True)


#EXEMPLE DE GRAPHIQUE
import pylab
size=(800,400)
maxl=len(date_d)
index=pylab.arange(maxl)
#ouverture d'une fenetre graphique
fig=pylab.figure(figsize=(size[0]/100, size[1]/100)) 
#construction du graphique
for i in range(0,maxl):
        pylab.plot([i, i],[0,volume_d[i]],linewidth = 2.0,color="black")
#ajout des legendes
pylab.title("choisir un titre approprie")
pylab.xlabel("abscisses ?")
pylab.ylabel("ordonnees ?")
xlabels=["" for i in index]
for i in range (0,maxl,maxl/20):
        jj=maxl-1
        xlabels[i]=md.num2date(date_d[jj-i]).strftime('%Y,%m,%d')
pylab.xticks(index, lab, fontsize ="small",rotation=13)
#pour voir le graphique
pylab.show()
#fermer la fenetre graphique pour pouvoir reprendre la main dans l'editeur de commande

