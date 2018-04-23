# coding=utf-8

from __future__ import unicode_literals

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if os.path.basename(os.getcwd()) != 'Statnum':
    os.chdir('./Statnum')

# https://www.data.gouv.fr/fr/datasets/data-insee-sur-les-communes/
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Feuil1', converters={u'Urbanité Ruralité': unicode})
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Feuil1', dtype={u'Urbanité Ruralité': str})
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Feuil1')
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Table Décisionnelle INSEE')
dataset = pd.read_excel('TP/MDB-INSEE-V2.xls', sheet_name='Table Décisionnelle INSEE')
df = pd.DataFrame(dataset)
df.columns.values
df['Urbanité Ruralité'].dtype
# df['Urbanité Ruralité'].astype(unicode)

print('-- Shape: {}'.format(df.shape))
print('-- Infos:')
df.info()
print('-- Infos END --')

df.describe()
df.head(5)

#  les noms de colonnes
df.columns.values
df.dtypes
print(df.dtypes)

df1 = pd.DataFrame(df, columns=['CODGEO',
                                'Orientation Economique',
                                'Urbanité Ruralité',
                                'LIBGEO',
                                'REG',
                                'DEP',
                                'Nb Omnipraticiens BV',
                                'Nb Infirmiers Libéraux BV',
                                'Nb dentistes Libéraux BV',
                                'Nb pharmaciens Libéraux BV',
                                'Population',
                                'Evolution Pop %',
                                'Nb Ménages',
                                'Nb Résidences Principales',
                                'Nb propriétaire',
                                'Nb Logement',
                                'Taux Propriété',
                                'Nb Résidences Secondaires',
                                'Nb Log Vacants',
                                'Nb Occupants Résidence Principale',
                                'Nb Femme',
                                'Nb Homme',
                                'Nb Mineurs',
                                'Nb Majeurs',
                                'Nb Etudiants',
                                'Nb Atifs',
                                'Nb Actifs Salariés',
                                'Nb Actifs Non Salariés',
                                'Taux étudiants',
                                'Dynamique Démographique BV',
                                'Environnement Démographique',
                                'Fidélité',
                                'Nb Entreprises Secteur Services',
                                'Nb Entreprises Secteur Commerce',
                                'Nb Entreprises Secteur Construction',
                                'Nb Entreprises Secteur Industrie',
                                'Nb Création Enteprises',
                                'Nb Création Industrielles',
                                'Nb Création Construction',
                                'Nb Création Commerces',
                                'Nb Création Services',
                                'Moyenne Revenus Fiscaux Départementaux',
                                'Dep Moyenne Salaires Horaires',
                                'Dep Moyenne Salaires Cadre Horaires',
                                'Dep Moyenne Salaires Prof Intermédiaire Horaires',
                                'Dep Moyenne Salaires Employé Horaires',
                                'Dep Moyenne Salaires Ouvrié Horaires'
                                ])
df1[u'Urbanité Ruralité']
df1[u'Urbanité Ruralité'].dtype
df1.head(5)
df1.describe()
df1.info(verbose=True)

df1['Nb praticiens'] = df1['Nb Omnipraticiens BV'] \
                       + df1['Nb Infirmiers Libéraux BV'] \
                       + df1['Nb dentistes Libéraux BV'] \
                       + df1['Nb pharmaciens Libéraux BV']
df1[['Nb Atifs', 'Population','Nb praticiens','Nb propriétaire']].corr(method='pearson')


df2 = pd.DataFrame(df, columns=['CODGEO',
                                'Orientation Economique',
                                'Urbanité Ruralité',
                                'LIBGEO',
                                'REG',
                                'DEP'
                                'Nb Omnipraticiens BV',
                                'Nb Infirmiers Libéraux BV',
                                'Nb dentistes Libéraux BV',
                                'Nb pharmaciens Libéraux BV',
                                'Population'
                                ])
df2.head(5)
df2.describe()
df1.info(verbose=True)
df2['Urbanité Ruralité']

df3 = pd.DataFrame(df, columns=['CODGEO',
                                'Orientation Economique',
                                'Urbanité Ruralité',
                                'LIBGEO',
                                'REG',
                                'DEP'])
df3['Nb praticiens'] = df['Nb Omnipraticiens BV'] \
                       + df['Nb Infirmiers Libéraux BV'] \
                       + df['Nb dentistes Libéraux BV'] \
                       + df['Nb pharmaciens Libéraux BV']
df3['Population'] = df['Population']
df3['Nb Atifs'] = df['Nb Atifs']
df3[['Nb praticiens', 'Population']].corr(method='pearson')
df3[['Nb Atifs', 'Population','Nb praticiens']].corr(method='pearson')
