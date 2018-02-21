# coding=utf-8


# docs sur Pandas: https://pandas.pydata.org/pandas-docs/stable/api.html


# %matplotlib nbagg # pour IPython et Jupyter
# %matplotlib nbagg # pour IPython et Jupyter
# %matplotlib Qt5Agg # pour PyCharm, essayer avec Jupyter

import matplotlib
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

q25 = np.percentile(flavanoids_serie,25)
# Math('q_{{25}}={}'.format(q25))

q75 = np.percentile(flavanoids_serie,75)
# Math('q_{{75}}={}'.format(q75))

eiq2575=q75-q25
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


flavanoids_freq = flavanoids_serie.value_counts()/flavanoids_serie.size
print('-- flavanoids_freq:')
print(flavanoids_freq)
print('Somme freq: {}'.format(flavanoids_freq.sum()))
print('-- END --')


def freq_var1_by_var2(dframe, var1, by_var2):
    by_var_unique = dframe[by_var2].unique()
    distrib_by_var = dict(
        [(x, dframe.loc[dframe[by_var2] == x, [by_var2, var1]][var1].value_counts()) for x in by_var_unique])
    size_by_var = dict([(x, dframe.loc[dframe[by_var2] == x, [by_var2, var1]][var1].size) for x in by_var_unique])
    freq_by_var = dict(
        [(x, distrib_by_var[x] / size_by_var[x]) for x in by_var_unique])
    return freq_by_var


def moment_centre(freq, r=1):
    freq_dropna = freq.dropna()
    freq_index = freq_dropna.index
    freq_values = freq_dropna.values
    freq_list = zip(freq_index, freq_values)
    moment_1 = reduce(lambda x, y: x + y, map(lambda (x, y): x * y, freq_list))
    if r == 1:
        moment_r = moment_1
    else:
        moment_r = reduce(lambda x, y: x + y, map(lambda (x, y): ((x-moment_1)**r) * y, freq_list))
    return round(moment_r,6)


print('flavanoids_serie mean:     {}'.format(flavanoids_serie.mean()))
print('flavanoids_serie moment_1: {}'.format(moment_centre(flavanoids_freq)))
print('flavanoids_serie var:      {}'.format(flavanoids_serie.var(ddof=0)))
print('flavanoids_serie moment_2: {}'.format(moment_centre(flavanoids_freq,2)))

mom_1 = reduce(lambda x,y: x+y, map((lambda (x,y): x*y), zip(flavanoids_freq.index,flavanoids_freq.values)))
print('mom_1: {}:'.format(mom_1))

mom_2 = reduce(lambda x,y: x+y, map((lambda (x,y): (x-mom_1)**2 *y), zip(flavanoids_freq.index,flavanoids_freq.values)))
print('mom_2: {}:'.format(mom_2))

# (6). Calculez la moyenne conditionnelle et la variance conditionnelle de la variable alcohol
#  sachant que la variable class vaut 0, 1 et 2. Interpretez les résultats.

# class_unique = Data['class'].unique()
# alcohol_distrib_by_class = dict([(x, Data.loc[Data['class']==x,['class','alcohol']]['alcohol'].value_counts()) for x in class_unique])
# alcohol_size_by_class = dict([(x, Data.loc[Data['class']==x,['class','alcohol']]['alcohol'].size) for x in class_unique])
# alcohol_freq_by_class = dict([(x, alcohol_distrib_by_class[x]/alcohol_size_by_class[x]) for x in class_unique])
class_alcohol = Data[['class','alcohol']]
alcohol_freq_by_class = freq_var1_by_var2(class_alcohol, var1='alcohol', by_var2='class')

alcohol_mean_by_class = [(x,moment_centre(alcohol_freq_by_class[x]))    for x in class_alcohol['class'].unique()]
alcohol_var_by_class  = [(x, moment_centre(alcohol_freq_by_class[x],2)) for x in class_alcohol['class'].unique()]
print('Alcohol by class, moyenne:')
print(pd.DataFrame(alcohol_mean_by_class, index=['']*len(alcohol_mean_by_class), columns=['class','alcohol']))
print('Alcohol by class, variance:')
print(pd.DataFrame(alcohol_var_by_class, index=['']*len(alcohol_mean_by_class), columns=['class','alcohol']))

