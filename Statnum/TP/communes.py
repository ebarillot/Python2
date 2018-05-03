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
regions[regions[b'REGION'] == 1]
regions.set_index('REGION', inplace=True)
regions
regions.loc[1]
regions.columns.values
regions.index
regions.loc[:, ['NCCENR']]
regions.loc[1]['NCCENR']
regions_noms = regions['NCCENR']
regions_noms.index
regions_noms[1]
regions_noms[2]
type(regions_noms)  # => Series
regions_noms.index

#
#
dataset = pd.read_excel('TP/MDB-INSEE-V2.xls', sheet_name='Table Décisionnelle INSEE')
df_raw = pd.DataFrame(dataset)
df_raw.set_index(['CODGEO'], inplace=True)
df_raw.index
df_raw.columns.values
df_raw.info()
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

# communes par population
# comm_pop = np.log(df_raw[df_raw['Population']>0][['Population']])
comm_pop = df_raw[df_raw['Population'] > 0]['Population']
comm_pop2 = map(lambda x: int(x), ((np.floor(comm_pop / 1000)) * 1000))
pop_freq = pd.Series(sorted(comm_pop2)).value_counts()
fig = 1
plt.figure(fig)
pop_freq[2:].plot()
plt.show()
plt.close(fig)

cuts = pd.cut(df_raw['Population'],
              range(0, 10000, 1000)
              + range(10000, 100000, 10000)
              + range(100000, 1000000, 100000)
              + range(1000000, 5000000, 1000000))
cuts.value_counts()[5:].plot(kind='bar')
plt.show()

pd.DataFrame(df_raw['Population']).boxplot()
plt.show()

#
#
comm_pop_pct = df_raw['Evolution Pop %']
pop_pct_freq = pd.Series(sorted(comm_pop_pct)).value_counts()
fig = 2
plt.figure(fig)
pop_pct_freq.hist()
plt.show()
plt.close(fig)

type(comm_pop)
np.array(comm_pop)
fig = 1
plt.figure(fig)
comm_pop.plot()
plt.hist(np.array(comm_pop), normed=True, bins=20)
plt.title("Histogramme population des communes")
plt.xlabel("Population")
plt.legend(["population"])
plt.show()

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
type(df1['REG'])
type(regions_noms)
regions_noms[df1['REG']]
#  ==> faire une serie à partir d'une autre
df1['Region'] = regions_noms[df1['REG']]
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
plt.ylim(0, 200)

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
#  Colonne BV : bassin de vie; voir association comunne -> BV
# dans fichier de référence INSEE 2012
df_raw_dep_1 = pd.DataFrame(df_raw, columns=[
    'DEP',
    'Nb Pharmacies et parfumerie',
    'Dynamique Entrepreneuriale',
    'Dynamique Entrepreneuriale Service et Commerce',
    'Population',
    'Evolution Population',
    'Nb Ménages',
    'Nb Résidences Principales',
    'Nb propriétaire',
    'Nb Logement',
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
    'Nb Logement Secondaire et Occasionnel',
    'Nb Hotel',
    'Capacité Hotel',
    'Nb Camping',
    'Capacité Camping'
    'Nb Entreprises Secteur Services',
    'Nb Entreprises Secteur Commerce',
    'Nb Entreprises Secteur Construction',
    'Nb Entreprises Secteur Industrie',
    'Nb Création Enteprises',
    'Nb Création Industrielles',
    'Nb Création Construction',
    'Nb Création Commerces',
    'Nb Création Services',
    'Nb Education, santé, action sociale',
    'Nb Services personnels et domestiques',
    'Nb Santé, action sociale',
])
df_raw_dep_2 = pd.DataFrame(df_raw, columns=[
    'DEP',
    'REG',
    'Moyenne Revenus Fiscaux Départementaux',
    'Dep Moyenne Salaires Horaires',
    'Dep Moyenne Salaires Cadre Horaires',
    'Dep Moyenne Salaires Prof Intermédiaire Horaires',
    'Dep Moyenne Salaires Employé Horaires',
    'Dep Moyenne Salaires Ouvrié Horaires'
])
df_dep_2 = df_raw_dep_2.groupby(['DEP']).aggregate(np.min)


df_dep_1 = df_raw_dep_1.groupby(['DEP']).aggregate(np.sum)
type(df_dep_1)
df_dep_1.index
df_dep_1.columns.values
df_dep_1.describe()
df_raw_dep_2.columns.values

df_dep = pd.concat([df_dep_1, df_dep_2], axis=1)

plt.figure()
pd.DataFrame(df_dep['Nb Résidences Principales']).boxplot()
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Population'], df_dep['Nb Education, santé, action sociale'], marker='o', s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Nb Résidences Principales'], df_dep['Nb Résidences Secondaires'], marker='o', s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Nb Création Industrielles'], df_dep['Nb Création Commerces'], marker='o', s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Nb Création Industrielles'], df_dep['Nb Création Services'], marker='o', s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Moyenne Revenus Fiscaux Départementaux'], df_dep['Dep Moyenne Salaires Horaires'], marker='o', s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Moyenne Revenus Fiscaux Départementaux'], df_dep['Dep Moyenne Salaires Cadre Horaires'], marker='o', s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Moyenne Revenus Fiscaux Départementaux'], df_dep['Dep Moyenne Salaires Prof Intermédiaire Horaires'], marker='o', s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Moyenne Revenus Fiscaux Départementaux'], df_dep['Dep Moyenne Salaires Ouvrié Horaires'], marker='o', s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()

