#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import datetime
import logging
import os
import sys

csv.register_dialect('csvdefault', delimiter=';', quoting=csv.QUOTE_NONE, lineterminator='\n')


def flatten(list_of_tuple):
    """
    Pour aplatir une liste de liste ou une liste de tuples dans une liste de valeurs simples
    :param list_of_tuple: la liste de tuples à aplatir
    :return: la liste aplatie
    """
    from itertools import chain
    return list(chain.from_iterable(list_of_tuple))


class FilesOfInfnegs(object):
    def __init__(self, path, inputFileList):
        # assert type(inputFileList) is [InputFile]
        self.path = path
        self.inputFileList = inputFileList
        self.infnegDictList = InfnegDictList(inputFileList)

    def parseFileList(self):
        for inputFile in self.inputFileList:
            with open(os.path.join(self.path, inputFile.get_name()), 'r') as file1:
                infnegsList = [Infneg(*inputFile.get_parse_fun(row)) for row in file1]
                self.infnegDictList.append_infneg_list(inputFile.get_name(), infnegsList)
        return self.infnegDictList


class InputFile(object):
    def __init__(self, name, parse_fun_format):
        self.name = name
        self.parse_fun = self.parse_fun_by_inputFormat(parse_fun_format)

    def get_name(self):
        return self.name

    def get_parse_fun(self, row):
        return self.parse_fun(row)

    @classmethod
    def parse_fun_by_inputFormat(self, inputFormat):
        def parse_fun1(row):
            return row[0:9], row[9:10], row[10:18]

        def parse_fun2(row):
            return row[0:9], row[9:11], row[11:19]

        if inputFormat == 'IJ1':
            return parse_fun1
        elif inputFormat == 'IJ2':
            return parse_fun2
        else:
            return None


class Dateff(object):
    def __init__(self, datetext):
        self.names = ('annee', 'mois', 'jour')
        self.data = (datetext[0:4], datetext[4:6], datetext[6:8])

    def __str__(self):
        return "/".join(self.data)


class Infneg(object):
    def __init__(self, siren, tranche, dateff):
        self.siren = siren
        self.tranche = tranche.strip()
        self.dateff = Dateff(dateff)

    @classmethod
    def empty(cls):
        return ("", "", "")

    def __str__(self):
        return str((self.siren, self.tranche, str(self.dateff)))

    def get_tranche(self):
        return self.tranche

    def get_siren(self):
        return self.siren

    def to_tuple(self):
        return self.siren, self.tranche, self.dateff

    def to_tuple_data(self):
        return self.tranche, self.dateff


