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
import urllib2
import textwrap

# répertoire racine à adapter
path_root = './Statnum'
# répertoire pour fichier de données, à adapter
path_data = './TP'
# url du fichier de données
data_file_url = 'https://www.data.gouv.fr/s/resources/data-insee-sur-les-communes/20141212-105948/MDB-INSEE-V2.xls'
#  nom du fichier de données
data_file = 'MDB-INSEE-V2.xls'
data_sheet_name = 'Table Décisionnelle INSEE'

if os.path.basename(os.getcwd()) != path_root:
    os.chdir(path_root)


# fonctions utiles
def qqplot(x, y):
    m = min([x.size, y.size])
    alpha = np.linspace(1. / float(m), 1., m)
    qx = x.quantile(alpha)
    qy = y.quantile(alpha)
    plt.scatter(qx, qy, marker='o', s=20, facecolors='none', edgecolors='r')


def scatter_qqplots(dframe, title='QQ-plots'):
    plt.figure(figsize=(10, 8))
    nvar = dframe.shape[1]
    plt.suptitle(title)
    iplot = 0
    ixplot = 0
    for ix in dframe.columns.values:
        ixplot += 1
        iyplot = 0
        for iy in dframe.columns.values:
            iyplot += 1
            iplot += 1
            plt.subplot(nvar, nvar, iplot)
            if ixplot == iyplot:
                plt.axis('off')
                plt.text(0.5, 0.5, "\n".join(textwrap.wrap(iy, 20)), dict(size=8),
                         horizontalalignment='center', verticalalignment='center')
            elif iyplot > ixplot:
                # plt.subplots_adjust(left=0.2, hspace=1., wspace=1., top=0.9)
                plt.subplots_adjust(hspace=0.3, wspace=0.3)
                qqplot((dframe[ix] - dframe[ix].mean()) / dframe[ix].std(),
                       (dframe[iy] - dframe[iy].mean()) / dframe[iy].std())
            else:
                plt.axis('off')
        plt.show()


def grid_scatter_plots(dframe, title='Plots'):
    plt.figure(figsize=(10, 8))
    nvar = dframe.shape[1]
    plt.suptitle(title)
    iplot = 0
    ixplot = 0
    iyplot = 0
    for ix in dframe.columns.values:
        ixplot += 1
        iyplot = 0
        for iy in dframe.columns.values:
            iyplot += 1
            iplot += 1
            plt.subplot(nvar, nvar, iplot)
            if ixplot == iyplot:
                plt.axis('off')
                plt.text(0.5, 0.5, "\n".join(textwrap.wrap(iy, 20)), dict(size=8),
                         horizontalalignment='center', verticalalignment='center')
            elif iyplot > ixplot:
                # plt.subplots_adjust(left=0.2, hspace=0.8, wspace=0.8, top=0.8)
                plt.subplots_adjust(hspace=0.3, wspace=0.3)
                plt.scatter(dframe[ix], dframe[iy], marker='o', s=20, facecolors='none', edgecolors='r')
            else:
                plt.axis('off')
    plt.show()


def myPCA(df):
    # Normalize data
    df_norm = (df - df.mean()) / df.std()
    # PCA
    pca = PCA()
    pca_transf = pca.fit_transform(df_norm.values)
    # Ebouli
    ebouli = pd.Series(pca.explained_variance_ratio_)
    coef = np.transpose(pca.components_)
    cols = ['PC-' + str(x) for x in range(len(ebouli))]
    pc_infos = pd.DataFrame(coef, columns=cols, index=df_norm.columns)
    return pc_infos, ebouli, pca_transf, pca


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


# raw_input()

# https://www.data.gouv.fr/s/resources/data-insee-sur-les-communes/20141212-105948/MDB-INSEE-V2.xls
print('Télécharger le fichier des données (dure quelques minutes) ? ')
if raw_input() == 'O':
    response = urllib2.urlopen(data_file_url)
    dataset_xls = response.read()
    with open(os.path.join(path_data, data_file), b'wb') as f:
        f.write(dataset_xls)

dataset = pd.read_excel(os.path.join(path_data, data_file), sheet_name=data_sheet_name)
df_raw = pd.DataFrame(dataset)
df_raw.set_index(['CODGEO'], inplace=True)
print('-- Shape: {}'.format(df_raw.shape))
print('-- Infos:')
df_raw.info()
df_raw.dtypes
df_raw.describe()
df_raw.head(5)
print('-- Infos END --')

# ajout colonne synthese des hébergements disponibles
df_raw['Capacité hebergements'] = df_raw['Capacité Hotel'].fillna(0) + df_raw['Capacité Camping'].fillna(0)
df_raw['Nb Entreprises'] = df_raw['Nb Entreprises Secteur Services'].fillna(0) \
                           + df_raw['Nb Entreprises Secteur Commerce'].fillna(0) \
                           + df_raw['Nb Entreprises Secteur Construction'].fillna(0) \
                           + df_raw['Nb Entreprises Secteur Industrie'].fillna(0)
