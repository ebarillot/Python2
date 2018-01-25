# -*- coding: utf-8 -*-

#
# Fonctions utiles à un programme pour
# - gestion d'erreur, stack du prog en cas de plantage
#
from __future__ import unicode_literals, print_function

import datetime
import inspect
import logging
import sys
from os.path import basename

import cx_Oracle
from typing import Any
import psutil
from operator import itemgetter

__author__ = 'Emmanuel Barillot'


def _who_call_me():
    frame, filename, line_number, function_name, lines, index = inspect.stack()[2]
    return filename, line_number, function_name


def force_to_unicode(text):
    """If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"""
    return text if isinstance(text, unicode) else text.decode('utf8')


class LocalError(Exception):
    """
    Classe qui permet de gérer une erreur personnalisée
    Elle dérive de Exception
    """

    def __init__(self, exception, keyerr=None):
        # type: (Exception, unicode) -> None
        """
        Constructeur

        :param exception: le float à formater
        :param keyerr: une clé qui permet d'identifier l'erreur pour mieux repérer son origine dans le code
        :return: None
        """
        self.exception = exception
        self.keyerr = keyerr if keyerr else _who_call_me()[2]

    def __unicode__(self):
        # type: () -> unicode
        return self.keyerr + ":" + str(self.exception)

    def __str__(self):
        # type: () -> unicode
        return self.__unicode__()


def call_stack():
    # type: () -> unicode
    """
    Produit un résumé de la "stack call"

    :return: Une chaine de caractères qui contient un résumé de la "stack call"
    """
    str_out = None  # type: unicode
    if "inspect" not in globals().keys():
        import inspect
        stack = [frame[3] for frame in inspect.stack() if frame[3] not in [inspect.stack()[0][3], "<module>"]]
        str_out = '()->'.join(reversed(stack))
    return str_out


def mngt_error(error):
    # type: () -> None
    """
    Fonction qui gère le logging des erreurs
    Produit un résumé de la "stack call"

    :param error: objet erreur à traiter
    :return: rien
    """
    logging.error('Stack frame: ' + call_stack())
    if isinstance(error, cx_Oracle.DatabaseError):
        logging.error('DatabaseError: {}'.format(error))
    else:
        logging.error('Error: {}'.format(error))


DEFAULT_LOG_FORMAT = "[%(asctime)s:%(levelname)-5s] %(message)s"
DEFAULT_LOG_LEVEL = logging.INFO


def log_init(logger_name='root', level=DEFAULT_LOG_LEVEL):
    # type: (unicode) -> logging.Logger
    """
    Initialisation de la session de logging

    :param level:
    :param logger_name: le nom du nouveau logger
    :return: un objet logger0
    """
    # logging.basicConfig(filename='copyBilan.log', filemode='w', level=logging.DEBUG)
    logger = logging.getLogger(logger_name)
    logging.basicConfig(format=DEFAULT_LOG_FORMAT, level=level)
    logging.info('====================')
    logging.info('BEGIN: ' + str(datetime.datetime.today()))
    logging.info('plateforme = ' + sys.version)
    logging.info('sys.path   = ')
    for p in sys.path:
        logging.info('    ' + p)
    logging.info('====================')
    logging.info('Default encoding for str(): ' + sys.getdefaultencoding())
    logging.info('filesystem encoding: ' + sys.getfilesystemencoding())
    logging.info('====================')
    return logger


def log_exit():
    # type: (None) -> None
    """
    Terminaison de la session de logging

    :return: None
    """
    logging.info('====================')
    logging.info('END: ' + str(datetime.datetime.today()))
    logging.info('====================')


def get_fun_ref(fun_name, module_name=__name__):
    # type: (unicode) -> Any
    """
    Retourne une reference sur la fonction du module courant à partir de son nom
    :param fun_name: nom de la fonction dotn on cherche la référence
    :param module_name: le nom du module ù se trouve la fonction
    :return: référence vers une fonction
    """
    this = sys.modules[module_name]  # les modules de l'espace de nommage courant
    # attrs = dir(this) # tous les symboles connus dans sys.modules[__name__]
    fn = getattr(this, fun_name)
    return fn


# catalogue des fonctions de logging
logging_fun = {
    logging.INFO: logging.info
    , logging.WARNING: logging.warning
    , logging.ERROR: logging.error
    , logging.DEBUG: logging.debug
}


def log_write(s=u"", level=logging.INFO):
    # type: (unicode) -> None
    """
    Ecriture d'une ligne de logging
    ATTENTION: unicode obligatoire en entrée, ne gère pas une str
    :param s: une ligne à écrire
    :param level: niveau de gravité
    :return: None
    """
    # recupere les infos de l'appelant
    # frame, filename, line_number, function_name, lines, index = inspect.stack()[1]
    filename, line_number, function_name = _who_call_me()
    logging_fun[level]("[{}:{}:{}] {}".format(basename(filename), line_number, function_name, s))


def print_proc_rsrc():
    # pid = os.getpid()
    p = psutil.Process()
    with p.oneshot():
        log_write('--- name: {}'.format(p.name()))  # execute internal routine once collecting multiple info
        log_write('cpu_times: {}'.format(p.cpu_times()))  # return cached value
        log_write('cpu_percent: {}'.format(p.cpu_percent()))  # return cached value
        log_write('memory_info: ')  # return cached value
        mem_info_data = map(lambda x: x/1024L, p.memory_info())
        mem_info_names = ['rss', 'vms', 'num_page_faults', 'peak_wset', 'wset', 'peak_paged_pool', 'paged_pool', 'peak_nonpaged_pool', 'nonpaged_pool', 'pagefile', 'peak_pagefile', 'private']
        for name, data in itemgetter(0,1,3,4)(zip(mem_info_names, mem_info_data)):
            log_write('  {}  : {}'.format(name, data))  # return cached value

        # log_write('status: {}'.format(p.status())) # return cached value
        # log_write('create_time: {}'.format(p.create_time()))  # return cached value
        # log_write('memory use: {}'.format(p.memory_info()[3]/1024))

