# coding=utf-8

from __future__ import unicode_literals
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn import preprocessing
import scipy.spatial.distance as ssd
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import urllib2
import textwrap

# répertoire racine à adapter
# Il correspond au répertoire de mon projet Python
# dont les sources sont gérés sous git et github
# Par défaut il faut le mettre à '.'
path_root = './Statnum'
# répertoire pour fichier de données, à adapter
# Par défaut il faut le mettre à '.'
path_data = './TP'
# si pb avec les répertoires, contacter ebarillot@yahoo.fr


# url du fichier de données
data_file_url = 'https://www.data.gouv.fr/s/resources/data-insee-sur-les-communes/20141212-105948/MDB-INSEE-V2.xls'
#  nom du fichier de données
data_file = 'MDB-INSEE-V2.xls'
data_sheet_name = 'Table Décisionnelle INSEE'

if os.path.basename(os.getcwd()) != path_root:
    os.chdir(path_root)


# fonctions utiles
def scatter3D_fig(df, cols=None, savefig=None, fmt='eps'):
    '''Affichage d'un nuage de points 3D'''
    if not cols:
        cols = df.columns.values[:3]
    plt.figure(figsize=(6, 6))
    ax = plt.axes(projection='3d')
    ax.set_title('Nuage de points en 3D')
    ax.set_xlabel(cols[0])
    ax.set_ylabel(cols[1])
    ax.set_zlabel(cols[2])
    ax.scatter3D(df[cols[0]], df[cols[1]], df[cols[2]], c='blue', s=8, marker='o')
    if savefig:
        typ_fig = 'scatter3D'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')


def boxplots_figs(df, cols=None, savefig=None, fmt='eps'):
    '''boxplots en ligne pour les variables de la DataFrame'''
    if not cols:
        cols = df.columns.values
    fig, axs = plt.subplots(nrows=1, ncols=len(cols), figsize=(8, 6))
    iboxp = 0
    for col in cols:
        axs[iboxp].boxplot(df[col])
        b_title = "\n".join(textwrap.wrap(col, 20))
        axs[iboxp].set_xticklabels(np.repeat(b_title, 2), rotation=0, fontsize=6)
        iboxp += 1
    plt.tight_layout()
    if savefig:
        typ_fig = 'boxplots'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')


def center_df(df):
    '''centrage des variables'''
    df_cr = pd.DataFrame()
    for col in df.columns.values:
        df_cr[col] = df[col] - df[col].mean()
    return df_cr


def centreduce_df(df):
    '''centrage et reduction des variables'''
    df_cr = pd.DataFrame()
    for col in df.columns.values:
        df_cr[col] = (df[col] - df[col].mean()) / df[col].std()
    return df_cr


def qqplot(x, y):
    '''figure QQplot centré de deux variables'''
    m = min([x.size, y.size])
    alpha = np.linspace(1. / float(m), 1., m)
    qx = x.quantile(alpha)
    qy = y.quantile(alpha)
    plt.scatter(qx, qy, marker='o', s=20, facecolors='none', edgecolors='r')


def grid_qqplots(dframe, title='QQ-plots', savefig=None, fmt='eps'):
    '''Affichage en grille des QQplot centrés des variables d'une DataFrame'''
    plt.figure(figsize=(8, 6))
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
                plt.text(0.5, 0.5, "\n".join(textwrap.wrap(ix, 20)), dict(size=8),
                         horizontalalignment='center', verticalalignment='center')
            elif iyplot < ixplot:
                # plt.subplots_adjust(left=0.2, hspace=1., wspace=1., top=0.9)
                plt.subplots_adjust(hspace=0.3, wspace=0.3)
                qqplot((dframe[ix] - dframe[ix].mean()) / dframe[ix].std(),
                       (dframe[iy] - dframe[iy].mean()) / dframe[iy].std())
            else:
                plt.axis('off')
    plt.show()
    if savefig:
        typ_fig = 'grid_qqplots'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')


