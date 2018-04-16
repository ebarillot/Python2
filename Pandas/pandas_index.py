# coding=utf-8

import pandas as pd
import numpy as np

#  exemples tirés du livre Mastering Pandas

# complex slicing
ar = np.arange(15);
ar

# [::-1] : permet d'inverser l'ordre des éléments
ar2 = np.arange(0, -10, -1)[::-1];
ar2

# remplace les 10 1ers éléments dans ar par les éléments de ar2
ar[:10] = ar2;
ar

# copies and views
ar1 = np.arange(12);
ar1
ar2 = ar1[::2];
ar2
ar2[1] = -1;
ar1  # tableau modifié

ar = np.arange(8);
ar
arc = ar[:3].copy();
arc
arc[0] = -1;
arc
ar  # non modifié

# Transposition
ar = np.array([[1, 2, 3], [4, 5, 6]]);
ar
ar.T

# comparaison
ar = np.arange(0, 6)
ar2 = np.array([0, 1, 2, 3, 4, 5])
np.array_equal(ar, ar2)
np.all(ar == ar2)

#  reduction
ar = np.arange(1, 5)
ar.prod()

ar = np.array([np.arange(1, 6), np.arange(1, 6)]);
ar
# Columns
np.prod(ar, axis=0)
# Rows
np.prod(ar, axis=1)

ar = np.array([[2, 3, 4], [5, 6, 7], [8, 9, 10]]);
ar.sum()
ar.mean()
np.median(ar)

# Statistical operators
np.random.seed(10)
ar = np.random.randint(0, 10, size=(4, 5));
ar
ar.mean()
ar.std()
ar.var(axis=0)  # across rows
ar.cumsum()

# Flattening a multi-dimensional array
ar = np.array([np.arange(1, 6), np.arange(10, 15)]);
ar
ar.ravel()
ar.T.ravel()
# You can also use np.flatten, which does the same thing, except that it returns a
# copy while np.ravel returns a view

# Reshaping
ar = np.arange(1, 16);
ar
ar.reshape(3, 5)

# Resizing
ar = np.arange(5);
ar.resize((8,));
ar
ar = np.arange(5);
ar

ar2 = ar
ar.resize((8,))  # ==> ValueError
np.resize(ar, (8,))  # marche

# Adding a dimension
ar = np.array([14, 15, 16]);
ar.shape
ar

ar = ar[:, np.newaxis];
ar.shape
ar

# Array sorting
# Sort the array along an axis; 뽸rst, let's discuss this along the y-axis:
ar = np.array([[3, 2], [10, -1]]);
ar
ar.sort(axis=1);
ar
# Here, we will explain the sorting along the x-axis
ar = np.array([[3, 2], [10, -1]]);
ar
ar.sort(axis=0);
ar

# Sorting by in -place(np.array.sort) and out - of - place(np.sort) functions.
# Other operations that are available for array sorting include the following:
# °  np.min(): It returns the minimum element in the array
# °  np.max(): It returns the maximum element in the array
# °  np.std(): It returns the standard deviation of the elements in the array
# °  np.var(): It returns the variance of elements in the array
# °  np.argmin(): It indices of minimum
# °  np.argmax(): It indices of maximum
# °  np.all(): It returns element-wise and all of the elements
# °  np.any(): It returns element-wise or all of the elements

np.any(ar)  # or entre élements
np.all(ar)  # and entre élements

# #########################################################
# Data structures in pandas
# Series: Series is really a 1D NumPy array under the hood. It consists of a NumPy array
# coupled with an array of labels
np.random.seed(100)
ser = pd.Series(np.random.rand(7));
ser

import calendar as cal

monthNames = [cal.month_name[i] for i in np.arange(1, 6)]
months = pd.Series(np.arange(1, 6), index=monthNames);
months
months.index

# Using Python dictionary
currDict = {'US'     : 'dollar', 'UK': 'pound',
            'Germany': 'euro', 'Mexico': 'peso',
            'Nigeria': 'naira',
            'China'  : 'yuan', 'Japan': 'yen'}
currSeries = pd.Series(currDict);
currSeries
currSeries.index

# The index of a pandas Series structure is of type pandas.core.index.Index and can
# be viewed as an ordered multiset (= un ensemble dans lequel un élément peut être présent plusieurs fois)

# Index
stockPrices = {'GOOG': 1180.97, 'FB': 62.57,
               'TWTR': 64.50, 'AMZN': 358.69,
               'AAPL': 500.6}
stockPriceSeries = pd.Series(stockPrices,
                             index=['GOOG', 'FB', 'YHOO',
                                    'TWTR', 'AMZN', 'AAPL'],
                             name='stockPrices')
stockPriceSeries
stockPriceSeries.index

# Using scalar values
dogSeries = pd.Series('chihuahua',
                      index=['breed', 'countryOfOrigin',
                             'name', 'gender'])
dogSeries
dogSeries.index

dogSeries = pd.Series('pekingese');
dogSeries
type(dogSeries)

# Assignment
currDict['China']
stockPriceSeries['GOOG'] = 1200.0
stockPriceSeries

