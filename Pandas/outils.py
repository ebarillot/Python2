# coding=utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# réutilisation de la fonction qqplot du TD NB2_figures.ipynb
def qqplot(x, y):
    """
    Affiche le qqplot de deux variables transmises sous la forme de deux séries
    :param x: une variable (série)
    :param y: une autre variable (série statistique)
    :return: None
    """
    m = min([x.size, y.size])
    alpha = np.linspace(1. / float(m), 1., m)
    qx = x.quantile(alpha)
    qy = y.quantile(alpha)
    plt.scatter(qx, qy, marker='o', s=40, facecolors='none', edgecolors='r')
    # plt.plot(qx, qx, '--')


# représentation de 2 séries sur une graphique 2D
xvar = pd.Series(np.random.randn(1000))
yvar = pd.Series(np.random.exponential(1,500))
plt.figure()
qqplot(xvar, yvar)
plt.show()
plt.close()

# représentation de 2 variables stockées dans une DF, sur une graphique 2D
X2 = pd.DataFrame(np.random.randn(1000,2), columns=['x','y'])
plt.figure()
qqplot(X2['x'], X2['y'])
plt.show()
plt.close()


def fdr(t, obs):
    """
    Evaluation de la fonction de répartition (fdr empirique) à partir d'une série d'observations
    et d'une liste de valeurs en lesquelles on veut évaluer la fdr.
    :param t: vecteur de points ou on veut evaluer la fdr
    :param obs: Series avec les observations
    :return: un tableau qui contient les valeurs de la fdr des données obs
    calculées en chaque point de t
    """
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


# représentation conjointe de 2 séries
xvar = pd.Series(np.random.randn(1000))
yvar = pd.Series(np.random.exponential(1,1000))
df = pd.DataFrame({'x': xvar, 'y': yvar})
df.plot(kind='scatter', x='x', y='y')
plt.show()
plt.close()

# représentation des points
plt.figure()
plt.scatter(xvar, yvar, marker='o', s=40, facecolors='none', edgecolors='r')
plt.show()
plt.close()


# correlation de deux séries
df.corr().loc