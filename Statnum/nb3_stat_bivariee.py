# coding=utf-8


# docs sur Pandas: https://pandas.pydata.org/pandas-docs/stable/api.html


# %matplotlib nbagg # pour IPython et Jupyter
# %matplotlib nbagg # pour IPython et Jupyter
# %matplotlib Qt5Agg # pour PyCharm, essayer avec Jupyter

import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from IPython.display import display, Math, Latex

vins = load_wine()
Data = pd.DataFrame(vins['data'],columns=vins['feature_names'])
Data['class'] = vins['target']

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


def moment_1(freq):
    mean = 0.
    for key, value in freq.dropna().iteritems():
        mean += np.double(value)*key
    return mean/freq.count()


def moment_centre(freq,r):
    mean = moment_1(freq)
    moment_r = 0.
    for key, value in freq.dropna().iteritems():
        moment_r += np.double(value)*(key-mean)**r
    return moment_r/freq.count()