stockPriceSeries['MSFT']  # ==> KeyError
stockPriceSeries.get('MSFT', np.NaN)  # retourne une valeur par defaut

# Slicing
stockPriceSeries[:4]
stockPriceSeries[stockPriceSeries > 100]

# Other operations
np.mean(stockPriceSeries)
np.std(stockPriceSeries)
ser
ser * ser
np.sqrt(ser)

# An important feature of Series is that the data is automatically aligned on the basis of the label
ser[1:]
ser[1:] + ser[:-2]
# Thus, we can see that for non-matching labels, NaN is inserted
# The default behavior is that the union of the indexes is produced for unaligned Series structures. This
# is preferable as information is preserved rather than lost.

# #########################################################
# DataFrame: DataFrame is an 2-dimensional labeled array
# It is similar to structured arrays in NumPy with mutability added
# Conceptually analogous to a table or spreadsheet of data.
# •  Similar to a NumPy ndarray but not a subclass of np.ndarray.
# •  Columns can be of heterogeneous types: oat64, int, bool, and so on.
# •  A DataFrame column is a Series structure.
# •  It can be thought of as a dictionary of Series structures where both the
# columns and the rows are indexed, denoted as 'index' in the case of rows
# and 'columns' in the case of columns.
# •  It is size mutable: columns can be inserted and deleted.
# Every axis in a Series/DataFrame has an index, whether default or not. Indexes are
# needed for fast lookups as well as proper aligning and joining of data in pandas. The
# axes can also be named-for example in the form of month for the array of columns
# Jan Feb Mar... Dec

# Using dictionaries of Series
stockSummaries = {
    'AMZN': pd.Series([346.15, 0.59, 459, 0.52, 589.8, 158.88],
                      index=['Closing price', 'EPS',
                             'Shares Outstanding(M)',
                             'Beta', 'P/E', 'Market Cap(B)']),
    'GOOG': pd.Series([1133.43, 36.05, 335.83, 0.87, 31.44, 380.64],
                      index=['Closing price', 'EPS', 'Shares Outstanding(M)',
                             'Beta', 'P/E', 'Market Cap(B)']),
    'FB'  : pd.Series([61.48, 0.59, 2450, 104.93, 150.92],
                      index=['Closing price', 'EPS', 'Shares Outstanding(M)',
                             'P/E', 'Market Cap(B)']),
    'YHOO': pd.Series([34.90, 1.27, 1010, 27.48, 0.66, 35.36],
                      index=['Closing price', 'EPS', 'Shares Outstanding(M)',
                             'P/E', 'Beta', 'Market Cap(B)']),
    'TWTR': pd.Series([65.25, -0.3, 555.2, 36.23],
                      index=['Closing price', 'EPS', 'Shares Outstanding(M)',
                             'Market Cap(B)']),
    'AAPL': pd.Series([501.53, 40.32, 892.45, 12.44, 447.59, 0.84],
                      index=['Closing price', 'EPS', 'Shares Outstanding(M)', 'P/E',
                             'Market Cap(B)', 'Beta'])}
stockDF = pd.DataFrame(stockSummaries);
stockDF

stockDF = pd.DataFrame(stockSummaries,
                       index=['Closing price', 'EPS',
                              'Shares Outstanding(M)',
                              'P/E', 'Market Cap(B)', 'Beta']);
stockDF

stockDF = pd.DataFrame(stockSummaries,
                       index=['Closing price', 'EPS',
                              'Shares Outstanding(M)',
                              'P/E', 'Market Cap(B)', 'Beta'],
                       columns=['FB', 'TWTR', 'SCNW'])
stockDF
stockDF.index
stockDF.columns

# Using a dictionary of ndarrays/lists
algos = {'search'          : ['DFS', 'BFS', 'Binary Search',
                              'Linear', 'ShortestPath (Djikstra)'],
         'sorting'         : ['Quicksort', 'Mergesort', 'Heapsort',
                              'Bubble Sort', 'Insertion Sort'],
         'machine learning': ['RandomForest',
                              'K Nearest Neighbor',
                              'Logistic Regression',
                              'K-Means Clustering',
                              'Linear Regression']}
algoDF = pd.DataFrame(algos);
algoDF
pd.DataFrame(algos, index=['algo_1', 'algo_2', 'algo_3', 'algo_4', 'algo_5'])

# Using a structured array
memberData = np.zeros((4,),
                      dtype=[('Name', 'a15'),
                             ('Age', 'i4'),
                             ('Weight', 'f4')])
memberData[:] = [('Sanjeev', 37, 162.4),
                 ('Yingluck', 45, 137.8),
                 ('Emeka', 28, 153.2),
                 ('Amy', 67, 101.3)]
memberDF = pd.DataFrame(memberData);
memberDF
pd.DataFrame(memberData, index=['a', 'b', 'c', 'd'])

# Using a Series structure
currSeries.name = 'currency'
pd.DataFrame(currSeries)

