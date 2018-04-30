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


if __name__=="__main__":
    fichier_air_liquide=r"D:\Emmanuel\Formations\Upmc\2016\L3_Cours\3M100_Python\TP\airliquide.csv"
    telecharge_et_sauve(fichier_air_liquide)
