# coding=utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# réutilisation de la fonction qqplot du TD NB2_figures.ipynb
def qqplot(x, y):
    m = min([x.size, y.size])
    alpha = np.linspace(1. / float(m), 1., m)
    qx = x.quantile(alpha)
    qy = y.quantile(alpha)
    plt.scatter(qx, qy, marker='o', s=40, facecolors='none', edgecolors='r')
    # plt.plot(qx, qx, '--')


def fdr(t, obs):
    # t : vecteur de points ou on veut evaluer la fdr
    # obs : Series avec les observations
    y = pd.Series(np.arange(0., len(t), 1))
    for i in range(len(t)):
        y[i] = (obs <= t[i]).mean()     # moyenne de booléens: True=1, False=0
    return y


obs = pd.Series([5, 2, 4, 2, 7, 5.])
t = [2., .4, 5]
fdr(t, obs)

pd.Series([True, True, True]).mean()
pd.Series([False, False, False]).mean()
pd.Series([True, True, False]).mean()
type((obs <= 2.))
(obs <= 2.).shape
(obs <= 2.).mean()

obs[obs <= 2.]
obs[obs <= 2.].mean()
