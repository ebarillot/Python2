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
# os.chdir('./Statnum')
Data = pd.read_csv('vins.csv', sep=';')
print(Data.shape)
print(Data.dtypes)
print(Data.index)
Data.info()
Data.describe()


flavanoids_serie = Data.sort_values(by='flavanoids')['flavanoids']
print(np.percentile(flavanoids_serie, q=range(1,100+1)))
print(flavanoids_serie.count()==flavanoids_serie.size)

q25 = np.percentile(flavanoids_serie,25)
# Math('q_{{25}}={}'.format(q25))

q75 = np.percentile(flavanoids_serie,75)
# Math('q_{{75}}={}'.format(q75))

eiq2575=q75-q25
# Math('\Delta=q_{{75}}-q_{{25}}={}'.format(eiq2575))

# plt.figure()
# pd.DataFrame(flavanoids_serie).boxplot()
# plt.show()

flavanoids_freq = flavanoids_serie.value_counts()/flavanoids_serie.size
print(flavanoids_freq)


# def moment_1(freq):
#     mean = 0.
#     for value, nb in freq.dropna().iteritems():
#         mean += np.double(nb)*value
#     return mean


# def moment_centre(freq,r):
#     mean = moment_1(freq)
#     moment_r = 0.
#     for value, nb in freq.dropna().iteritems():
#         moment_r += np.double(nb)*(value-mean)**r
#     return moment_r


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
    return round(moment_r,3)

print('mean: {}'.format(flavanoids_serie.mean()))
print('moment_1: {}'.format(moment_centre(flavanoids_freq)))
print('var: {}'.format(flavanoids_serie.var(ddof=0)))
print('moment_2: {}'.format(moment_centre(flavanoids_freq,2)))

# print(flavanoids_freq.dropna().apply(lambda x: x*x))
# map((lambda (x,y): x*y), zip(flavanoids_freq.index,flavanoids_freq.values))
mom_1 = reduce(lambda x,y: x+y, map((lambda (x,y): x*y), zip(flavanoids_freq.index,flavanoids_freq.values)))
print(mom_1)

mom_2 = reduce(lambda x,y: x+y, map((lambda (x,y): (x-mom_1)**2 *y), zip(flavanoids_freq.index,flavanoids_freq.values)))
print(mom_2)

# (6). Calculez la moyenne conditionnelle et la variance conditionnelle de la variable alcohol
#  sachant que la variable class vaut 0, 1 et 2. Interpretez les résultats.

class_unique = Data['class'].unique()
alcohol_distrib_by_class = dict([(x, Data.loc[Data['class']==x,['class','alcohol']]['alcohol'].value_counts()) for x in class_unique])
alcohol_size_by_class = dict([(x, Data.loc[Data['class']==x,['class','alcohol']]['alcohol'].size) for x in class_unique])
alcohol_freq_by_class = dict([(x, alcohol_distrib_by_class[x]/alcohol_size_by_class[x]) for x in class_unique])

alcohol_mean_by_class = [(x,moment_centre(alcohol_distrib_by_class[x]/alcohol_size_by_class[x])) for x in class_unique]
alcohol_var_by_class  = [(x, moment_centre(alcohol_distrib_by_class[x]/alcohol_size_by_class[x],2)) for x in class_unique]
print(alcohol_mean_by_class)
print(alcohol_var_by_class)

# (8). Calculez les fréquences de la variable alcohol pour les intervalles (10.,12.5], (12.5,13.5] et (13.5,15.]
#  sachant que la variable class vaut 0, 1 et 2. (La notation (a,b] signifie que l'intervalle est ouvert à gauche
#  et fermé à droite)

# Data[['class','alcohol']]
# alcohol_serie_a = Data.loc[Data['alcohol']>10 & Data['alcohol']<=12.5, ['class','alcohol']]
alcohol_serie_a = Data.loc[(Data['alcohol']>10)&(Data['alcohol']<=12.5), ['class','alcohol']]
print(alcohol_serie_a)

alcohol_serie_b = Data.loc[(Data['alcohol']>12.5)&(Data['alcohol']<=13.5), ['class','alcohol']]
print(alcohol_serie_b)

alcohol_serie_c = Data.loc[(Data['alcohol']>13.5)&(Data['alcohol']<=15), ['class','alcohol']]
print(alcohol_serie_c)

alcohol_a_distrib_by_class = dict([(x, alcohol_serie_a.loc[alcohol_serie_a['class']==x,['class','alcohol']]['alcohol'].value_counts()) for x in class_unique])
alcohol_a_size_by_class = dict([(x, alcohol_serie_a.loc[alcohol_serie_a['class']==x,['class','alcohol']]['alcohol'].size) for x in class_unique])
alcohol_a_freq_by_class = dict([(x, alcohol_a_distrib_by_class[x]/alcohol_a_size_by_class[x]) for x in class_unique])

alcohol_b_distrib_by_class = dict([(x, alcohol_serie_b.loc[alcohol_serie_b['class']==x,['class','alcohol']]['alcohol'].value_counts()) for x in class_unique])
alcohol_b_size_by_class = dict([(x, alcohol_serie_b.loc[alcohol_serie_b['class']==x,['class','alcohol']]['alcohol'].size) for x in class_unique])
alcohol_b_freq_by_class = dict([(x, alcohol_b_distrib_by_class[x]/alcohol_b_size_by_class[x]) for x in class_unique])

alcohol_c_distrib_by_class = dict([(x, alcohol_serie_c.loc[alcohol_serie_c['class']==x,['class','alcohol']]['alcohol'].value_counts()) for x in class_unique])
alcohol_c_size_by_class = dict([(x, alcohol_serie_c.loc[alcohol_serie_c['class']==x,['class','alcohol']]['alcohol'].size) for x in class_unique])
alcohol_c_freq_by_class = dict([(x, alcohol_c_distrib_by_class[x]/alcohol_c_size_by_class[x]) for x in class_unique])
print(alcohol_a_freq_by_class)
print(alcohol_b_freq_by_class)
print(alcohol_c_freq_by_class)