# DataFrame.from_dict: It takes a dictionary of dictionaries or sequences and
# returns DataFrame.
# •  DataFrame.from_records: It takes a list of tuples or structured ndarray.
# •  DataFrame.from_items: It takes a sequence of (key, value) pairs. The keys
# are the column or index names, and the values are the column or row values.
# If you wish the keys to be row index names, you must specify orient='index'
# as a parameter and specify the column names.
# •  pandas.io.parsers.read_csv: This is a helper function that reads a CSV
# file into a pandas DataFrame structure.
# •  pandas.io.parsers.read_table: This is a helper function that reads a
# delimited file into a pandas DataFrame structure.
# •  pandas.io.parsers.read_fwf: This is a helper function that reads a table
# of fixed-width lines into a pandas DataFrame structure.


# Selection
memberDF['Name']

# Assignment
memberDF['Height'] = 60;
memberDF

# Deletion
del memberDF['Height'];
memberDF

memberDF['BloodType'] = 'O'
bloodType = memberDF.pop('BloodType');
bloodType

# Basically, a DataFrame structure can be treated as if it were a dictionary of Series
# objects. Columns get inserted at the end; to insert a column at a speci欠c location,
# you can use the insert function:
memberDF.insert(2, 'isSenior', memberDF['Age'] > 60);
memberDF

# Alignment
ore1DF = pd.DataFrame(np.array([[20, 35, 25, 20],
                                [11, 28, 32, 29]]),
                      columns=['iron', 'magnesium',
                               'copper', 'silver'])
ore2DF = pd.DataFrame(np.array([[14, 34, 26, 26],
                                [33, 19, 25, 23]]),
                      columns=['iron', 'magnesium',
                               'gold', 'silver'])
ore1DF + ore2DF

ore1DF + pd.Series([25, 25, 25, 25],
                   index=['iron', 'magnesium',
                          'copper', 'silver'])

# Other mathematical operations
np.sqrt(ore1DF)

# Basic indexing
SpotCrudePrices_2013_Data = {'U.K. Brent'             : {'2013-Q1': 112.9, '2013-Q2': 103.0, '2013-Q3': 110.1,
                                                         '2013-Q4': 109.4},
                             'Dubai'                  : {'2013-Q1': 108.1, '2013-Q2': 100.8,
                                                         '2013-Q3': 106.1, '2013-Q4': 106.7},
                             'West Texas Intermediate': {'2013-Q1': 94.4, '2013-Q2': 94.2, '2013-Q3': 105.8,
                                                         '2013-Q4': 97.4}}
SpotCrudePrices_2013 = pd.DataFrame.from_dict(SpotCrudePrices_2013_Data)
SpotCrudePrices_2013

dubaiPrices = SpotCrudePrices_2013['Dubai'];
dubaiPrices

SpotCrudePrices_2013[['West Texas Intermediate', 'U.K. Brent']]

SpotCrudePrices_2013['Brent Blend']  # ==> KeyError
SpotCrudePrices_2013.get('Brent Blend', 'N/A')  # ==> pas d'erreur en spécifiant une valeur par défaut

# Note that rows cannot be selected with the bracket operator []
# in a DataFrame
SpotCrudePrices_2013['2013-Q1']  # ==> KeyError
#  mais marche sur une série:
dubaiPrices['2013-Q1']

# Accessing attributes using dot operator
SpotCrudePrices_2013.Dubai

# SpotCrudePrices_2013."West Texas Intermediate"  # ==> incalid syntax
# We can resolve this by renaming the column index names so that they are all valid
# identifiers:
SpotCrudePrices_2013
SpotCrudePrices_2013.columns = ['Dubai', 'UK_Brent',
                                'West_Texas_Intermediate']
SpotCrudePrices_2013

# Range slicing
# ar[startIndex: endIndex: stepValue]
SpotCrudePrices_2013[:2]
SpotCrudePrices_2013[2:]
SpotCrudePrices_2013[::2]
SpotCrudePrices_2013[::-1]
dubaiPrices = SpotCrudePrices_2013['Dubai']

dubaiPrices[1:]
dubaiPrices[:-1]
dubaiPrices[::-1]

# Label, integer, and mixed indexing
# •  The .loc operator: It allows label-oriented indexing
# •  The .iloc operator: It allows integer-based indexing
# •  The .ix operator: It allows mixed label and integer-based indexing

# Label-oriented indexing .loc
NYC_SnowAvgsData = {'Months'           :
                        ['January', 'February', 'March',
                         'April', 'November', 'December'],
                    'Avg SnowDays'     : [4.0, 2.7, 1.7, 0.2, 0.2, 2.3],
                    'Avg Precip. (cm)' : [17.8, 22.4, 9.1, 1.5, 0.8, 12.2],
                    'Avg Low Temp. (F)': [27, 29, 35, 45, 42, 32]}
NYC_SnowAvgs = pd.DataFrame(NYC_SnowAvgsData,
                            index=NYC_SnowAvgsData['Months'],
                            columns=['Avg SnowDays', 'Avg Precip. (cm)',
                                     'Avg Low Temp. (F)'])
NYC_SnowAvgs
NYC_SnowAvgs.loc['January']
NYC_SnowAvgs.loc[['January', 'April']]
NYC_SnowAvgs.loc['January':'March']

