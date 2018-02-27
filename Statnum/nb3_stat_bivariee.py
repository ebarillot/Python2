# coding=utf-8


# docs sur Pandas: https://pandas.pydata.org/pandas-docs/stable/api.html


# %matplotlib nbagg # pour IPython et Jupyter
# %matplotlib nbagg # pour IPython et Jupyter
# %matplotlib Qt5Agg # pour PyCharm, essayer avec Jupyter

# import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, Math, Latex

# from sklearn.datasets import load_wine
# vins = load_wine()
# Data = pd.DataFrame(vins['data'],columns=vins['feature_names'])
# Data['class'] = vins['target']
# print(vins['DESCR'])

import os

if os.path.basename(os.getcwd()) != 'Statnum':
    os.chdir('./Statnum')
Data = pd.read_csv('vins.csv', sep=';')
print('-- Shape: {}'.format(Data.shape))
# print(Data.dtypes)
# print(Data.index)
print('-- Infos:')
Data.info()
print('-- Infos END --')
# Data.describe()


flavanoids_serie = Data.sort_values(by='flavanoids')['flavanoids']
# print(np.percentile(flavanoids_serie, q=range(1,100+1)))
# print(flavanoids_serie.count()==flavanoids_serie.size)

q25 = np.percentile(flavanoids_serie, 25)
# Math('q_{{25}}={}'.format(q25))

q75 = np.percentile(flavanoids_serie, 75)
# Math('q_{{75}}={}'.format(q75))

eiq2575 = q75 - q25
# Math('\Delta=q_{{75}}-q_{{25}}={}'.format(eiq2575))

# plt.figure()
# pd.DataFrame(flavanoids_serie).boxplot()
# plt.show()

# quantiles
# m = min([x.size, y.size])
# alpha = np.linspace(1. / float(m), 1., m)
# qx = x.quantile(alpha)
# qy = y.quantile(alpha)
flavanoids_serie.quantile(.25)
flavanoids_serie.quantile(.75)

flavanoids_freq = flavanoids_serie.value_counts() / flavanoids_serie.size
print('-- flavanoids_freq:')
print(flavanoids_freq)
print('Somme freq: {}'.format(flavanoids_freq.sum()))
print('-- END --')


def freq_nvars(dframe, varlist):
    """
    :param dframe: DateFrame
    :param varlist: liste des variables jointes
    :return: retourne un tableau 2D de fréquences jointes sur les variables var1 et var2
    """
    return dframe[varlist].groupby(varlist).size() / len(dframe)


def freq_nvars_filters(dframe, filters, varlist):
    """
    :param dframe: DateFrame
    :param filters: dictionnaire de filtres; chaque filtre contient une série (panda) de booleen de la longueur
     de la DataFrame
    :param varlist: liste des variables dont on veut calculer les fréquences jointes
    :return: retourne un dictionnaire de tableaux nD de fréquences jointes sur les variables de la varlist
    un tableau par filtre
    les clés du dictionnaire sont celles du dictionnaire de filtres
    """
    return dict( [ (filter_name, freq_nvars(dframe.loc[filter_values], varlist))
                    for filter_name, filter_values in filters.iteritems() ] )


def freq_var1_by_var2(dframe, var1, by_var2):
    """ fonction qui calcule un tableau de fréquences conditionnelles à partir d'une DataFrame
    :param dframe:
    :param var1:
    :param by_var2:
    :return:
    """
    by_var_unique = dframe[by_var2].unique()
    distrib_by_var = dict(
        [(x, dframe.loc[dframe[by_var2] == x, [by_var2, var1]][var1].value_counts()) for x in by_var_unique])
    size_by_var = dict([(x, dframe.loc[dframe[by_var2] == x, [by_var2, var1]][var1].size) for x in by_var_unique])
    freq_by_var = dict(
        [(x, distrib_by_var[x] / size_by_var[x]) for x in by_var_unique])
    return freq_by_var


def moment_centre(freq, r=1):
    """
    Calcule le moment centré d'ordre r
    :param freq: tableau des fréquences sous la forme d'une DataFrame panda de lignes (valeurs, fréquence)
    :param r: ordre
    :return: la valeur du moement centré
    """
    freq_dropna = freq.dropna()
    freq_index = freq_dropna.index
    freq_values = freq_dropna.values
    freq_list = zip(freq_index, freq_values)
    moment_1 = reduce(lambda x, y: x + y, map(lambda (x, y): x * y, freq_list))
    if r == 1:
        moment_r = moment_1
    else:
        moment_r = reduce(lambda x, y: x + y, map(lambda (x, y): ((x - moment_1) ** r) * y, freq_list))
    return round(moment_r, 6)


print('flavanoids_serie mean:     {}'.format(flavanoids_serie.mean()))
print('flavanoids_serie moment_1: {}'.format(moment_centre(flavanoids_freq)))
print('flavanoids_serie var:      {}'.format(flavanoids_serie.var(ddof=0)))
print('flavanoids_serie moment_2: {}'.format(moment_centre(flavanoids_freq, 2)))

