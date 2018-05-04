# coding=utf-8

from __future__ import unicode_literals
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import scipy.spatial.distance as ssd
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

if os.path.basename(os.getcwd()) != 'Statnum':
    os.chdir('./Statnum')

# https://www.data.gouv.fr/fr/datasets/data-insee-sur-les-communes/
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Feuil1', converters={u'Urbanité Ruralité': unicode})
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Feuil1', dtype={u'Urbanité Ruralité': str})
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Feuil1')
# dataset = pd.read_excel('TP/MDB-INSEE-V2.xlsx', sheet_name='Table Décisionnelle INSEE')
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

#
# données groupées par département
#
# TODO: faire aggrégat de ruralité:
# TODO: - nb de communes rurales par dep
# TODO: - cumul pop des communes rurales par dep
# TODO: - % de la pop rurales par dep
#  Colonne BV : bassin de vie; voir association comunne -> BV
# dans fichier de référence INSEE 2012

# donnée entreprises
df_raw_dep_entrep = pd.DataFrame(df_raw, columns=[
    'DEP',
    'Nb Pharmacies et parfumerie',
    'Dynamique Entrepreneuriale',
    'Dynamique Entrepreneuriale Service et Commerce',
    'Nb Hotel',
    'Capacité Hotel',
    'Nb Camping',
    'Capacité Camping',
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
df_dep_entrep = df_raw_dep_entrep.groupby(['DEP']).aggregate(np.sum)
type(df_dep_entrep)
df_dep_entrep.index
df_dep_entrep.columns.values
df_dep_entrep.describe()

# donnée population
df_raw_dep_pop = pd.DataFrame(df_raw, columns=[
    'DEP',
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
])
df_dep_pop = df_raw_dep_pop.groupby(['DEP']).aggregate(np.sum)
type(df_dep_pop)
df_dep_pop.index
df_dep_pop.columns.values
df_dep_pop.describe()

# donnée salaires
df_raw_dep_salr = pd.DataFrame(df_raw, columns=[
    'DEP',
    'Moyenne Revenus Fiscaux Départementaux',
    'Dep Moyenne Salaires Horaires',
    'Dep Moyenne Salaires Cadre Horaires',
    'Dep Moyenne Salaires Prof Intermédiaire Horaires',
    'Dep Moyenne Salaires Employé Horaires',
    'Dep Moyenne Salaires Ouvrié Horaires'
])
df_raw_dep_salr.columns.values
type(df_raw_dep_salr)
df_raw_dep_salr.index
df_raw_dep_salr.columns.values
df_raw_dep_salr.describe()
df_dep_salr = df_raw_dep_salr.groupby(['DEP']).aggregate(np.min)

# regroupement de toutes les données quantitatives départementales
df_dep = pd.concat([df_dep_pop, df_dep_salr, df_dep_entrep], axis=1)
df_dep.index
df_dep.columns.values
df_dep.describe()

# pour garder la correspondance DEP - REG
df_raw_dep_reg = pd.DataFrame(df_raw, columns=['DEP', 'REG'])
df_raw_dep_reg.columns.values
type(df_raw_dep_reg)
df_raw_dep_reg.index
df_raw_dep_reg.columns.values
df_raw_dep_reg.describe()
df_dep_reg = df_raw_dep_reg.groupby(['DEP']).aggregate(np.min)

# centrage des variables
df_dep_c = pd.DataFrame()
for col in df_dep.columns.values:
    df_dep_c[col] = df_dep[col] - df_dep[col].mean()

# centrage et reduction des variables
df_dep_cr = pd.DataFrame()
for col in df_dep.columns.values:
    df_dep_cr[col] = (df_dep[col] - df_dep[col].mean()) / df_dep[col].std()
df_dep_pop_cr = pd.DataFrame()
for col in df_dep_pop.columns.values:
    df_dep_pop_cr[col] = (df_dep_pop[col] - df_dep_pop[col].mean()) / df_dep_pop[col].std()
df_dep_salr_cr = pd.DataFrame()
for col in df_dep_salr.columns.values:
    df_dep_salr_cr[col] = (df_dep_salr[col] - df_dep_salr[col].mean()) / df_dep_salr[col].std()
df_dep_entrep_cr = pd.DataFrame()
for col in df_dep_entrep.columns.values:
    df_dep_entrep_cr[col] = (df_dep_entrep[col] - df_dep_entrep[col].mean()) / df_dep_entrep[col].std()

df_dep_cr.describe()
df_dep_cr.shape
df_dep_cr.dropna().shape
for col in df_dep.columns.values:
    print('{}: {}'.format(col, df_dep_cr[col].dropna().shape))

# PCA sur données non reduites, non centrées
pca_dep = PCA()
# pca = PCA(n_components=2)
df_dep_transf = pca_dep.fit_transform(df_dep)  # pas nécessaire de centrer les colonnes ; renvoie les comp. princ.
df_dep_transf

print("Shape of reduced dataset: {}".format(str(df_dep_transf.shape)))

plt.figure()
plt.plot(df_dep_transf[:, 0], df_dep_transf[:, 1], 'o', markersize=7, color='blue')
plt.xlabel('1er axe principal')
plt.ylabel('2e axe principal')
plt.legend()
plt.title('ACP avec 2 composantes principales')
plt.show()

inerties = pca_dep.explained_variance_  # inertie expliquée par chaque composante principale
print("Inertie d'une, deux, trois composantes principales : {}".format(np.cumsum(inerties)))
print('valeurs singulieres : {}'.format(np.sqrt(inerties * df_dep_transf.shape[0])))

# PCA sur données reduites centrées
pca_dep_cr = PCA()
# pca = PCA(n_components=2)
df_dep_cr_transf = pca_dep_cr.fit_transform(
    df_dep_cr)  # pas nécessaire de centrer les colonnes ; renvoie les comp. princ.
df_dep_cr_transf

print("Shape of reduced dataset: {}".format(str(df_dep_cr_transf.shape)))

plt.figure()
plt.plot(df_dep_cr_transf[:, 0], df_dep_cr_transf[:, 1], 'o', markersize=7, color='blue')
plt.xlabel('1er axe principal')
plt.ylabel('2e axe principal')
plt.legend()
plt.title('ACP avec 2 composantes principales')
plt.show()

inerties_cr = pca_dep_cr.explained_variance_  # inertie expliquée par chaque composante principale
print("Inertie d'une, deux, trois composantes principales : {}".format(np.cumsum(inerties_cr)))
print('valeurs singulieres : {}'.format(np.sqrt(inerties_cr * df_dep_cr_transf.shape[0])))

# PCA sur données salaires reduites centrées
pca_salr_cr = PCA()
# pca = PCA(n_components=2)
df_dep_salr_cr_transf = pca_salr_cr.fit_transform(df_dep_salr_cr)
df_dep_salr_cr_transf

print("Shape of reduced dataset: {}".format(str(df_dep_salr_cr_transf.shape)))

plt.figure()
plt.plot(df_dep_salr_cr_transf[:, 0], df_dep_salr_cr_transf[:, 1], 'o', markersize=7, color='blue')
plt.xlabel('1er axe principal')
plt.ylabel('2e axe principal')
plt.legend()
plt.title('ACP avec 2 composantes principales')
plt.show()

inerties_salr_cr = pca_salr_cr.explained_variance_  # inertie expliquée par chaque composante principale
print("Inertie d'une, deux, trois composantes principales : {}".format(np.cumsum(inerties_salr_cr)))
print("Inertie % expliquée cumulée : {}".format(np.cumsum(pca_salr_cr.explained_variance_ratio_)))
print('valeurs singulieres : {}'.format(np.sqrt(inerties_salr_cr * df_dep_salr_cr_transf.shape[0])))

plt.figure()
scree_salr_cr = pd.Series(pca_salr_cr.explained_variance_ratio_)
scree_salr_cr.plot(kind='bar', title=u"Part de la variance expliquée par CP")
scree_salr_cr_cum = pd.Series(np.cumsum(pca_salr_cr.explained_variance_ratio_))
scree_salr_cr_cum.plot(drawstyle="steps-post", color='red', linestyle='--')
plt.show()

# PCA sur données salaires ni reduites ni centrées
pca_salr = PCA()
df_dep_salr_transf = pca_salr.fit_transform(
    df_dep_salr)  # pas nécessaire de centrer les colonnes ; renvoie les comp. princ.
df_dep_salr_transf

print("Shape of reduced dataset: {}".format(str(df_dep_salr_transf.shape)))

plt.figure()
plt.plot(df_dep_salr_transf[:, 0], df_dep_salr_transf[:, 1], 'o', markersize=7, color='blue')
plt.xlabel('1er axe principal')
plt.ylabel('2e axe principal')
plt.legend()
plt.title('ACP avec 2 composantes principales')
plt.show()

inerties_salr = pca_salr.explained_variance_  # inertie expliquée par chaque composante principale
print("Inertie d'une, deux, trois composantes principales : {}".format(np.cumsum(inerties_salr)))
print("Inertie % expliquée par la 1ere composante principale : {}".format(
    100.0 * inerties_salr[0] / np.sum(inerties_salr)))
print("Inertie % expliquée par les 2eres composantes principales : {}".format(
    100.0 * np.sum(inerties_salr[0:2]) / np.sum(inerties_salr)))
print('valeurs singulieres : {}'.format(np.sqrt(inerties_salr * df_dep_salr_transf.shape[0])))
plt.figure()
scree_salr = pd.Series(pca_salr.explained_variance_ratio_)
scree_salr.plot(kind='bar', title=u"Part de la variance expliquée par CP")
plt.show()


# fig = plt.figure(figsize=(8, 6))
# fig.suptitle("Dimensionality reduction on iris data")
# ax = fig.add_subplot(1, 1, 1)
# colors = ['red', 'yellow', 'magenta']
# cols = [colors[i] for i in df_dep.target]
# ax.scatter(df_dep_red[:, 0], df_dep[:, 1], c=cols)

def myPCA(df):
    # Normalize data
    df_norm = (df - df.mean()) / df.std()
    # PCA
    pca = PCA()
    pca_res = pca.fit_transform(df_norm.values)
    # Ebouli
    ebouli = pd.Series(pca.explained_variance_ratio_)
    coef = np.transpose(pca.components_)
    cols = ['PC-' + str(x) for x in range(len(ebouli))]
    pc_infos = pd.DataFrame(coef, columns=cols, index=df_norm.columns)
    return pc_infos, ebouli


def circleOfCorrelations(pc_infos, ebouli):
    plt.Circle((0, 0), radius=10, color='g', fill=False)
    circle1 = plt.Circle((0, 0), radius=1, color='g', fill=False)
    fig = plt.gcf()
    fig.gca().add_artist(circle1)
    for idx in range(len(pc_infos["PC-0"])):
        x = pc_infos["PC-0"][idx]
        y = pc_infos["PC-1"][idx]
        plt.plot([0.0, x], [0.0, y], 'k-')
        plt.plot(x, y, 'rx')
        plt.annotate(pc_infos.index[idx], xy=(x, y))
    plt.xlabel("PC-1 (%s%%)" % str(ebouli[0])[:4].lstrip("0."))
    plt.ylabel("PC-2 (%s%%)" % str(ebouli[1])[:4].lstrip("0."))
    plt.xlim((-1, 1))
    plt.ylim((-1, 1))
    plt.title("Circle of Correlations")


plt.figure()
pc_infos_salr, ebouli_salr = myPCA(df_dep_salr)
circleOfCorrelations(pc_infos_salr, ebouli_salr)
plt.show()

# K-means clustering:données après PCA
k_means_salr_cr_transf = KMeans(n_clusters=3, random_state=0)
k_means_salr_cr_transf.fit(df_dep_salr_cr_transf)
y_pred = k_means_salr_cr_transf.predict(df_dep_salr_cr_transf)
fig = plt.figure(figsize=(8, 6))
fig.suptitle("K-Means clustering on PCA-reduced, K=3")
ax = fig.add_subplot(1, 1, 1)
ax.scatter(df_dep_salr_cr_transf[:, 0], df_dep_salr_cr_transf[:, 1], c=y_pred)
plt.show()
type(df_dep_salr_cr_transf)

# K-means clustering:données centrées reduites
k_means_salr_cr = KMeans(n_clusters=3, random_state=0)
k_means_salr_cr.fit(df_dep_salr_cr)
y_pred = k_means_salr_cr.predict(df_dep_salr_cr)
fig = plt.figure(figsize=(8, 6))
fig.suptitle("K-Means clustering on PCA-reduced, K=3")
ax = fig.add_subplot(1, 1, 1)
ax.scatter(np.array(df_dep_salr_cr)[:, 0], np.array(df_dep_salr_cr)[:, 1], c=y_pred)
plt.show()

# Regroupement hiérarchique ascendant
distArray = ssd.squareform(ssd.pdist(df_dep_salr_cr, metric=b'euclidean'))
type(distArray)
distArray.shape

# methode plus courte distance
linkAverage = linkage(distArray, method=b'single')
dendrogram(linkAverage)
plt.show()

# methode de ward
linkAverage = linkage(distArray, method=b'ward')
dendrogram(linkAverage)
plt.show()

# clusters à partir de méthode de ward
clusters = fcluster(linkAverage, 100., criterion=b'distance')
clusters
type(clusters)
clusters.shape
len(clusters)
uniq, unique_indices, unique_inverse, unique_counts = np.unique(clusters, return_counts=True, return_inverse=True,
                                                                return_index=True)

type(df_dep_salr_cr.index)
type(df_dep_salr_cr.index[0])
# dictionnaire des clusters: une entrée par cluster
# chaque entrée est associée à la liste des départements qui constituent un cluster particulier
dep_clusters = dict()
for clu in uniq:
    dep_clusters[clu] = list()
    for i in range(df_dep_salr_cr.shape[0]):
        if clusters[i] == clu:
            dep_clusters[clu].append(df_dep_salr_cr.index[i])

ind = np.arange(2)  # les coordonnées des abscisses x des bâtons
width = 0.35  # largeur des bâtons
clu_1 = (len(dep_clusters[1]), 0)
clu_2 = (0, len(dep_clusters[2]))
p1 = plt.bar(ind, clu_1, width, color='r')
p2 = plt.bar(ind, clu_2, width, color='b', bottom=clu_1)

plt.title('Nombres de départements dans chaque cluster')
plt.xticks(ind + width / 2., ('1', '2'))
plt.legend((p1[0], p2[0]), ('Cluster 1', 'Cluster 2'), loc=0)


def scatter_matrix(dframe):
    plt.figure(figsize=(8, 6))
    nvar = dframe.shape[1]
    plt.suptitle('QQ-plots')
    iplot = 0
    ixplot = 0
    iyplot = 0
    for ix in dframe.columns.values:
        ixplot += 1
        for iy in dframe.columns.values:
            iyplot += 1
            iplot += 1
            plt.subplot(nvar, nvar, iplot)
            if ixplot == 1:
                plt.xlabel(ix, )
            if iyplot == 1:
                plt.ylabel(iy)
            plt.subplots_adjust(left=0.2, hspace=0.8, wspace=0.8, top=0.8)
            qqplot((dframe[ix] - dframe[ix].mean()) / dframe[ix].std(),
                   (dframe[iy] - dframe[iy].mean()) / dframe[iy].std())
    plt.show()


plt.figure()
pd.DataFrame(df_dep['Nb Résidences Principales']).boxplot()
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Population'], df_dep['Nb Education, santé, action sociale'], marker='o', s=50, facecolors='none',
            edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Nb Résidences Principales'], df_dep['Nb Résidences Secondaires'], marker='o', s=50,
            facecolors='none', edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Nb Création Industrielles'], df_dep['Nb Création Commerces'], marker='o', s=50, facecolors='none',
            edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Nb Création Industrielles'], df_dep['Nb Création Services'], marker='o', s=50, facecolors='none',
            edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Moyenne Revenus Fiscaux Départementaux'], df_dep['Dep Moyenne Salaires Horaires'], marker='o', s=50,
            facecolors='none', edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Moyenne Revenus Fiscaux Départementaux'], df_dep['Dep Moyenne Salaires Cadre Horaires'], marker='o',
            s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Moyenne Revenus Fiscaux Départementaux'],
            df_dep['Dep Moyenne Salaires Prof Intermédiaire Horaires'], marker='o', s=50, facecolors='none',
            edgecolors='r')
plt.show()
plt.close()

plt.figure()
plt.scatter(df_dep['Moyenne Revenus Fiscaux Départementaux'], df_dep['Dep Moyenne Salaires Ouvrié Horaires'],
            marker='o', s=50, facecolors='none', edgecolors='r')
plt.show()
plt.close()
