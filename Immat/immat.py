# coding=utf-8

from __future__ import print_function, unicode_literals

import csv
import os


class Immat(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def count(self):
        with open(self.file_name, "r") as f:
            nb = 1
            line = f.readline()
            while line:
                line = f.readline()
                nb += 1
                if nb%10000 == 0:
                    print("nb: {}".format(nb))
        return nb

    def read(self):
        pass


if __name__ == '__main__':
    file_path = r"D:/D_Documents/Projets/EnvironmentDarwinBatch/Data/siv_mi_20190227"
    # file_name = r"2019-143_1_20190219010305_ET.csv"
    file_name = r"2019-143_1_20190219010305_DATA.csv"
    # file_name = r"2019-143_1_20190219010305_DATA_100.csv"
    immat = Immat(file_path + os.path.sep + file_name)
    print(immat.count())