mom_1 = reduce(lambda x, y: x + y, map((lambda (x, y): x * y), zip(flavanoids_freq.index, flavanoids_freq.values)))
print('mom_1: {}:'.format(mom_1))

mom_2 = reduce(lambda x, y: x + y,
               map((lambda (x, y): (x - mom_1) ** 2 * y), zip(flavanoids_freq.index, flavanoids_freq.values)))
print('mom_2: {}:'.format(mom_2))


# (6). Calculez la moyenne conditionnelle et la variance conditionnelle de la variable alcohol
#  sachant que la variable class vaut 0, 1 et 2. Interpretez les résultats.

class_alcohol = Data[['class', 'alcohol']]
alcohol_freq_by_class = freq_var1_by_var2(class_alcohol, var1='alcohol', by_var2='class')

alcohol_mean_by_class = [(x, moment_centre(alcohol_freq_by_class[x])) for x in class_alcohol['class'].unique()]
alcohol_var_by_class = [(x, moment_centre(alcohol_freq_by_class[x], 2)) for x in class_alcohol['class'].unique()]
print('Alcohol by class, moyenne:')
print(pd.DataFrame(alcohol_mean_by_class, index=[''] * len(alcohol_mean_by_class), columns=['class', 'alcohol']))
print('Alcohol by class, variance:')
print(pd.DataFrame(alcohol_var_by_class, index=[''] * len(alcohol_mean_by_class), columns=['class', 'alcohol']))

# Du point de vue du degré alcoolique, les vins semblent différents.


# (7). Affichez sur une même figure l'histogramme de la distribution de la variable alcohol sachant que
#  la variable class vaut 0, 1 et 2 (conseil: utilisez le paramètre alpha de la fonction hist pour mieux
#  voir les superpositions). En quoi cette représentation graphique confirme vos précédents résultats ?

def hist_var1_by_var2(dframe, var1, by_var2, title=None, xlabel=None, ylabel=None):
    """
    Affiche les histogrammes superposés de la distribution de la variable var1 en fonction des valeurs
    de la variable by_var2; il y a un histogramme par valeur de la variable by_var2.
    """
    by_var2_unique = np.sort(dframe[by_var2].unique())
    bins = max([dframe.loc[dframe[by_var2] == cl, var1].value_counts().size for cl in by_var2_unique])
    plt.figure()
    for idx in by_var2_unique:
        plt.hist(dframe.loc[dframe[by_var2] == by_var2_unique[idx], var1], bins, alpha=0.7, normed=True)
    legends = ['{} {}'.format(by_var2, cl) for cl in by_var2_unique]
    plt.legend(legends)
    plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)


# histogrammes de la distribution de 'alcohol' en fonction des valeurs de 'class'
hist_var1_by_var2(Data, var1='alcohol', by_var2='class', title='Histogramme alcool', xlabel=u"Degré alcool")
plt.close('all')

# cette représentation graphique confirme que les vins des producteurs sont différentsdu point de vue du degré d'alcool


# (8). Calculez les fréquences de la variable alcohol pour les intervalles (10.,12.5], (12.5,13.5] et (13.5,15.]
#  sachant que la variable class vaut 0, 1 et 2. (La notation (a,b] signifie que l'intervalle est ouvert à gauche
#  et fermé à droite)

#  Vision: découpage de la population par intervalle de la variable 'alcohol'
# on construit un dictionnaire des filtres à partir des intervalles de valeur d'alcool
alcohol_filters = {
    '(10.,12.5]': (Data['alcohol'] > 10.) & (Data['alcohol'] <= 12.5),
    '(12.5,13.5]': (Data['alcohol'] > 12.5) & (Data['alcohol'] <= 13.5),
    '(13.5,15.]': (Data['alcohol'] > 13.5) & (Data['alcohol'] <= 15.)
    }

# calcul d'un tableau de fréquences par valeur de filtre
# => tableau à 2D: 'class' x 'alcohol'
alcohol_subserie_freq = freq_nvars_filters(Data, alcohol_filters, ['class', 'alcohol'])

# controle de la somme des fréquences
for idx in alcohol_subserie_freq.keys():
    print('filter {}, {} values, sum={}'.format(idx, len(alcohol_subserie_freq[idx]), alcohol_subserie_freq[idx].sum()))


#  Vision: classes / intervalles de la variable 'alcohol' => réduction de la population
for alc in alcohol_filters.keys():
    for cl in Data['class'].unique():
        print alc, cl, Data.loc[(alcohol_filters[alc]) & (Data['class']==cl)].index.size


def alcohol_interval(val):
    if val>10. and val <= 12.5:
        return '(10.,12.5]'
    elif val>12.5 and val <= 13.5:
        return '(12.5.,13.5]'
    elif val>13.5 and val <= 15.:
        return '(13.5.,15.]'

