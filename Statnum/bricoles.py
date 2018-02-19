# coding=utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data2 = pd.DataFrame(np.random.randn(500,1)*1.5+2,columns=['Normal'])
data2['Uniform'] = np.random.rand(500,1)
data2['Exponentiel'] = np.random.exponential(2,500)
data2['Poisson'] = np.random.poisson(2,500)
data2.head()

plt.figure()
bp = data2.boxplot()
plt.show()