def grid_scatter_plots(dframe, title='Plots', savefig=None, fmt='eps'):
    '''Affichage en grille des figures pyplot.scatter des variables d'une DataFrame'''
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
                plt.text(0.5, 0.5, "\n".join(textwrap.wrap(ix, 20)), dict(size=8),
                         horizontalalignment='center', verticalalignment='center')
            elif iyplot < ixplot:
                # plt.subplots_adjust(left=0.2, hspace=0.8, wspace=0.8, top=0.8)
                plt.subplots_adjust(hspace=0.3, wspace=0.3)
                plt.scatter(dframe[ix], dframe[iy], marker='o', s=20, facecolors='none', edgecolors='r')
            else:
                plt.axis('off')
    plt.show()
    if savefig:
        typ_fig = 'grid_scatter'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')


def myPCA(df):
    '''Calcul PCA sur DataFrame après centrage et réduction des variables'''
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
    '''Cercle des corrélations, à partir du résultat d'une PCA'''
    plt.Circle((0, 0), radius=10, color='g', fill=False)
    plt.figure(figsize=(6, 6))
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


def pca_figs(df, savefig=None, fmt='eps'):
    '''Figures résultat d'une PCA'''
    pca_infos, ebouli, pca_transf, pca = myPCA(df)
    # la projection des individus (centrés et réduits) sur le plan des 2 CP

    # cercle des correlations
    circleOfCorrelations(pca_infos, ebouli)
    # projection des individus: revoir
    # proj_indiv = centreduce_df(df).as_matrix().dot(pca.components_[:, 0:2])
    # plt.scatter(proj_indiv[:, 0], proj_indiv[:, 1], marker='o', s=5, facecolors='none', edgecolors='b')
    plt.scatter(pca_transf[:, 0], pca_transf[:, 1], marker='o', s=5, facecolors='none', edgecolors='b')
    plt.show()
    if savefig:
        typ_fig = 'Corr'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')

    # variance expliquée
    plt.figure()
    scree = pd.Series(pca.explained_variance_ratio_)
    scree.plot(kind='bar', title=u"Part de la variance expliquée par CP")
    np.cumsum(scree).plot(drawstyle="steps-post", color='red', linestyle='--')
    plt.show()
    if savefig:
        typ_fig = 'Var'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')

    # projection sur les 2 composantes principales
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

    # # inerties et variance
    # inerties = pca.explained_variance_  # inertie expliquée par chaque composante principale
    # print("Inertie d'une, deux, trois composantes principales : {}".format(np.cumsum(inerties)))
    # print('valeurs singulieres : {}'.format(np.sqrt(inerties * df.shape[0])))
    # plt.figure()
    # pd.Series(np.sqrt(inerties * df.shape[0])).plot(kind='bar', title=u"Valeurs singulières")
    # plt.show()
    # if savefig:
    #     typ_fig = 'Inert'
    #     plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')
    return pca_infos, ebouli, pca_transf, pca


def Kmeans_figs(ndarr, suptitle='', n_clusters=2, savefig=None, fmt='eps'):
    '''Figures résultat d'un Kmeans'''
    k_means = KMeans(n_clusters=n_clusters, random_state=0)
    k_means.fit(ndarr)
    y_pred = k_means.predict(ndarr)
    fig = plt.figure(figsize=(6, 5))
    fig.suptitle("K-Means clustering {}, K={}".format(suptitle, n_clusters))
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(ndarr[:, 0], ndarr[:, 1], c=y_pred)
    plt.show()
    if savefig:
        typ_fig = 'Kmeans'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')
    return {i: np.where(k_means.labels_ == i)[0] for i in range(k_means.n_clusters)}
    # return {i: ndarr[np.where(k_means.labels_ == i)] for i in range(k_means.n_clusters)}