# il faut bien créer une nouvelle instance de DF, sinon sans pd.DataFrame(),
#  Data2 est un slice logique sur Data et python refuse d'appliquer une réaffectation de la colonne alcohol
Data2 = pd.DataFrame(Data[['class','alcohol']])
Data2['alcohol'] = Data2['alcohol'].map(alcohol_interval)
Data2.groupby(['class','alcohol']).size()
alcohol_subserie_freq = Data2.groupby(['class','alcohol']).size() / len(Data2)
alcohol_subserie_freq.rename('freq',inplace=True)
type(alcohol_subserie_freq)
alcohol_subserie_freq.name

# df = pd.DataFrame([{'a': 15, 'b': 15, 'c': 5}, {'a': 20, 'b': 10, 'c': 7}, {'a': 25, 'b': 30, 'c': 9}])
# df['a'] = df['a'].map(lambda a: a / 2.)



# (9). Affichez le nuage de points des variables flavanoids et total_phenols et le nuage de points
#  des variables flavanoids et nonflavanoid_phenols sur des figures différentes (mais dans une même fenêtre).
#  Interpretez ces deux graphiques.

# Data[['flavanoids','total_phenols']]
# fig = 2
# plt.figure(fig)
plt.figure()
plt.subplot(121)
plt.title('scatter flavanoids vs. total_phenols')
plt.scatter(Data['flavanoids'], Data['total_phenols'], marker='o', s=50, facecolors='none', edgecolors='r')
plt.subplot(122)
plt.title('scatter flavanoids vs. nonflavanoid_phenols')
plt.scatter(Data['flavanoids'], Data['nonflavanoid_phenols'], marker='o', s=50, facecolors='none', edgecolors='r')
# plt.close(fig)


# réutilisation de la fonction qqplot du TD NB2_figures.ipynb
def qqplot(x, y):
    m = min([x.size, y.size])
    alpha = np.linspace(1. / float(m), 1., m)
    qx = x.quantile(alpha)
    qy = y.quantile(alpha)
    plt.scatter(qx, qy, marker='o', s=40, facecolors='none', edgecolors='r')
    # plt.plot(qx, qx, '--')


# fig = 3
# plt.figure(fig)
plt.figure()
plt.subplot(121)
plt.title('qqplot flavanoids \nvs. total_phenols')
qqplot(Data['flavanoids'], Data['total_phenols'])
plt.subplot(122)
plt.title('qqplot flavanoids \nvs. nonflavanoid_phenols')
qqplot(Data['flavanoids'], Data['nonflavanoid_phenols'])
# plt.close(fig)


# sur variables réduites
# fig = 4
# plt.figure(fig)
plt.figure()
plt.subplot(121)
plt.title('qqplot flavanoids \nvs. total_phenols normalized')
qqplot((Data['flavanoids'] - Data['flavanoids'].mean()) / Data['flavanoids'].std(),
       (Data['total_phenols'] - Data['total_phenols'].mean()) / Data['total_phenols'].std())
plt.subplot(122)
plt.title('qqplot flavanoids \nvs. nonflavanoid_phenols normalized')
qqplot((Data['flavanoids'] - Data['flavanoids'].mean()) / Data['flavanoids'].std(),
       (Data['nonflavanoid_phenols'] - Data['nonflavanoid_phenols'].mean()) / Data['nonflavanoid_phenols'].std())
# plt.close(fig)


# (10). Quelle statistique utiliseriez-vous pour justifier votre réponse à la question précédente ?
#  Justifiez votre choix et calculez la valeur de cette statistique pour les deux cas.
# ==> corrélation

Data[['flavanoids','total_phenols']]
Data[['flavanoids','nonflavanoid_phenols']].sort_values(by='flavanoids')

round(Data['flavanoids'].corr(Data['total_phenols']),6)
# => correlation 0.864564

round(Data['flavanoids'].corr(Data['nonflavanoid_phenols']),6)
# => correlation -0.537900

Data['flavanoids'].cov(Data['total_phenols'])
Data['flavanoids'].cov(Data['nonflavanoid_phenols'])

# quantiles
m=20
Data['flavanoids'].quantile(np.linspace(1. / float(m), 1., m))
Data['total_phenols'].quantile(np.linspace(1. / float(m), 1., m))
Data['nonflavanoid_phenols'].quantile(np.linspace(1. / float(m), 1., m))


# (11). À partir des résultats de la question 8, comment feriez-vous pour calculer la distribution jointe
#  des variables alcohol et class ? (où les valeurs sont 0, 1 et 2 pour la variable class et
#  les intervalles (10.,12.5], (12.5,13.5] et (13.5,15.] pour la variable alcohol)
#  Calculez cette distribution jointe. Faites le produit entre la distribution marginale de la variable
# alcohol et celle de la variable class. Qu'est-ce que vous en concluez ?

alcohol_subserie_freq
alcohol_subserie_freq.reset_index()
alcohol_subserie_freq.reset_index().index

# controle de la somme des fréquences
alcohol_subserie_freq.cumsum()


# => variables indépendantes ?