# Note that while using the .loc, .iloc, and .ix operators on a DataFrame, the row
# index must always be speci湥ed 湥rst. This is the opposite of the [] operator, where
# only columns can be selected directly. Hence, we get an error if we do the following:
NYC_SnowAvgs.loc['Avg SnowDays']  # ==> KeyError
NYC_SnowAvgs.loc[:, 'Avg SnowDays']  # syntaxe correcte pour toutes les lignes

NYC_SnowAvgs.loc['March', 'Avg SnowDays']  # une cellule ligne,colonne
NYC_SnowAvgs.loc['March']['Avg SnowDays']
NYC_SnowAvgs['Avg SnowDays']['March']
NYC_SnowAvgs['March'][
    'Avg SnowDays']  # KeyError, car avec cette syntaxe il faut spécifier le nom de la série (colonne) d'abord
NYC_SnowAvgs['March']  # même KeyError
NYC_SnowAvgs.loc['March']  # fonctionne

# Selection using a Boolean array
NYC_SnowAvgs.loc[NYC_SnowAvgs['Avg SnowDays'] < 1, :]
SpotCrudePrices_2013.loc[:, SpotCrudePrices_2013.loc['2013-Q1'] > 110]
SpotCrudePrices_2013.loc['2013-Q1'] > 110

# Integer-oriented indexing
import scipy.constants as phys
import math

sci_values = pd.DataFrame([[math.pi, math.sin(math.pi),
                            math.cos(math.pi)],
                           [math.e, math.log(math.e),
                            phys.golden],
                           [phys.c, phys.g, phys.e],
                           [phys.m_e, phys.m_p, phys.m_n]],
                          index=list(range(0, 20, 5)))
sci_values.iloc[:2]
sci_values.iloc[2, 0:2]
# !!! Note that the arguments to .iloc are strictly positional and have nothing to do with the index values
sci_values.iloc[10]  # IndexError: la valeur 10 est bien une valeur de l'index mais pas une position !
sci_values.iloc[2:3, :]  # une ligne spécifique
sci_values.iloc[3]  # ligne 3
sci_values.iloc[6, :]  # IndexError car au delà des lignes du tableau

# The .iat and .at operators
# The .iat and .at operators can be used for a quick selection of scalar values
sci_values.iloc[3, 0]
sci_values.iat[3, 0]
# %timeit sci_values.iloc[3, 0]
# %timeit sci_values.iat[3, 0]
# Thus, we can see that .iat is much faster than the .iloc/.ix operators. The same
# applies to .at versus .loc.

# Mixed indexing with the .ix operator
# The .ix operator behaves like a mixture of the .loc and .iloc operators, with the
# .loc behavior taking precedence. It takes the following as possible inputs:
# •  A single label or integer
# •  A list of integers or labels
# Operations in pandas, Part I – Indexing and Selecting
# •  An integer slice or label slice
# •  A Boolean array
#  pour regler pb de PATH
import os

if os.path.basename(os.getcwd()) != 'Pandas':
    os.chdir('./Pandas')
print(os.getcwd())
stockIndexDataDF = pd.read_csv('data/stock_index_closing.csv')  # index numérique par defaut
stockIndexDataDF
stockIndexDF = stockIndexDataDF.set_index('TradingDate')  # changement d'index: la 1ere colonne
stockIndexDF

# !!! ATTENTION: Starting in 0.20.0, the .ix indexer is deprecated, in favor of the more strict .iloc and .loc indexers.
# Using a single label
stockIndexDF.ix['2014/01/30']
# Using a list of labels
stockIndexDF.ix[['2014/01/30']]
stockIndexDF.ix[['2014/01/30', '2014/01/31']]

dfd = pd.DataFrame({'A': [1, 2, 3],
                    'B': [4, 5, 6]},
                   index=list('abc'))
# pour remplacer la syntaxe suivante:
dfd.ix[[0, 2], 'A']
#  il faut utiliser:
dfd.loc[dfd.index[[0, 2]], 'A']
dfd.iloc[[0, 2], dfd.columns.get_loc('A')]
dfd.iloc[[0, 2], dfd.columns.get_indexer(['A', 'B'])]  # plusieurs indexers

###########################################################
# MultiIndexing
# We now turn to the topic of MultiIndexing. Multi-level or hierarchical indexing is
# useful because it enables the pandas user to select and massage data in multiple
# dimensions by using data structures such as Series and DataFrame
import os

if os.path.basename(os.getcwd()) != 'Pandas':
    os.chdir('./Pandas')
print(os.getcwd())
sharesIndexDataDF = pd.read_csv('data/stock_index_prices.csv')
sharesIndexDF = sharesIndexDataDF.set_index(['TradingDate', 'PriceType'])
mIndex = sharesIndexDF.index;
mIndex  # index à deux niveaux hiérarchiques
# we see that the MultiIndex consists of a list of tuples.

mIndex.get_level_values(0)
mIndex.get_level_values(1)
mIndex.get_level_values(2)  # IndexError évidemment car il n'y a pas de niveau 2
sharesIndexDF.loc['2014/02/21']
sharesIndexDF.loc['2014/02/21':'2014/02/24']

