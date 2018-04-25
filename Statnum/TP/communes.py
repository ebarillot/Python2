# coding=utf-8

from __future__ import unicode_literals
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if os.path.basename(os.getcwd()) != 'Statnum':
    os.chdir('./Statnum')

# https://www.data.gouv.fr/fr/datasets/data-insee-sur-les-communes/
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Feuil1', converters={u'Urbanité Ruralité': unicode})
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Feuil1', dtype={u'Urbanité Ruralité': str})
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Feuil1')
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Table Décisionnelle INSEE')
regions = pd.read_csv('TP/reg1999.txt', sep='\t', encoding='iso-8859-15')
regions
regions.columns.values
regions.index
regions.reset_index()
regions.reset_index().reset_index()
regions.loc[:, ['REGION', 'NCCENR']]
regions['REGION'].unique()
regions['REGION'].unique()
regions.loc['REGION'=='1']
regions.reindex(index=['REGION'])
pd.DataFrame(regions,index=regions['REGION'].unique())


dataset = pd.read_excel('TP/MDB-INSEE-V2.xls', sheet_name='Table Décisionnelle INSEE')
df_raw = pd.DataFrame(dataset)
df_raw.columns.values
df_raw['Urbanité Ruralité'].dtype
# df['Urbanité Ruralité'].astype(unicode)

print('-- Shape: {}'.format(df_raw.shape))
print('-- Infos:')
df_raw.info()
print('-- Infos END --')

df_raw.describe()
df_raw.head(5)

#  les noms de colonnes
df_raw.columns.values
df_raw.dtypes
print(df_raw.dtypes)

df1 = pd.DataFrame(df_raw, columns=['CODGEO',
                                    'LIBGEO',
                                    'Orientation Economique',
                                    'Urbanité Ruralité',
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
df1.shape
df1.dtypes
df1['Urbanité Ruralité'].unique()
df1['Urbanité Ruralité'].dtype
df1.head(5)
df1.describe()
df1.info(verbose=True)
df1['Population'].sum()
df1['Nb praticiens'] = df1['Nb Omnipraticiens BV'] \
                       + df1['Nb Infirmiers Libéraux BV'] \
                       + df1['Nb dentistes Libéraux BV'] \
                       + df1['Nb pharmaciens Libéraux BV']
df1['Region'] = regions[df1['REG']]
df1[['Nb Atifs', 'Population', 'Nb praticiens', 'Nb propriétaire']].corr(method='pearson')


df1['Nb praticiens'].mean()
df1['Nb praticiens'].quantile(0.25)
df1['Nb praticiens'].quantile(0.50)
df1['Nb praticiens'].quantile(0.75)
np.percentile(df1['Nb praticiens'], 25)
np.percentile(df1['Nb praticiens'], 50)
np.percentile(df1['Nb praticiens'], 75)

plt.subplot(121)
plt.title('Population')
pd.DataFrame(df1['Population']).boxplot()
plt.subplot(122)
plt.title('Nb praticiens')
pd.DataFrame(df1['Nb praticiens']).boxplot()
plt.show()
plt.close()

df1.boxplot(column='Nb praticiens', by='REG')
plt.title("Nb praticiens par région")
plt.suptitle("")
plt.ylabel("Nb praticiens")
plt.xlabel("Région")
plt.ylim(0,200)


df1.loc[:, ['Population', 'Nb praticiens']].boxplot()
df1.loc[:, ['Nb Omnipraticiens BV', 'Nb Infirmiers Libéraux BV', 'Nb dentistes Libéraux BV',
            'Nb pharmaciens Libéraux BV']].boxplot()
plt.show()
plt.close()

df1['Population'].mean()
df1['Population'].quantile(0.25)
df1['Population'].quantile(0.50)
df1['Population'].quantile(0.75)

plt.figure()
plt.scatter(df1['Population'], df1['Nb praticiens'], marker='o', s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()

#
# données groupées par département
#
# TODO: faire aggrégat de ruralité:
# TODO: - nb de communes rurales par dep
# TODO: - cumul pop des communes rurales par dep
# TODO: - % de la pop rurales par dep
df1_dep = df1.groupby(['DEP']).aggregate(np.sum)
df1_dep.drop('Evolution Pop %', axis=1, inplace=True)
df1_dep.shape
df1_dep.info()
df1_dep.dtypes
plt.figure()
pd.DataFrame(df1_dep['Nb praticiens']).boxplot()
plt.show()
plt.close()

plt.figure()
plt.scatter(df1_dep['Population'], df1_dep['Nb praticiens'], marker='o', s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()

#
#
df2 = pd.DataFrame(df_raw, columns=['CODGEO',
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

df3 = pd.DataFrame(df_raw, columns=['CODGEO',
                                    'Orientation Economique',
                                    'Urbanité Ruralité',
                                    'LIBGEO',
                                    'REG',
                                    'DEP'])
df3['Nb praticiens'] = df_raw['Nb Omnipraticiens BV'] \
                       + df_raw['Nb Infirmiers Libéraux BV'] \
                       + df_raw['Nb dentistes Libéraux BV'] \
                       + df_raw['Nb pharmaciens Libéraux BV']
df3['Population'] = df_raw['Population']
df3['Nb Atifs'] = df_raw['Nb Atifs']
df3[['Nb praticiens', 'Population']].corr(method='pearson')
df3[['Nb Atifs', 'Population', 'Nb praticiens']].corr(method='pearson')