class InfnegDictList(dict):
    """
    Dictionnaire de liste d'infos négatives
    La clé du dictionnaire est le nom du fichier d'où proviennent les données
    Pour chaque clé, le dictionnaire contient la liste des enregistrements
        nom_du_fichier1 => [(infneg1), (infneg2), ...]
        nom_du_fichier2 => [(infneg1), (infneg2), ...]
        ...
    """

    def __init__(self, inputFileList):
        """
        Constructeur d'un dictionnaire des infos négatives, dont chaque entrée
         est associée à un nom de fichier et dont le contenu est initialisé
         comme une liste vide
        :param inputFileList: la liste des noms des fichiers
        """
        for inputFile in inputFileList:
            self[inputFile.name] = []

    def pretty_print(self):
        for keyName in self.keys():
            logging.info(keyName + " =>")
            for infneg in self[keyName]:
                logging.info("  " + str(infneg))

    def append_infneg_list(self, inputFileName, infnegList):
        """
        Permet d'ajouter une liste de données associée à un nom de fichier
        :param inputFileName: le nom du fichier
        :param infnegList: la liste des tuples de données de type Infneg
        :return: None
        """
        assert isinstance(inputFileName, str)
        assert isinstance(infnegList, list)
        self[inputFileName] = infnegList

    def append_infneg(self, inputFileName, infneg):
        """
        Ajoute un tuple à la liste associée à un nom de fichier
        :param inputFileName: le nom du fichier dont il faut compléter la liste de tuples
        :param infneg: le tuple qui contient une Infneg
        :return: None
        """
        assert isinstance(inputFileName, str)
        assert isinstance(infneg, Infneg)
        self[inputFileName].append(infneg)

    def get_siren_uniq_sorted(self, keyName=None):
        """
        :param keyName: le nom de la clé à utiliser
            Si None, alors toutes les clés disponibles sont parcourues
        :return: un set des sirens (uniques) pour une clé donnée du dictionnaire
        """
        if keyName is None:
            return sorted(set([infneg.get_siren() for keyName in self.keys() for infneg in self[keyName]]))
        else:
            assert isinstance(keyName, str)
            return sorted(set([infneg.get_siren() for infneg in self[keyName]]))

    def merge(self):
        """
        Transforme une instance de la classe InfnegDictList en un autre dict:
        InfnegDictList: est un dict dont la clé est le nom du fichier et dont chaque valeur est une liste de tuples
        type de sortie: est un dict dont la clé est le siren et dont chaque valeur est un tuple constitué des Infnegs
        des différents fichiers. Chaque Infneg est elle même un tuple de valeurs.

        :return: un dict de tuples de tuples de tuples
         key => siren
         Liste de tuples: un tuple par fichier d'origine
        """

        def build_dict_of_data_by_siren():
            merge_dict_tmp = {}
            for keyName in self.keys():
                v = []
                for infneg in self[keyName]:
                    v.append((infneg.get_siren(), infneg.to_tuple()))
                merge_dict_tmp[keyName] = dict(v)
            return merge_dict_tmp

        dict_of_data_by_siren = build_dict_of_data_by_siren()
        logging.debug(dict_of_data_by_siren)
        siren_set = self.get_siren_uniq_sorted()
        logging.debug(len(siren_set))
        merge_dict = {}
        for siren in siren_set:
            v = [
                (keyName, dict_of_data_by_siren[keyName][siren]) if dict_of_data_by_siren[keyName].has_key(siren) else (
                keyName, Infneg.empty()) for keyName in self.keys()]
            logging.debug(v)
            merge_dict[siren] = tuple(v)
        logging.info(merge_dict)
        return merge_dict

    @classmethod
    def merge_dict_write_csv(self, merge_dict, outputFileName):
        """
        Ecriture dans un fichier CSV des données du dict issu du merge
        :param merge_dict: doit avoir le type retourné par la fonction merge: un dict qui contient des tuples
        :param outputFileName: le nom du fichier CSV
        :return: None
        """
        # le parametre merge_dict
        assert isinstance(merge_dict, dict)
        assert isinstance(outputFileName, str)
        # pour déterminer les noms des champs à partir du 1er enregistrement
        tup0 = merge_dict[merge_dict.keys()[0]]
        logging.info("{} {} {}".format("tup0", type(tup0), len(tup0)))
        logging.info("tup0: {}".format(tup0))
        fieldnames_data = ['tranche', "dateff"]
        fieldnames = ['siren'] + [fd + str(i + 1) for i in range(len(tup0)) for fd in fieldnames_data]
        logging.info("Ecriture de {} enregistrements au format {}".format(len(merge_dict),fieldnames))
        # for siren in merge_dict.keys():
        #     tup0 = merge_dict[siren]
        #     fields = [(siren,)] + [tup0[i][1][1:] for i in range(len(tup0))]
        #     logging.info("fields: {}".format(flatten(fields)))
        #     logging.info("fields: {}".format(dict(zip(fieldnames,flatten(fields)))))
        with open(outputFileName, 'w') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='csvdefault')
            csv_writer.writeheader()
            for siren in merge_dict.keys():
                tup0 = merge_dict[siren]
                fields = [(siren,)] + [tup0[i][1][1:] for i in range(len(tup0))]
                logging.info("fields: {}".format(flatten(fields)))
                output = dict(zip(fieldnames, flatten(fields)))
                logging.info("fields: {}".format(output))
                csv_writer.writerow(output)
        return None