# try slicing at a lower level:
sharesIndexDF.loc[('2014/02/21', 'open'):('2014/02/24', 'open')]  # ==> UnsortedIndexError car index non trié
sharesIndexDF.sortlevel(0).loc[('2014/02/21', 'open'):('2014/02/24', 'open')]  # marche !
# sortlevel() method sorts the labels of an axis within a MultiIndex
# To be on the safe side, sort ꤪrst before slicing with a MultiIndex

# We can also pass a list of tuples
sharesIndexDF.ix[[('2014/02/21', 'close'), ('2014/02/24', 'open')]]

# Swapping and reordering levels
swappedDF = sharesIndexDF[:7].swaplevel(0, 1, axis=0)

# reorder_levels function is more general, allowing you to specify the order of the levels
reorderedDF = sharesIndexDF[:7].reorder_levels(['PriceType',
                                                'TradingDate'],
                                               axis=0)
reorderedDF

# Cross sections
# The xs method provides a shortcut means of selecting data based on a particular index level value
sharesIndexDF.xs('open', level='PriceType')
sharesIndexDF.swaplevel(0, 1, axis=0).loc['open']  # equivalent à .xs

# Boolean indexing
sharesIndexDataDF.loc[(sharesIndexDataDF['PriceType'] == 'close') & (sharesIndexDataDF['Nasdaq'] > 4300)]

highSelection = sharesIndexDataDF['PriceType'] == 'high'
NasdaqHigh = sharesIndexDataDF['Nasdaq'] < 4300
sharesIndexDataDF.ix[highSelection & NasdaqHigh]

# The is in and any all methods
stockSeries = pd.Series(['NFLX', 'AMZN', 'GOOG', 'FB', 'TWTR'])
stockSeries.isin(['AMZN', 'FB'])
stockSeries[stockSeries.isin(['AMZN', 'FB'])]

australianMammals = \
    {'kangaroo'     : {'Subclass'      : 'marsupial',
                       'Species Origin': 'native'},
     'flying fox'   : {'Subclass'      : 'placental',
                       'Species Origin': 'native'},
     'black rat'    : {'Subclass'      : 'placental',
                       'Species Origin': 'invasive'},
     'platypus'     : {'Subclass'      : 'monotreme',
                       'Species Origin': 'native'},
     'wallaby'      : {'Subclass'      : 'marsupial',
                       'Species Origin': 'native'},
     'palm squirrel': {'Subclass': 'placental',
                       'Origin'  : 'invasive'},
     'anteater'     : {'Subclass': 'monotreme', 'Origin': 'native'},
     'koala'        : {'Subclass': 'marsupial', 'Origin': 'native'}
     }
ozzieMammalsDF = pd.DataFrame(australianMammals)
aussieMammalsDF = ozzieMammalsDF.T;
aussieMammalsDF
aussieMammalsDF.isin({'Subclass': ['marsupial'], 'Origin': ['native']})
nativeMarsupials = {'Mammal Subclass': ['marsupial'],
                    'Species Origin' : ['native']}
nativeMarsupialMask = aussieMammalsDF.isin(nativeMarsupials)
# nativeMarsupialMask = aussieMammalsDF.isin(nativeMarsupials).all(True)  # ne marche pas ?
aussieMammalsDF[nativeMarsupialMask]

# Using the where() method
np.random.seed(100)
normvals = pd.Series([np.random.normal() for i in np.arange(10)])   # ATTENTION: Serie
normvals
normvals[normvals>0]
normvals.where(normvals > 0)

np.random.seed(100)
normDF = pd.DataFrame([[round(np.random.normal(), 3) for i in
                        np.arange(5)] for j in range(3)],
                      columns=['0', '30', '60', '90', '120'])
normDF
normDF[normDF > 0]  # pas besoin de where() sur une DF pour avoir des NaN
normDF.where(normDF > 0)
normDF.mask(normDF>0)   # mask() est l'inverse de where()

# Operations on indexes
import os
if os.path.basename(os.getcwd()) != 'Pandas':
    os.chdir('./Pandas')
print(os.getcwd())
stockIndexDataDF=pd.read_csv('data/stock_index_closing.csv')
stockIndexDataDF
stockIndexDF=stockIndexDataDF.set_index('TradingDate')
stockIndexDF
type(stockIndexDF)
stockIndexDF.reset_index()  # reset_index() défait l'index fabriqué avec set_index()
type(stockIndexDF.reset_index())

# Grouping of data
# The groupby operation can be thought of as part of a process that involves the
# following three steps:
# •  Splitting the dataset
# •  Analyzing the data
# •  Aggregating or combining the data
# The result of a groupby operation is not a DataFrame but dict of DataFrame objects
import os
if os.path.basename(os.getcwd()) != 'Pandas':
    os.chdir('./Pandas')
print(os.getcwd())
uefaDF=pd.read_csv('data/euro_winners.csv')
uefaDF.head()
nationsGrp = uefaDF.groupby('Nation')
type(nationsGrp)
nationsGrp.groups

len(nationsGrp.groups)
nationWins=nationsGrp.size()
nationWins.sort_values(ascending=False)
type(nationWins)
nationWins