df_raw['Nb Création Entreprises'] = df_raw['Nb Création Services'].fillna(0) \
                                    + df_raw['Nb Création Commerces'].fillna(0) \
                                    + df_raw['Nb Création Construction'].fillna(0) \
                                    + df_raw['Nb Création Industrielles'].fillna(0)
df_raw['Nb Entreprises serv comm'] = df_raw['Nb Entreprises Secteur Services'].fillna(0) \
                                     + df_raw['Nb Entreprises Secteur Commerce'].fillna(0)
df_raw['Nb Entreprises cons indus'] = df_raw['Nb Entreprises Secteur Construction'].fillna(0) \
                                      + df_raw['Nb Entreprises Secteur Industrie'].fillna(0)
df_raw['Nb Création Entreprises serv comm'] = df_raw['Nb Création Services'].fillna(0) \
                                              + df_raw['Nb Création Commerces'].fillna(0)
df_raw['Nb Création Entreprises cons indus'] = df_raw['Nb Création Construction'].fillna(0) \
                                               + df_raw['Nb Création Industrielles'].fillna(0)

df_raw.info()

# données groupées par département
#
# TODO: faire aggrégat de ruralité:
# TODO: - nb de communes rurales par dep
# TODO: - cumul pop des communes rurales par dep
# TODO: - % de la pop rurales par dep
#  Colonne BV : bassin de vie; voir association comunne -> BV
# dans fichier de référence INSEE 2012

# donnée economiques
df_raw_dep_entrep = pd.DataFrame(df_raw, columns=[
    'DEP',
    'Nb Entreprises',
    'Nb Création Entreprises',
    'Nb Education, santé, action sociale',
    'Capacité hebergements',
])
df_dep_entrep = df_raw_dep_entrep.groupby(['DEP']).aggregate(np.sum)
df_raw_dep_salaires = pd.DataFrame(df_raw, columns=[
    'DEP',
    'Moyenne Revenus Fiscaux Départementaux',
    'Dep Moyenne Salaires Cadre Horaires',
    'Dep Moyenne Salaires Prof Intermédiaire Horaires',
    'Dep Moyenne Salaires Employé Horaires',
    'Dep Moyenne Salaires Ouvrié Horaires',
])
df_dep_salaires = df_raw_dep_salaires.groupby(['DEP']).aggregate(np.min)
df_dep_eco = pd.DataFrame(pd.concat([df_dep_entrep, df_dep_salaires], axis=1))
type(df_dep_eco)
df_dep_eco.info()
df_dep_eco.shape
df_dep_eco.index
df_dep_eco.columns.values
df_dep_eco.describe()
df_dep_eco.head()

# donnée population
# df_raw_dep_pop = pd.DataFrame(df_raw, columns=[
#     'DEP',
#     'Population',
#     'Evolution Population',
#     'Nb Ménages',
#     'Nb Résidences Principales',
#     'Nb propriétaire',
#     'Nb Logement',
#     'Nb Résidences Secondaires',
#     'Nb Log Vacants',
#     'Nb Femme',
#     'Nb Homme',
#     'Nb Mineurs',
#     'Nb Majeurs',
#     'Nb Etudiants',
#     'Nb Actifs Salariés',
#     'Nb Actifs Non Salariés',
# ])
df_raw_dep_pop = pd.DataFrame(df_raw, columns=[
    'DEP',
    'Population',
    'Evolution Population',
    'Nb Ménages',
    'Nb propriétaire',
    'Nb Etudiants',
    'Nb Actifs Salariés',
    'Nb Actifs Non Salariés',
])
df_dep_pop = pd.DataFrame(df_raw_dep_pop.groupby(['DEP']).aggregate(np.sum))
df_dep_pop['Evolution Population %'] = np.round(100.*df_dep_pop['Evolution Population'].fillna(0) / df_dep_pop['Population'].fillna(1), 1)
del(df_dep_pop['Population'])
del(df_dep_pop['Evolution Population'])
type(df_dep_pop)
df_dep_pop.info()
df_dep_pop.shape
df_dep_pop.index
df_dep_pop.columns.values
df_dep_pop.describe()

# regroupement de toutes les données quantitatives départementales
df_dep = pd.DataFrame(pd.concat([df_dep_pop, df_dep_eco], axis=1))
df_dep.info()
df_dep.shape
df_dep.index
df_dep.columns.values
df_dep.dtypes
df_dep.describe()

# existence de NaN
df_dep.dropna().shape
df_dep_eco.dropna().shape
df_dep_pop.dropna().shape
for col in df_dep.columns.values:
    print('{}: {}'.format(col, df_dep[col].dropna().shape))


