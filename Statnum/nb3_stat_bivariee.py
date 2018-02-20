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

Data = pd.read_csv('vins.csv')

# print(vins['DESCR'])
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

flavanoids_freq = flavanoids_serie.value_counts()
print(flavanoids_freq)


# def moment_1(freq):
#     mean = 0.
#     nbtot = 0
#     for value, nb in freq.dropna().iteritems():
#         mean += np.double(nb)*value
#         nbtot += nb
#     return mean/np.double(nbtot)


# def moment_centre(freq,r):
#     mean = moment_1(freq)
#     moment_r = 0.
#     nbtot = 0
#     for value, nb in freq.dropna().iteritems():
#         moment_r += np.double(nb)*(value-mean)**r
#         nbtot += nb
#     return moment_r/np.double(nbtot)


def moment_centre(freq,r=1):
    def moment_1(freq):
        mean = 0.
        nbtot = 0
        for value, nb in freq.dropna().iteritems():
            mean += np.double(nb) * value
            nbtot += nb
        return mean / np.double(nbtot)
    mean = moment_1(freq)
    if r == 1:
        return mean
    mean = moment_1(freq)
    moment_r = 0.
    nbtot = 0
    for value, nb in freq.dropna().iteritems():
        moment_r += np.double(nb)*(value-mean)**r
        nbtot += nb
    return moment_r/np.double(nbtot)

print('mean: {}'.format(flavanoids_serie.mean()))
print('moment_1: {}'.format(moment_centre(flavanoids_freq)))
print('var: {}'.format(flavanoids_serie.var(ddof=0)))
print('moment_2: {}'.format(moment_centre(flavanoids_freq,2)))
