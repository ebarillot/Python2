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

__author__ = 'Emmanuel Barillot'


def force_to_unicode(text):
    """If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"""
    return text if isinstance(text, unicode) else text.decode('utf8')


class LocalError(Exception):
    """
    Classe qui permet de gérer une erreur personnalisée
    Elle dérive de Exception
    """

    def __init__(self, exception, keyerr):
        # type: (Exception, unicode) -> None
        """
        Constructeur

        :param exception: le float à formater
        :param keyerr: une clé qui permet d'identifier l'erreur pour mieux repérer son origine dans le code
        :return: None
        """
        self.exception = exception
        self.keyerr = keyerr

    def __unicode__(self):
        # type: () -> unicode
        return "keyerr: " + self.keyerr + ":" + unicode(self.exception) if '2' == sys.version[:1] else str(
            self.exception)

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


# TODO créer une classe Logger(Logging) ?
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
    logging.info(
        'BEGIN: ' + unicode(datetime.datetime.today()) if '2' == sys.version[:1] else str(datetime.datetime.today()))
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
    logging.info(
        'END: ' + unicode(datetime.datetime.today()) if '2' == sys.version[:1] else str(datetime.datetime.today()))
    logging.info('====================')


# retourne une reference sur la fonction du module courant à partir de son nom
def get_fun_ref(fun_name, module_name=__name__):
    # type: (unicode) -> Any
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


def log_write(s="", level=logging.INFO):
    # type: (unicode) -> None
    """
    Ecriture d'une ligne de logging
    :param s: une ligne à écrire
    :return: None
    """
    # recupere les infos de l'appelant
    frame, filename, line_number, function_name, lines, index = inspect.stack()[1]
    logging_fun[level]("[{}:{}:{}] {}".format(basename(filename), line_number, function_name, s))