# centrage et reduction des variables
def center_df(df):
    df_cr = pd.DataFrame()
    for col in df.columns.values:
        df_cr[col] = (df[col] - df[col].mean()) / df[col].std()
    return df_cr


df_dep_entrep_cr = center_df(df_dep_entrep)
df_dep_salaires_cr = center_df(df_dep_salaires)
df_dep_pop_cr = center_df(df_dep_pop)
df_dep_cr = center_df(df_dep)
df_dep_eco_cr = center_df(df_dep_eco)



#######################################################################
# affichage des plots 2x2
scatter_qqplots(df_dep_entrep, 'QQ-plots variables entreprises')
scatter_qqplots(df_dep_salaires, 'QQ-plots variables salaires')
scatter_qqplots(df_dep_pop, 'QQ-plots démographie')
grid_scatter_plots(df_dep_pop, 'Démographie')
grid_scatter_plots(df_dep_pop.iloc[:, :3], 'Démographie')


#######################################################################
# calcul PCA sur données complètes
pca_infos_dep, ebouli_dep, pca_transf_dep, pca_dep = myPCA(df_dep)

plt.figure()
circleOfCorrelations(pca_infos_dep, ebouli_dep)
plt.show()

plt.figure()
scree_dep_cr = pd.Series(pca_dep.explained_variance_ratio_)
scree_dep_cr.plot(kind='bar', title=u"Part de la variance expliquée par CP")
np.cumsum(scree_dep_cr).plot(drawstyle="steps-post", color='red', linestyle='--')
plt.show()

plt.figure()
plt.plot(pca_transf_dep[:, 0], pca_transf_dep[:, 1], 'o', markersize=3, color='blue')
plt.xlabel('1er axe principal')
plt.ylabel('2e axe principal')
plt.legend()
plt.title('ACP avec 2 composantes principales')
plt.show()

inerties_cr = pca_dep.explained_variance_  # inertie expliquée par chaque composante principale
print("Inertie d'une, deux, trois composantes principales : {}".format(np.cumsum(inerties_cr)))
print('valeurs singulieres : {}'.format(np.sqrt(inerties_cr * df_dep.shape[0])))
plt.figure()
pd.Series(np.sqrt(inerties_cr * df_dep.shape[0])).plot(kind='bar', title=u"Valeurs singulières")
plt.show()


#######################################################################
# boxplot sur données salaires ni reduites ni centrées
fig, axs = plt.subplots(nrows=1, ncols=5, figsize=(10, 4))
iboxp = 0
for col in ['Moyenne Revenus Fiscaux Départementaux',
            'Dep Moyenne Salaires Prof Intermédiaire Horaires',
            'Dep Moyenne Salaires Employé Horaires',
            'Dep Moyenne Salaires Employé Horaires',
            'Dep Moyenne Salaires Ouvrié Horaires']:
    axs[iboxp].boxplot(df_dep_eco[col])
    b_title = "\n".join(textwrap.wrap(col, 20))
    axs[iboxp].set_xticklabels(np.repeat(b_title, 2), rotation=0, fontsize=6)
    iboxp += 1
plt.tight_layout()


#######################################################################
# PCA sur données salaires reduites centrées
def pca_figs(df, savefig=None, fmt='eps'):
    pca_infos, ebouli, pca_transf, pca = myPCA(df)
    plt.figure()
    circleOfCorrelations(pca_infos, ebouli)
    plt.show()
    if savefig:
        typ_fig = 'Corr'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')

    plt.figure()
    scree = pd.Series(pca.explained_variance_ratio_)
    scree.plot(kind='bar', title=u"Part de la variance expliquée par CP")
    np.cumsum(scree).plot(drawstyle="steps-post", color='red', linestyle='--')
    plt.show()
    if savefig:
        typ_fig = 'Var'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')

    plt.figure()
    plt.plot(pca_transf[:, 0], pca_transf[:, 1], 'o', markersize=3, color='blue')
    plt.xlabel('1er axe principal')
    plt.ylabel('2e axe principal')
    plt.legend()
    plt.title('ACP avec 2 composantes principales')
    plt.show()
    if savefig:
        typ_fig = '2CP'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')

    inerties = pca.explained_variance_  # inertie expliquée par chaque composante principale
    print("Inertie d'une, deux, trois composantes principales : {}".format(np.cumsum(inerties)))
    print('valeurs singulieres : {}'.format(np.sqrt(inerties * df.shape[0])))
    plt.figure()
    pd.Series(np.sqrt(inerties * df.shape[0])).plot(kind='bar', title=u"Valeurs singulières")
    plt.show()
    if savefig:
        typ_fig = 'Inert'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')
    return pca_infos, ebouli, pca_transf, pca


