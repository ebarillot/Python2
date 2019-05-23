#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Emmanuel Barillot'


#
# programme d'enrichissement d'un fichier CSV avec des données en base Oracle
#

import datetime
import sys
import cx_Oracle
import logging
import csv
from traceback import format_stack

connstr = dict()
connstr['DEV'  ,'bileprod'] = 'bileprod/bileprod@devdbirisfr.int.dns:1521/svcproddev2.world'
connstr['IA'   ,'bileprod'] = 'bileprod/bileprodia@intdbirisfr.int.dns:1521/svcprodint1.world'
connstr['UA'   ,'bileprod'] = 'bileprod/bileprodpre@irisfrpx.int.dns:1523/SVCPRODPRE1.world'
connstr['clone','bileprod'] = 'etudes_consult/IF5489rG@dbirisclone.int.dns:1521/svcprodclo1.world'

connstr['DEV'  ,'fra2prod'] = 'fra2prod/fra2prod@devdbirisfr.int.dns:1521/svcproddev2.world'
connstr['IA'   ,'fra2prod'] = 'fra2prod/fra2prodia@intdbirisfr.int.dns:1521/svcprodint1.world'
connstr['UA'   ,'fra2prod'] = 'fra2prod/fra2prodpre@irisfrpx.int.dns:1523/SVCPRODPRE1.world'
connstr['clone','fra2prod'] = 'etudes_consult/IF5489rG@dbirisclone.int.dns:1521/svcprodclo1.world'

connstr['DEV'  ,'ort2prod'] = 'ort2prod/ort2prod@devdbirisfr.int.dns:1521/svcdiffdev2.world'
connstr['IA'   ,'ort2prod'] = 'ort2prod/ort2prodia@intdbirisfr.int.dns:1521/svcdiffint1.world'
connstr['UA'   ,'ort2prod'] = 'ort2prod/ort2prodpre@irisfrpx.int.dns:1523/svcdiffpre1.world'
connstr['clone','ort2prod'] = 'etudes_consult/IF5489rG@dbirisclone.int.dns:1521/svcdiffclo1.world'

csv.register_dialect('csvdefault', delimiter=';', quoting=csv.QUOTE_NONE, lineterminator='\n')


class LocalError(Exception):
    def __init__(self, exception, keyerr):
        self.exception = exception
        self.keyerr = keyerr

    def __str__(self):
        return "keyerr: " + str(self.keyerr) + ":" + str(self.exception)


def call_stack():
    """
    Produit un résumé de la "stack call"

    :return: Une chaine de caractères qui contient un résumé de la "stack call"
    """
    # if "inspect" not in globals().keys():
    #     import inspect
    # stack = [frame[3] for frame in inspect.stack()
    #          if frame[3] not in [inspect.stack()[0][3],"<module>"]]
    # s='()->'.join(reversed(stack))
    s = format_stack()
    return s


def mngtError(error):
    """
    Fonction qui gère le logging des erreurs
    Produit un résumé de la "stack call"

    :param error: objet erreur à traiter
    :return: rien
    """
    logging.error('Stack frame: '+str(call_stack()))
    if isinstance(error,cx_Oracle.DatabaseError):
        logging.error('DatabaseError: {}'.format(error))
    else:
        logging.error('Error: {}'.format(error))


def floatOrNoneToStr(a_float, a_format):
    """
    Formattage  d'un float qui gère le fait qu'il soit None

    :param a_float: le float à formater
    :param a_format: le format attendu
    :return: le float formaté ou une chaine vide
    """
    return ("" if a_float is None else format(a_float,a_format))


def strOrNone(s):
    """
    Retourne une chaine vide si None

    :param s: la chaine de caractere à tester
    :return: une chaine vide "" ou la chaine non vide
    """
    return ("" if s is None else s)


def getSysdate(curs):
    try:
        curs.execute('select sysdate from dual')
        the_sysdate, = curs.fetchone()
        return the_sysdate
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,"sysdate")
        mngtError(le)
        raise(le)


def getCount(curs, schema, tabname, keycols, keyvals):
    try:
        logging.debug("keyvals = " + str(keyvals))
        tabprefix = 'b'
        ph = ' and '.join([tabprefix+'.'+col +'=:' + col for col in keycols])
        req = "select count(*)" \
                + " from " + schema + '.' + tabname + " " + tabprefix \
                + " where " + ph
        curs.execute(req, dict(zip(keycols, keyvals)))
        (nb,) = curs.fetchone()
        return nb
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,tabname+","+str(keyvals))
        mngtError(le)
        raise(le)


def getRows(curs, schema, tabname, cols, keycols, keyvals):
    """
    Selectionne les lignes d'une table à partir de critères

    :param curs: curseur ouvert sur le schéma auquel appartient la table
    :param schema: le schéma Oracle de la table à requêter
    :param tabname: la table à requêter
    :param cols: les colonnes attendues en sortie
    :param keycols: les noms des colonnes dans la clause where
    :param keyvals: les valeurs des colonnes dans la clause where
    :return: les lignes de la table sélectionnées
    """
    if keyvals is None:
        raise ValueError('clé non renseigné')
    logging.debug("keyvals = " + str(keyvals))
    tabprefix = 'b'
    ph = ' and '.join([tabprefix+'.'+col +'=:' + col for col in keycols])
    colsToSelect = ','.join(map(lambda (x,y) : x+y, zip([tabprefix+'.']*len(cols), cols)))
    req = "select " \
            + colsToSelect \
            + " from " + schema + '.' + tabname + " " + tabprefix \
            + " where " + ph

    try:
        curs.execute(req, dict(zip(keycols, keyvals)))
        rows = curs.fetchall()
        return rows
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,"keyvals:"+str(keyvals))
        mngtError(le)
        raise (le)


