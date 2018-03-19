# coding=utf-8

from __future__ import print_function, unicode_literals
import logging
import os
import psutil
from operator import itemgetter

ficpath="f:/Musique/Litterature/AndreBreton-Nadja/AndreBreton-Nadja_D1"

for fic in os.listdir(ficpath):
    newname='1-{}'.format(fic)
    print('{} -> {}'.format(fic,newname))
    os.rename(fic,newname)