pca_salaires = dict()
pca_salaires['pca_infos'], \
pca_salaires['ebouli'], \
pca_salaires['pca_transf'], \
pca_salaires['pca'] = \
    pca_figs(df_dep_salaires, os.path.join(path_data, 'salaires'))

pca_entrep = dict()
pca_entrep['pca_infos'], \
pca_entrep['ebouli'], \
pca_entrep['pca_transf'], \
pca_entrep['pca'] = \
    pca_figs(df_dep_entrep, os.path.join(path_data, 'entrep'))

pca_pop = dict()
pca_pop['pca_infos'], \
pca_pop['ebouli'], \
pca_pop['pca_transf'], \
pca_pop['pca'] = \
    pca_figs(df_dep_pop, os.path.join(path_data, 'population'))




########################################################################################
# K-means clustering: données après PCA
def Kmeans_figs(ndarr, suptitle='', n_clusters = 2):
    k_means = KMeans(n_clusters=n_clusters, random_state=0)
    k_means.fit(ndarr)
    y_pred = k_means.predict(ndarr)
    fig = plt.figure(figsize=(8, 6))
    fig.suptitle("K-Means clustering {}, K={}".format(suptitle, n_clusters))
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(ndarr[:, 0], ndarr[:, 1], c=y_pred)
    plt.show()


Kmeans_figs(pca_salaires['pca_transf'], 'on PCA-reduced')
Kmeans_figs(pca_entrep['pca_transf'], 'on PCA-reduced')
Kmeans_figs(pca_pop['pca_transf'], 'on PCA-reduced')
Kmeans_figs(np.array(df_dep_salaires_cr), 'on salaires CR')




# Regroupement hiérarchique ascendant
distArray = ssd.squareform(ssd.pdist(df_dep_salaires_cr, metric=b'euclidean'))
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

type(df_dep_salaires_cr.index)
type(df_dep_salaires_cr.index[0])
# dictionnaire des clusters: une entrée par cluster
# chaque entrée est associée à la liste des départements qui constituent un cluster particulier
dep_clusters = dict()
for clu in uniq:
    dep_clusters[clu] = list()
    for i in range(df_dep_salaires_cr.shape[0]):
        if clusters[i] == clu:
            dep_clusters[clu].append(df_dep_salaires_cr.index[i])

ind = np.arange(2)  # les coordonnées des abscisses x des bâtons
width = 0.35  # largeur des bâtons
clu_1 = (len(dep_clusters[1]), 0)
clu_2 = (0, len(dep_clusters[2]))
p1 = plt.bar(ind, clu_1, width, color='r')
p2 = plt.bar(ind, clu_2, width, color='b', bottom=clu_1)
plt.title('Nombres de départements dans chaque cluster')
plt.xticks(ind + width / 2., ('1', '2'))
plt.legend((p1[0], p2[0]), ('Cluster 1', 'Cluster 2'), loc=0)


# Regroupement hiérarchique ascendant
def clustering(df, seuil):
    distArray = ssd.squareform(ssd.pdist(df, metric=b'euclidean'))

    # methode plus courte distance
    plt.figure()
    linkAverage = linkage(distArray, method=b'single')
    dendrogram(linkAverage)
    plt.show()

    # methode de ward
    plt.figure()
    linkAverage = linkage(distArray, method=b'ward')
    dendrogram(linkAverage)
    plt.show()

    # clusters à partir de méthode de ward
    clusters = fcluster(linkAverage, seuil, criterion=b'distance')
    uniq, unique_indices, unique_inverse, unique_counts = np.unique(clusters, return_counts=True, return_inverse=True,
                                                                    return_index=True)

    # dictionnaire des clusters: une entrée par cluster
    # chaque entrée est associée à la liste des départements qui constituent un cluster particulier
    dep_clusters = dict()
    for clu in uniq:
        dep_clusters[clu] = list()
        for i in range(df.shape[0]):
            if clusters[i] == clu:
                dep_clusters[clu].append(df.index[i])

    ind = np.arange(2)  # les coordonnées des abscisses x des bâtons
    width = 0.35  # largeur des bâtons
    clu_1 = (len(dep_clusters[1]), 0)
    clu_2 = (0, len(dep_clusters[2]))
    plt.figure()
    p1 = plt.bar(ind, clu_1, width, color='r')
    p2 = plt.bar(ind, clu_2, width, color='b', bottom=clu_1)
    plt.title('Nombres de départements dans chaque cluster')
    plt.xticks(ind + width / 2., ('1', '2'))
    plt.legend((p1[0], p2[0]), ('Cluster 1', 'Cluster 2'), loc=0)
    return dep_clusters


dep_clusters_salaires = clustering(df_dep_salaires_cr, seuil=100.)
dep_clusters_entrep = clustering(df_dep_entrep_cr, seuil=140.)
dep_clusters_pop = clustering(df_dep_pop_cr, seuil=140.)