def enrichCSV(entnums, base_from):
    """
    Fonction qui va chercher les données en base, siren par siren

    :param entnums: [obligatoire] liste des sirens à enrichir
    :param base_from: [obligatoire] object base de données d'origine
    :return: rien
    """
    conn_from = cx_Oracle.connect(connstr[base_from])
    curs_from = conn_from.cursor()
    tabschema = {
            'ENTREP'            : 'ort2prod'
        ,   'SCORES_RATING'     : 'ort2prod'
        ,   'IDCELLIXIUM'       : 'ort2prod'
    }
    tabcols = {
            'ENTREP'          :('entnum', 'entdenoff', 'entcatjurcod')
        ,   'SCORES_RATING'   :('sco_score',)
        ,   'IDCELLIXIUM'     :('elx_elxidccod',)
    }
    tabkeyscols = {
            'ENTREP'          :('entnum',)
        ,   'SCORES_RATING'   :('sco_entnum_pk','sco_etatcod')
        ,   'IDCELLIXIUM'     :('elx_entnum','elx_etatcod')
    }
    rows = {}
    outs=[]  # liste de tuples en sortie
    with conn_from:
        logging.info('sysdate bdd from: '+ str(getSysdate(curs_from)))
        for entnum in entnums:
            tabkeysvals = {
                    'ENTREP'          :(entnum,)
                ,   'SCORES_RATING'   :(entnum,'ACT')
                ,   'IDCELLIXIUM'     :(entnum,'ACT')
            }
            # pour toutes les tables de niveau 1
            # c'est à dire dont le nom est une clé du dict des tables
            for tabname_1 in tabschema.iterkeys():
                # count_from[tabname_1] = getCount(
                #         curs    =   curs_from
                #     ,   schema  =   tabschema[tabname_1]
                #     ,   tabname =   tabname_1
                #     ,   keycols =   tabkeyscols[tabname_1]
                #     ,   keyvals =   tabkeysvals[tabname_1]
                # )
                # logging.info (tabname_1 + " entnum=" + entnum + ", count_from = " + str(count_from))
                rows[tabname_1] = getRows(
                        curs    =   curs_from
                    ,   schema  =   tabschema[tabname_1]
                    ,   tabname =   tabname_1
                    ,   cols    =   tabcols[tabname_1]
                    ,   keycols =   tabkeyscols[tabname_1]
                    ,   keyvals =   tabkeysvals[tabname_1]
                )
                # logging.info(tabname_1+" Extraction : %d rows" % len(rows))

            # on verifie l'existance d'une valeur : à rendre plus generique et parametrable,
            # utilisation de index sur tabcols, boucle ?
            try:
                _score = rows['SCORES_RATING'][0][0]
            except:
                _score = ''
            try:
                _idc = rows['IDCELLIXIUM'][0][0]
            except:
                _idc = 'NA'
            try:
                _deno = rows['ENTREP'][0][1]
                _cju  = rows['ENTREP'][0][2]
            except:
                _deno = ''
                _cju  = ''

            # le resultat est un tuple
            out = (entnum, _idc, _cju, _score, _deno)
            outs.append(out)

        try:
            curs_from.close()
        except cx_Oracle.DatabaseError as e:
            le = LocalError(e, str(entnum))
            mngtError(le)
    return outs


#####################
# programme principal
#####################
if __name__ == "__main__":
    logger = logging.getLogger('root')
    FORMAT = "[%(asctime)s:%(levelname)-7s:%(name)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    # logging.basicConfig(filename='copyBilan.log', filemode='w', level=logging.DEBUG)
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    # logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    logging.info ('====================')
    logging.info ('BEGIN: ' + str(datetime.datetime.today()))
    logging.info ('plateforme = ' + sys.version)
    logging.info ('sys.path   = ')
    for p in sys.path:
        logging.info ('    '+p)
    logging.info ('====================')
    base_from   = 'clone', 'ort2prod'

    # fileNameIn = 'input.csv'
    fileNameIn = '2016-07-04-Ellixium_Unilend_in.txt'
    fileNameOut = fileNameIn.replace("_in.txt", "_out.csv")
    fieldnames = ['entnum', 'Ellix', 'fj', 'score', 'nom']  # en relation avec tabcols
    entnums=[]  # liste de siren en entrée
    outs=[]  # liste de tuples en sortie
    with open(fileNameIn, 'rb') as f:
        reader = csv.reader(f, 'csvdefault')
        for row in reader:
            # print row
            entnums.append(row[0])

    outs = enrichCSV(entnums=entnums, base_from=base_from)

    with open(fileNameOut, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, dialect='csvdefault')
        writer.writeheader()
        for out in outs:
            writer.writerow(
                {
                    fieldnames[0]: out[0]
                ,   fieldnames[1]: out[1]
                ,   fieldnames[2]: out[2]
                ,   fieldnames[3]: out[3]
                ,   fieldnames[4]: out[4]
                }
            )

    logging.info ('====================')
    logging.info ('END: ' + str(datetime.datetime.today()))
    logging.info ('====================')