# Du point de vue du degré alcoolique, les vins semblent différents.

# (7). Affichez sur une même figure l'histogramme de la distribution de la variable alcohol sachant que
#  la variable class vaut 0, 1 et 2 (conseil: utilisez le paramètre alpha de la fonction hist pour mieux
#  voir les superpositions). En quoi cette représentation graphique confirme vos précédents résultats ?
# plt.figure()

plt.hist((Data.loc[Data['class'] == 0]['alcohol'],
          Data.loc[Data['class'] == 1]['alcohol'],
          Data.loc[Data['class'] == 2]['alcohol']),
         normed=True, bins=20)
plt.legend(["class 0", "class 1", "class 2"])
plt.title("Histogramme alcool")
plt.xlabel(u"Degré alcool")
plt.close('all')

# cette représentation graphique confirme que les vins des producteurs sont différentsdu point de vue du degré d'alcool


# (8). Calculez les fréquences de la variable alcohol pour les intervalles (10.,12.5], (12.5,13.5] et (13.5,15.]
#  sachant que la variable class vaut 0, 1 et 2. (La notation (a,b] signifie que l'intervalle est ouvert à gauche
#  et fermé à droite)

alcohol_subserie = {}
alcohol_subserie['(10.,12.5]']  = Data.loc[(Data['alcohol']>10.)&(Data['alcohol']<=12.5), ['class','alcohol']]
alcohol_subserie['(12.5,13.5]'] = Data.loc[(Data['alcohol']>12.5)&(Data['alcohol']<=13.5), ['class','alcohol']]
alcohol_subserie['(13.5,15.]']  = Data.loc[(Data['alcohol']>13.5)&(Data['alcohol']<=15), ['class','alcohol']]

alcohol_subserie_freq = dict([ (x, freq_var1_by_var2(alcohol_subserie[x], 'alcohol', 'class')) for x in alcohol_subserie.keys() ])
[alcohol_subserie_freq[x][cl].sum() for x in alcohol_subserie_freq.keys() for cl in alcohol_subserie_freq[x].keys()]


# (9). Affichez le nuage de points des variables flavanoids et total_phenols et le nuage de points
#  des variables flavanoids et nonflavanoid_phenols sur des figures différentes (mais dans une même fenêtre).
#  Interpretez ces deux graphiques.

# Data[['flavanoids','total_phenols']]
fig = 2
plt.figure(fig)
plt.subplot(121)
plt.scatter(Data['flavanoids'], Data['total_phenols'], marker='o',s=50, facecolors='none', edgecolors='r')
plt.subplot(122)
plt.scatter(Data['flavanoids'], Data['nonflavanoid_phenols'], marker='o',s=50, facecolors='none', edgecolors='r')
plt.close(fig)


# réutilisation de la fonction qqplot du TD NB2_figures.ipynb
def qqplot(x, y):
    m = min([x.size,y.size])
    alpha = np.linspace(1./float(m),1.,m)
    qx = x.quantile(alpha)
    qy = y.quantile(alpha)
    plt.scatter(qx, qy, marker='o',s=40, facecolors='none', edgecolors='r')
    plt.plot(qx, qx, '--')



fig = 3
plt.figure(fig)
plt.subplot(121)
qqplot(Data['flavanoids'], Data['total_phenols'])
plt.subplot(122)
qqplot(Data['flavanoids'], Data['nonflavanoid_phenols'])
plt.close(fig)

# sur variables réduites
fig = 4
plt.figure(fig)
plt.subplot(121)
qqplot((Data['flavanoids']-Data['flavanoids'].mean())/Data['flavanoids'].std(),
       (Data['total_phenols']-Data['total_phenols'].mean())/Data['total_phenols'].std())
plt.subplot(122)
qqplot((Data['flavanoids']-Data['flavanoids'].mean())/Data['flavanoids'].std(),
       (Data['nonflavanoid_phenols']-Data['nonflavanoid_phenols'].mean())/Data['nonflavanoid_phenols'].std())
plt.close(fig)




# (10). Quelle statistique utiliseriez-vous pour justifier votre réponse à la question précédente ?
#  Justifiez votre choix et calculez la valeur de cette statistique pour les deux cas.
# ==> matrice de corrélation


