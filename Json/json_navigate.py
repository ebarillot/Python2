# coding=utf-8

from __future__ import print_function, unicode_literals
from EBCommons.json_helper import json_navigate
from json import load
from sys import argv

''' navigation dans un json '''

__author__ = 'Emmanuel Barillot'


if __name__ == '__main__':
    fname, path = argv[1], argv[2:]
    obj = load(open(fname))
    print(json_navigate(obj, path))
