# coding=utf-8

from __future__ import print_function, unicode_literals
import os
from string import maketrans   # Required to call maketrans function

intab = " "
outtab = "_"
trantab = maketrans(intab, outtab)

ficpath=b"C:\Users\emmanuel_barillot\Documents\Work\TEMP"
os.chdir(ficpath)

for fic in os.listdir(ficpath):
    newname='1-{}'.format(fic.translate(trantab))
    print('{} -> {}'.format(fic,newname))
    os.rename(fic,newname)
