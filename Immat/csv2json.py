# coding=utf-8

from __future__ import print_function, unicode_literals

import cProfile
# from memory_profiler import profile
import os
import json
from collections import OrderedDict
from datetime import datetime
import time

DEFAULT_CSV_SEP = ";"


def csv2json(csv_line, titles):
    json_buf = OrderedDict([(titles[i], csv_line[i]) for i in range(len(titles))])
    return json_buf


# @profile(precision=1)
def convert_csv_file_to_json(csv_file_name, json_file_name, indent=0, in_enc='utf8'):
    first_line = True
    with open(file_path + os.path.sep + csv_file_name, 'r') as fin, \
            open(file_path + os.path.sep + json_file_name, 'w') as fout:
        titles = []
        nlines_in = 0
        nlines_out = 0
        for line in fin.readlines():
            if nlines_in % 1000 == 0:
                print("{} lines in {}  lines out {}".format(str(datetime.now()), nlines_in, nlines_out))
            nlines_in += 1
            nlines_out += len(titles) + 1
            # print(line.rstrip())
            # csv_line = line.rstrip().replace("\"", '').split(DEFAULT_CSV_SEP)
            csv_line = [x.rstrip('"').lstrip('"') for x in line.rstrip().decode(in_enc).split(DEFAULT_CSV_SEP)]
            if first_line:
                titles = csv_line
                first_line = False
            else:
                json_dict = csv2json(csv_line, titles)
                json.dump(json_dict, fout, indent=indent)

        print("{} lines in {}  lines out {}".format(str(datetime.now()), nlines_in, nlines_out))
        return nlines_in, nlines_out


if __name__ == '__main__':
    file_path = r"D:/D_Documents/Projets/EnvironmentDarwinBatch/Data/siv_mi_20190227"
    # file_path = r"C:/Users/emmanuel_barillot/Documents/Work/Darwin/Immat/siv_mi_20190227"

    # csv_file_name = r"sample.csv"
    # csv_file_name = r"2019-143_1_20190219010305_DATA_100.csv"
    # csv_file_name = r"2019-143_1_20190219010305_DATA_1e4.csv"
    # csv_file_name = r"2019-143_1_20190219010305_DATA_1e5.csv"
    csv_file_name = r"2019-143_1_20190219010305_DATA_1e6.csv"

    json_file_name = os.path.splitext(csv_file_name)[0] + ".json"
    # avec profiler
    # cProfile.run('convert_csv_file_to_json(csv_file_name, json_file_name)', sort='tottime')
    start = time.time()
    nlines_in, nlines_out = convert_csv_file_to_json(csv_file_name, json_file_name)
    delta = time.time() - start
    print("{:d} lines in {:.3f} seconds ({:.0f}/s)".format(nlines_in, delta, nlines_in / delta))