def clustering_rha(df, seuil, savefig=None, fmt='eps'):
    '''Figures résultat d'un regroupement jiérarchique ascendant'''
    distArray = ssd.squareform(ssd.pdist(df, metric=b'euclidean'))

    # methode plus courte distance
    # plt.figure()
    # linkAverage = linkage(distArray, method=b'single')
    # dendrogram(linkAverage)
    # plt.show()

    # methode de ward
    plt.figure()
    linkAverage = linkage(distArray, method=b'ward')
    dendrogram(linkAverage)
    plt.show()
    if savefig:
        typ_fig = 'rha_tree'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')

    # clusters à partir de méthode de ward
    clusters = fcluster(linkAverage, seuil, criterion=b'distance')
    uniq, unique_indices, unique_inverse, unique_counts = np.unique(clusters, return_counts=True, return_inverse=True,
                                                                    return_index=True)

    # dictionnaire des clusters: une entrée par cluster
    # chaque entrée est associée à la liste des départements qui constituent un cluster particulier
    print('Clusters shape: {}'.format(clusters.shape))
    clusters_dict = dict()
    for clu in uniq:
        clusters_dict[clu] = list()
        for i in range(df.shape[0]):
            if clusters[i] == clu:
                clusters_dict[clu].append(df.index[i])

    ind = np.arange(2)  # les coordonnées des abscisses x des bâtons
    width = 0.35  # largeur des bâtons
    clu_1 = (len(clusters_dict[1]), 0)
    clu_2 = (0, len(clusters_dict[2]))
    plt.figure()
    p1 = plt.bar(ind, clu_1, width, color='r')
    p2 = plt.bar(ind, clu_2, width, color='b', bottom=clu_1)
    plt.title('Nombres de départements dans chaque cluster')
    plt.xticks(ind + width / 2., ('1', '2'))
    plt.legend((p1[0], p2[0]), ('Cluster 1', 'Cluster 2'), loc=0)
    if savefig:
        typ_fig = 'rha_bar'
        plt.savefig("{}_{}.{}".format(savefig, typ_fig, fmt), format='eps')
    return clusters_dict


#####################################################################################""""
#
# Les actions commencent ici
#
#
print('Télécharger le fichier des données (dure quelques minutes) ? ')
if raw_input() == 'O':
    response = urllib2.urlopen(data_file_url)
    dataset_xls = response.read()
    with open(os.path.join(path_data, data_file), b'wb') as f:
        f.write(dataset_xls)

print("Chargement des données en mémoire")
dataset = pd.read_excel(os.path.join(path_data, data_file), sheet_name=data_sheet_name)
df_raw = pd.DataFrame(dataset)
df_raw.set_index(['CODGEO'], inplace=True)
print('-- Shape: {}'.format(df_raw.shape))
print('-- Infos:')
df_raw.info()
df_raw.dtypes
# df_raw.describe()
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
#  Colonne BV : bassin de vie; voir association comunne -> BV
# dans fichier de référence INSEE 2012

# donnée economiques
df_raw_dep_entrep = pd.DataFrame(df_raw, columns=[
    'DEP',
    'Nb Education, santé, action sociale',
    'Nb Entreprises',
    'Nb Création Entreprises',
])
# df_raw_dep_entrep = pd.DataFrame(df_raw, columns=[
#     'DEP',
#     'Nb Education, santé, action sociale',
#     'Nb Entreprises Secteur Services',
#     'Nb Création Services',
#     'Nb Entreprises Secteur Commerce',
#     'Nb Création Commerces',
#     'Nb Entreprises Secteur Construction',
#     'Nb Création Construction',
#     'Nb Entreprises Secteur Industrie',
#     'Nb Création Industrielles',
# ])
# df_raw_dep_entrep = pd.DataFrame(df_raw, columns=[
#     'DEP',
#     'Nb Education, santé, action sociale',
#     'Nb Entreprises serv comm',
#     'Nb Création Entreprises serv comm',
#     'Nb Entreprises cons indus',
#     'Nb Création Entreprises cons indus',
# ])
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

# calcul variable nb communes rurales par département
# del(df_dep_eco['Nb communes rurales'])
print('Ajout variable Nb communes rurales, calculée à partir de Urbanité Ruralité')
sr_dep_rurales = pd.Series([0] * df_dep_entrep.shape[0], dtype=np.int64, index=df_dep_entrep.index)
for icomm in df_raw.index:
    if df_raw.loc[icomm, 'Urbanité Ruralité'] in ['Com rurale < 2 000 m habts', 'Com rurale > 2 000 habts']:
        # print("{} {}".format(df_raw.loc[icomm, 'DEP'], df_raw.loc[icomm, 'Urbanité Ruralité']))
        sr_dep_rurales[df_raw.loc[icomm, 'DEP']] += 1