winnersGrp = uefaDF.groupby(['Nation', 'Winners'])
clubWins=winnersGrp.size()
clubWins.sort_values(ascending=False)
type(clubWins)
clubWins

# advanced group by
import os
if os.path.basename(os.getcwd()) != 'Pandas':
    os.chdir('./Pandas')
print(os.getcwd())
goalStatsDF=pd.read_csv('data/goal_stats_euro_leagues_2012-13.csv')
goalStatsDF = goalStatsDF.set_index('Month')
goalStatsDF.head(3)
goalStatsDF.tail(3)
goalStatsGroupedByYear = goalStatsDF.groupby(lambda Month: Month.split('/')[2])
for name, group in goalStatsGroupedByYear:
    print name
    print group

goalStatsGroupedByMonth = goalStatsDF.groupby(level=0)
for name, group in goalStatsGroupedByMonth:
    print name
    print group
    print "\n"

goalStatsDF=goalStatsDF.reset_index()
goalStatsDF=goalStatsDF.set_index(['Month','Stat'])
monthStatGroup = goalStatsDF.groupby(level=['Month', 'Stat'])
for name, group in monthStatGroup:
    print name
    print group

# Using groupby with a MultiIndex
goalStatsDF2=pd.read_csv('data/goal_stats_euro_leagues_2012-13.csv')
goalStatsDF2=goalStatsDF2.set_index(['Month','Stat'])
print goalStatsDF2.head(3)
print goalStatsDF2.tail(3)
grouped2 = goalStatsDF2.groupby(level='Stat')
grouped2.sum()
for name, group in grouped2:
    print name
    print group

goalStatsDF2.sum(level='Stat')
totalsDF=grouped2.sum()
totalsDF.loc['GoalsScored'] / totalsDF.loc['MatchesPlayed']

# Obtain goals per game data as a DataFrame. Note that we have to transpose it since gpg is returned as a Series
gpg=totalsDF.loc['GoalsScored']/totalsDF.loc['MatchesPlayed']
goalsPerGameDF=pd.DataFrame(gpg).T
goalsPerGameDF

# Reindex the goalsPerGameDF DataFrame so that the 0 index is replaced by GoalsPerGame
goalsPerGameDF=goalsPerGameDF.rename(index={0:'GoalsPerGame'})
goalsPerGameDF

# Append the goalsPerGameDF DataFrame to the original one:
pd.options.display.float_format='{:.2f}'.format
totalsDF.append(goalsPerGameDF)


# Using the aggregate method
# Another way to generate summary statistics is by using the aggregate method explicitly
pd.options.display.float_format = None
grouped2.aggregate(np.sum)
# This generates a grouped DataFrame object


# Applying multiple functions
# For a grouped DataFrame object, we can specify a list of functions to be applied to each column
grouped2.agg([np.sum, np.mean, np.size])

nationsGrp['Attendance'].agg({'Total':np.sum, 'Average':np.mean, 'Deviation':np.std})   # will be deprecated

# The transform() method
# The groupby-transform function is used to perform transformation operations on
# a groupby object. For example, we could replace NaN values in the groupby object
# using the fillna method. The resulting object after using transform has the same
# size as the original groupby objec
import os
if os.path.basename(os.getcwd()) != 'Pandas':
    os.chdir('./Pandas')
print(os.getcwd())
goalStatsDF3=pd.read_csv('data/goal_stats_euro_leagues_2012-13.csv')
goalStatsDF3=goalStatsDF3.set_index(['Month'])
goalsScoredDF=goalStatsDF3.loc[goalStatsDF3['Stat']=='GoalsScored']
goalsScoredDF.iloc[:,1:]

goalsScoredPerYearGrp=goalsScoredDF.groupby(lambda Month: Month.split('/')[2])
goalsScoredPerYearGrp.mean()
goalsScoredPerYearGrp.count()
fill_fcn = lambda x: x.fillna(x.mean())
trans = goalsScoredPerYearGrp.transform(fill_fcn)
tGroupedStats = trans.groupby(lambda Month:   Month.split('/')[2])
tGroupedStats.mean()

tGroupedStats.count()


# Filtering
# The Ƿlter method enables us to apply Ƿltering on a groupby object that results in
# a subset of the initial object
# The filter method enables us to apply filtering on a groupby object that results in
# a subset of the initial object. Here, we illustrate how to display the months of the
# season in which more than 100 goals were scored in each of the four leagues
goalsScoredDF.groupby(level='Month').filter(lambda x: np.all([x[col] > 100 for col in goalsScoredDF.columns]))
# Note the use of the np.all operator to ensure that the constraint is enforced for all the columns

# Merging and joining
# The concat function
# The concat function is used to join multiple pandas' data structures along a specified
# axis and possibly perform union or intersection operations along other axes
# concat(objs, axis=0, , join='outer', join_axes=None, ignore_index=False,
# keys=None, levels=None, names=None, verify_integrity=False)
# The synopsis of the elements of concat function are as follows:
# • The objs function: A list or dictionary of Series, DataFrame, or Panel objects
# to be concatenated.
# • The axis function: The axis along which the concatenation should be
# performed. 0 is the default value.
# • The join function: The type of join to perform when handling indexes on
# other axes. The 'outer' function is the default.
# • The join_axes function: This is used to specify exact indexes for the
# remaining indexes instead of doing outer/inner join.
# • The keys function: This specifies a list of keys to be used to construct
# a MultiIndex.
import os
if os.path.basename(os.getcwd()) != 'Pandas':
    os.chdir('./Pandas')