def main(path, inputFileList, outputFileName='output.txt'):
    # lecture des fichiers
    infnegsFiles = FilesOfInfnegs(path, inputFileList)
    infnegs = infnegsFiles.parseFileList()
    if logging._checkLevel(logging.DEBUG):
        for fic in infnegs.keys():
            logging.debug("File: {}".format(fic))
            for i, infneg in enumerate(infnegs[fic]):
                logging.debug("[{}] {}".format(i, infneg))

    # repartition par fichiers et tranches
    total_histg = {}
    tranches_histg = {}
    for fic in infnegs.keys():
        tranches_histg[fic] = {}
        total_histg[fic] = {}
        total_histg[fic]["total"] = 0
        logging.info("File: {}".format(fic))
        tranches_liste = [infneg.get_tranche() for infneg in infnegs[fic]]
        logging.debug(tranches_liste)
        for tranche in tranches_liste:
            total_histg[fic]["total"] += 1
            if tranches_histg[fic].has_key(tranche):
                tranches_histg[fic][tranche] += 1
            else:
                tranches_histg[fic][tranche] = 1
        for tranche in sorted(set(tranches_histg[fic].keys()), key=int):
            logging.info("{{{}: {}}}".format(tranche, tranches_histg[fic][tranche]))

        for total in sorted(set(total_histg[fic].keys())):
            logging.info("{{{}: {}}}".format(total, total_histg[fic][total]))

    # rapprochement des fichiers
    #  une table globale avec toutes les lignes de tous les fichiers
    #  cle = siren
    infnegs.pretty_print()
    infnegs_merge = infnegs.merge()
    InfnegDictList.merge_dict_write_csv(infnegs_merge, outputFileName)


#####################
# programme principal
#####################
if __name__ == "__main__":
    logger = logging.getLogger('root')
    FORMAT = "[%(asctime)s:%(levelname)-6s:%(name)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    # logging.basicConfig(filename='copyBilan.log', filemode='w', level=logging.DEBUG)
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logging.info('====================')
    logging.info('BEGIN: ' + str(datetime.datetime.today()))
    logging.info('Python plateforme  = ' + sys.version)
    logging.debug('sys.path   = ')
    for p in sys.path:
        logging.debug('    ' + p)
    logging.info('====================')
    # defaultDir = r"D:\Documents\Projets\work\Ellixium_IJCOF\test"   # pour tests
    defaultDir = r"D:\Documents\Projets\work\Ellixium_IJCOF\originaux"   # les fchiers comlplets
    inputFileListFull = [
        InputFile("IJRAPPR_INTRUMJU_1462320.rcv.trt_20160829", 'IJ1')
        , InputFile("IJ_RAPPROA_201609021046.TXT", 'IJ2')
        , InputFile("IJ_RAPPROB_201609021046.TXT", 'IJ2')
        , InputFile("IJ_RAPPROA_201609151002.TXT", 'IJ2')
        , InputFile("IJ_RAPPROB_201609151003.TXT", 'IJ2')]

    inputFileList1 = [InputFile("IJ_RAPPROB_201609021046.TXT", 'IJ2')]
    inputFileList2 = [
        InputFile("IJRAPPR_INTRUMJU_1462320.rcv.trt_20160829", 'IJ1')
        , InputFile("IJ_RAPPROA_201609021046.TXT", 'IJ2')]

    # launch_tests(path=defaultDir, inputFileList=inputFileList1)
    # launch_tests(path=defaultDir, inputFileList=inputFileList2)
    main(path=defaultDir, inputFileList=inputFileListFull)

    logging.info('====================')
    logging.info('END: ' + str(datetime.datetime.today()))
    logging.info('====================')