# ajout nb communes rurales à chacun des DataFrames
df_dep_entrep['Nb communes rurales'] = sr_dep_rurales
df_dep_salaires['Nb communes rurales'] = sr_dep_rurales
df_dep_pop['Nb communes rurales'] = sr_dep_rurales
df_dep_eco['Nb communes rurales'] = sr_dep_rurales
df_dep['Nb communes rurales'] = sr_dep_rurales


# existence de NaN
if df_dep.shape == df_dep.dropna().shape:
    print("Aucun NaN dans le jeu de données")
else:
    print("Existence de NaN dans le jeu de données")
    for col in df_dep.columns.values:
        print('{}: {}'.format(col, df_dep[col].dropna().shape))

# centrage des variables (sans réduction)
print('Calcul DFs centrées')
df_dep_entrep_c = center_df(df_dep_entrep)
df_dep_salaires_c = center_df(df_dep_salaires)
df_dep_pop_c = center_df(df_dep_pop)
df_dep_c = center_df(df_dep)
df_dep_eco_c = center_df(df_dep_eco)


# centrage et reduction des variables
print('Calcul DFs centrées et réduites')
df_dep_entrep_cr = centreduce_df(df_dep_entrep)
df_dep_salaires_cr = centreduce_df(df_dep_salaires)
df_dep_pop_cr = centreduce_df(df_dep_pop)
df_dep_cr = centreduce_df(df_dep)
df_dep_eco_cr = centreduce_df(df_dep_eco)



#######################################################################
# plot 3D sur données salaires
df_dep_salaires.columns.values
scatter3D_fig(df_dep_salaires, cols=['Nb communes rurales',
                                     'Dep Moyenne Salaires Cadre Horaires',
                                     'Dep Moyenne Salaires Ouvrié Horaires'],
              savefig=os.path.join(path_data, 'salaires'))

df_dep_entrep.columns.values
scatter3D_fig(df_dep_entrep, cols=['Nb communes rurales',
                                   'Nb Entreprises',
                                   'Nb Création Entreprises'],
              savefig=os.path.join(path_data, 'entrep_1'))

scatter3D_fig(df_dep_entrep, cols=['Nb communes rurales',
                                   'Nb Education, santé, action sociale',
                                   'Nb Création Entreprises'],
              savefig=os.path.join(path_data, 'entrep_2'))

scatter3D_fig(df_dep_entrep, cols=['Nb Education, santé, action sociale',
                                   'Nb Création Entreprises',
                                   'Nb Création Entreprises'],
              savefig=os.path.join(path_data, 'entrep_3'))

df_dep_pop.columns.values
scatter3D_fig(df_dep_pop, cols=['Nb communes rurales',
                                'Evolution Population %',
                                'Nb Etudiants'],
              savefig=os.path.join(path_data, 'pop_1'))
scatter3D_fig(df_dep_pop, cols=['Nb propriétaire',
                                'Evolution Population %',
                                'Nb Etudiants'],
              savefig=os.path.join(path_data, 'pop_2'))
scatter3D_fig(df_dep_pop, cols=['Nb communes rurales',
                                'Evolution Population %',
                                'Nb propriétaire'],
              savefig=os.path.join(path_data, 'pop_3'))

# plt.close('all')

#######################################################################
# boxplot sur données salaires ni reduites ni centrées

boxplots_figs(df_dep_salaires, savefig=os.path.join(path_data, 'salaires'))
boxplots_figs(df_dep_entrep, savefig=os.path.join(path_data, 'entrep'))
boxplots_figs(df_dep_pop, savefig=os.path.join(path_data, 'pop'))
boxplots_figs(df_dep_eco, savefig=os.path.join(path_data, 'eco'))
# boxplots_figs(df_dep)


#######################################################################
# affichage des plots N x N
grid_qqplots(df_dep_salaires, 'QQ-plots variables salaires', savefig=os.path.join(path_data, 'salaires'))
grid_qqplots(df_dep_entrep, 'QQ-plots variables entreprises', savefig=os.path.join(path_data, 'entrep'))
grid_qqplots(df_dep_pop, 'QQ-plots démographie', savefig=os.path.join(path_data, 'pop'))