print(os.getcwd())
stockDataDF = pd.read_csv('data/tech_stockprices.csv').set_index(['Symbol']);stockDataDF
# A=stockDataDF.ix[:4, ['Closing price', 'EPS']]; A # syntaxe .ix obsolète remplacée par la ligne suivante:
A = stockDataDF.loc[stockDataDF.index[:4], ['Closing price', 'EPS']]; A   # avec loc
A = stockDataDF.iloc[:4, stockDataDF.columns.get_indexer(['Closing price', 'EPS'])]; A    # avec iloc

# B = stockDataDF.ix[2:-2, ['P/E']];B   # .ix deprecated
B = stockDataDF.iloc[2:-2, stockDataDF.columns.get_indexer(['P/E'])]; B    # avec iloc

# C=stockDataDF.ix[1:5, ['Market Cap(B)']];C
C = stockDataDF.iloc[1:5, stockDataDF.columns.get_indexer(['Market Cap(B)'])]; C    # avec iloc

# Here, we perform a concatenation by specifying an outer join, which concatenates
# and performs a union on all the three data frames, and includes entries that do not
# have values for all the columns by inserting NaN for such columns:
pd.concat([A,B,C],axis=1) # outer join

# We can also specify an inner join that does the concatenation, but only includes rows
# that contain values for all the columns in the final data frame by throwing out rows
# with missing columns, that is, it takes the intersection:
pd.concat([A,B,C],axis=1, join='inner') # Inner join ==> pas de NaN dans le DF résultat


# The third case enables us to use the specific index from the original DataFrame to join on:
#  est-ce que ça veut dire que les A,B,C sont des vues et non des copies sur stockDataDF ?
#  ainsi elle partagent bien les index ?
np.shares_memory(stockDataDF,A) # ==> répond false pourtant ... donc A,B,C seraient indépendantes en mémoire
np.shares_memory(stockDataDF.index,A.index) # répond True: les index seraient partagés
pd.concat([A,B,C], axis=1, join_axes=[stockDataDF.index])
A.index
A.index

np.random.seed(100)
normDF=pd.DataFrame(np.random.randn(3,4));normDF
binomDF=pd.DataFrame(np.random.binomial(100,0.5,(3,4)));binomDF
poissonDF=pd.DataFrame(np.random.poisson(100,(3,4)));poissonDF
rand_distribs=[normDF,binomDF,poissonDF]
rand_distribsDF=pd.concat(rand_distribs,keys=['Normal','Binomial', 'Poisson']);rand_distribsDF


# Using append
# The append function is a simpler version of concat that concatenates along axis=0
stockDataA=stockDataDF.iloc[:2,:3]
stockDataA
stockDataB=stockDataDF[2:]
stockDataB
stockDataA.append(stockDataB)

# In order to maintain the order of columns similar to the original DataFrame, we can
# apply the reindex function
stockDataA.append(stockDataB).reindex(stockDataDF.columns,axis=1)
# The append function does not work in places, but it returns a new DataFrame with the second DataFrame
# appended to the first

# Appending a single row to a DataFrame
algos = {'search'          : ['DFS', 'BFS', 'Binary Search', 'Linear'],
         'sorting'         : ['Quicksort', 'Mergesort', 'Heapsort', 'Bubble Sort'],
         'machine learning': ['RandomForest', 'K Nearest Neighbor', 'Logistic Regression', 'K-Means Clustering']}
algoDF = pd.DataFrame(algos);
algoDF
moreAlgos = {'search'          : 'ShortestPath', 'sorting': 'Insertion Sort',
             'machine learning': 'Linear Regression'}
algoDF.append(moreAlgos,ignore_index=True)
# In order for this to work, you must pass the ignore_index=True argument so that the index [0,1,2,3] in algoDF is ignored.


# SQL-like merging/joining of DataFrame objects
# The merge function is used to obtain joins of two DataFrame objects similar to those
# used in SQL database queries. The DataFrame objects are analogous to SQL tables
# merge(left, right, how='inner', on=None, left_on=None,
#     right_on=None, left_index=False, right_index=False,
#     sort=True, suffixes=('_x', '_y'), copy=True)
# Following is the synopsis of merge function:
# • The left argument: This is the first DataFrame object
# • The right argument: This is the second DataFrame object
# • The how argument: This is the type of join and can be inner, outer, left, or
# right. The default is inner.
# • The on argument: This shows the names of columns to join on as join keys.
# • The left_on and right_on arguments : This shows the left and right
# DataFrame column names to join on.
# • The left_index and right_index arguments: This has a Boolean value. If
# this is True, use the left or right DataFrame index/row labels to join on.
# • The sort argument: This has a Boolean value. The default True setting
# results in a lexicographical sorting. Setting the default value to False may
# improve performance.
# • The suffixes argument: The tuple of string suffixes to be applied to
# overlapping columns. The defaults are '_x' and '_y'.
# • The copy argument: The default True value causes data to be copied from
# the passed DataFrame objects.
import os
if os.path.basename(os.getcwd()) != 'Pandas':
    os.chdir('./Pandas')
