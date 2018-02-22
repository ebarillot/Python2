# coding=utf-8


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame({'A': [ 1  , 2  , 3  , 3  , 4  , 4  , 3  ],
                   'B': ['a' ,'b' ,'c' ,'a' ,'b' ,'c' , 'a'],
                   'C': ['0' ,'1' ,'1' ,'0' ,'0' ,'0' , '1'],
                   'D': ['d1','d2','d3','d4','d5','d6','d6']})
df.size
df.count()
df.index
df.columns
df.shape
df['A'].count()
len(df)

df_filters = {
    'A1': (df['A'] == 1),
    'A2': (df['A'] == 2),
    'A3': (df['A'] == 3),
    'A4': (df['A'] == 4),
    }

df.loc[df_filters['A1'], ['B', 'C']]
df.loc[df_filters['A1'], ['B', 'C']].groupby(['B', 'C']).size()
df.loc[df_filters['A1']].groupby(['B', 'C']).size()

df.loc[df_filters['A3']]
df.loc[df_filters['A3']].size
df.loc[df_filters['A3'], ['B', 'C']]
df.loc[df_filters['A3'], ['B', 'C']].size
df.loc[df_filters['A3']].groupby(['B', 'C']).size()
len(df.loc[df_filters['A3']])
df.loc[df_filters['A3'], ['B', 'C']]
len(df.loc[df_filters['A3'], ['B', 'C']])


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



df_freq = freq_nvars_filters(df, df_filters, ['B', 'C'])


# controle de la somme des fréquences
for idx in df_freq.keys():
    print('filter {}, {} values, sum={}'.format(idx, len(df_freq[idx]), df_freq[idx].sum()))