grid_scatter_plots(df_dep_salaires, 'Plots variables salaires', savefig=os.path.join(path_data, 'salaires'))
grid_scatter_plots(df_dep_entrep, 'Plots variables entreprises', savefig=os.path.join(path_data, 'entrep'))
grid_scatter_plots(df_dep_pop, 'Plots démographie', savefig=os.path.join(path_data, 'pop'))

# grid_scatter_plots(df_dep_pop.iloc[:, :3], 'Démographie')
# grid_scatter_plots(df_dep_pop, 'Démographie')
# grid_scatter_plots(df_dep_entrep, 'Entreprises')


#######################################################################
# PCA sur données salaires reduites centrées
pca_salaires = dict()
pca_salaires['pca_infos'], \
pca_salaires['ebouli'], \
pca_salaires['pca_transf'], \
pca_salaires['pca'] = \
    pca_figs(df_dep_salaires, savefig=os.path.join(path_data, 'salaires'))

# revoir correction, semble incorrecte
# proj_indiv = df_dep_salaires_cr.as_matrix().dot(pca_salaires['pca'].components_[:, 0:2])
# proj_indiv.shape
# plt.figure()
# plt.scatter(proj_indiv[:, 0], proj_indiv[:, 1], marker='o', s=5, facecolors='none', edgecolors='b')
# plt.show()

pca_entrep = dict()
pca_entrep['pca_infos'], \
pca_entrep['ebouli'], \
pca_entrep['pca_transf'], \
pca_entrep['pca'] = \
    pca_figs(df_dep_entrep, savefig=os.path.join(path_data, 'entrep'))

# pour trouver l'indice (département) de l'individu le plus à l'écart sur la projection 2CP
np.argmax(pca_entrep['pca_transf'][:,0])

pca_pop = dict()
pca_pop['pca_infos'], \
pca_pop['ebouli'], \
pca_pop['pca_transf'], \
pca_pop['pca'] = \
    pca_figs(df_dep_pop, savefig=os.path.join(path_data, 'pop'))



#######################################################################
# calcul PCA sur données complètes
pca_dep = dict()
pca_dep['pca_infos'], \
pca_dep['ebouli'], \
pca_dep['pca_transf'], \
pca_dep['pca'] = \
    pca_figs(df_dep, os.path.join(path_data, 'toutes_var'))


########################################################################################
# K-means clustering: données après PCA

dep_kmeans_clusters_salaires = Kmeans_figs(pca_salaires['pca_transf'], 'on PCA-reduced', n_clusters=3,
                                           savefig=os.path.join(path_data, 'salaires'))
#  liste des départements avec les saiaires les plus élevés
[df_dep_salaires.index[i] for i in dep_kmeans_clusters_salaires[2]]

# dep_kmeans_clusters_salaires_cr = Kmeans_figs(np.array(df_dep_salaires_cr), 'on salaires CR', n_clusters=3,
#                                               savefig=os.path.join(path_data, 'salaires_cr'))
dep_kmeans_clusters_entrep = Kmeans_figs(pca_entrep['pca_transf'], 'on PCA-reduced', n_clusters=3,
                                         savefig=os.path.join(path_data, 'entrep'))
dep_kmeans_clusters_pop = Kmeans_figs(pca_pop['pca_transf'], 'on PCA-reduced', n_clusters=3,
                                      savefig=os.path.join(path_data, 'pop'))



########################################################################################
# Regroupement hiérarchique ascendant

dep_rha_clusters_salaires = clustering_rha(df_dep_salaires_cr, seuil=100.,
                                           savefig=os.path.join(path_data, 'salaires'))
dep_rha_clusters_entrep = clustering_rha(df_dep_entrep_cr, seuil=140.,
                                         savefig=os.path.join(path_data, 'entrep'))
dep_rha_clusters_pop = clustering_rha(df_dep_pop_cr, seuil=100.,
                                      savefig=os.path.join(path_data, 'pop'))
