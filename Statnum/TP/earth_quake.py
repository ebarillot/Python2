# coding=utf-8


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if os.path.basename(os.getcwd()) != 'Statnum':
    os.chdir('./Statnum')

dataset = pd.read_csv('TP/earthquake_week.csv', sep=',')
df = pd.DataFrame(dataset)
print('-- Shape: {}'.format(df.shape))
print('-- Infos:')
df.info()
print('-- Infos END --')

df.describe()
df.head(5)