print(os.getcwd())
USIndexDataDF = pd.read_csv('data/us_index_data.csv');USIndexDataDF
slice1=USIndexDataDF.iloc[:2,:3]
slice1
slice2=USIndexDataDF.iloc[:2,[0,3,4]]
slice2
slice3=USIndexDataDF.iloc[[1,2],:3]
slice3
pd.merge(slice1,slice2)
pd.merge(slice3,slice2,how='inner')
pd.merge(slice3,slice2,how='outer')
pd.merge(slice3,slice2,how='left')
pd.merge(slice3,slice2,how='right')


# The join function
# The DataFrame.join function is used to combine two DataFrames that have
# different columns with nothing in common. Essentially, this does a longitudinal
# join of two DataFrames
slice_NASD_SP=USIndexDataDF.iloc[:4,:3]
slice_NASD_SP
slice_Russ_DJIA=USIndexDataDF.iloc[:4,3:]
slice_Russ_DJIA
slice_NASD_SP.join(slice_Russ_DJIA)
slice1.join(slice2) # ValueError: columns overlap but no suffix specified: Index([u'TradingDate'], dtype='object')


# Pivots and reshaping data
# This section deals with how you can reshape data. Sometimes, data is stored in
# what is known as the stacked format
import os
if os.path.basename(os.getcwd()) != 'Pandas':
    os.chdir('./Pandas')
print(os.getcwd())
plantGrowthRawDF = pd.read_csv('data/PlantGrowth.csv');plantGrowthRawDF
plantGrowthRawDF[plantGrowthRawDF['group']=='ctrl']
plantGrowthRawDF.pivot(index='observation',columns='group',values='weight')
pd.pivot_table(plantGrowthRawDF,values='weight',index='observation', columns=['group'])
pd.pivot_table(plantGrowthRawDF,values='weight',columns=['group'],aggfunc=np.mean)

# autre exemple tiré de la doc python
df = pd.DataFrame({"A": ["foo", "foo", "foo", "foo", "foo",
                         "bar", "bar", "bar", "bar"],
                   "B": ["one", "one", "one", "two", "two",
                         "one", "one", "two", "two"],
                   "C": ["small", "large", "large", "small",
                         "small", "large", "small", "small",
                         "large"],
                   "D": [1, 2, 2, 3, 3, 4, 5, 6, 7]})
df
table = pd.pivot_table(df, values='D', index=['A', 'B'],
                       columns=['C'], aggfunc=np.sum)
table


# Stacking and unstacking
# In addition to the pivot functions, the stack and unstack functions are also available
# on Series and DataFrames, that work on objects containing MultiIndexes

# The stack() function
# First, we set the group and observation column values to be the components of the
# row index respectively, which results in a MultiIndex:
plantGrowthStackedDF=plantGrowthRawDF.set_index(['group','observation'])
plantGrowthStackedDF

# Here, we see that the row index consists of a MultiIndex on the group and
# observation with the weight column as the data value. Now, let us see what
# happens if we apply unstack to the group level:
plantGrowthStackedDF.unstack(level='group')
# The following call is equivalent to the preceding one:
plantGrowthStackedDF.unstack(level=0)
plantGrowthStackedDF.index
plantGrowthStackedDF.columns

# The unstacking operation removes the group from the row index, changing it into a
# single-level index:
plantGrowthStackedDF.unstack(level='group').index
# The MultiIndex is now on the columns:
plantGrowthStackedDF.unstack(level='group').columns

plantGrowthStackedDF.unstack(level=0).stack('group')
plantGrowthStackedDF.unstack()

# The stack() function by default sets the stacked level as the lowest level in the
# resulting MultiIndex on the rows:
plantGrowthStackedDF.unstack().stack()

# Using the melt function
# The melt function enables us to transform a DataFrame by designating some of
# its columns as ID columns. This ensures that they will always stay as columns after
# any pivoting transformations. The remaining non-ID columns can be treated as
# variable and can be pivoted and become part of a name-value two column scheme.
# ID columns uniquely identify a row in the DataFrame
# The names of those non-ID columns can be customized by supplying the var_name
# and value_name parameters. The use of melt is perhaps best illustrated by an
# example, as follows:
USIndexDataDF[:2]
pd.melt(USIndexDataDF[:2], id_vars=['TradingDate'], var_name='Index Name', value_name='Index Value')

# The pandas.get_dummies() function
# This function is used to convert a categorical variable into an indicator DataFrame,
# which is essentially a truth table of possible values of the categorical variable. An
# example of this is the following command:
melted=pd.melt(USIndexDataDF[:2], id_vars=['TradingDate'], var_name='Index Name', value_name='Index Value')
melted
pd.get_dummies(melted['Index Name'])
