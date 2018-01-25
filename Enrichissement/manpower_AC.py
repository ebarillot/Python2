#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Emmanuel Barillot'


#
# programme de recopie d'un bilan de PROD/clone vers DEV ou IA
#

import datetime
import sys
import cx_Oracle
import logging
from itertools import chain
from traceback import print_exc, format_stack
import csv

connstr = dict()
connstr['DEV'  ,'bileprod'] = 'bileprod/bileprod@devdbirisfr.int.dns:1521/svcproddev2.world'
connstr['IA'   ,'bileprod'] = 'bileprod/bileprodia@intdbirisfr.int.dns:1521/svcprodint1.world'
connstr['UA'   ,'bileprod'] = 'bileprod/bileprodpre@irisfrpx.int.dns:1523/SVCPRODPRE1.world'
connstr['clone','bileprod'] = 'etudes_consult/IF5489rG@dbirisclone.int.dns:1521/svcprodclo1.world'

connstr['DEV'  ,'fra2prod'] = 'fra2prod/fra2prod@devdbirisfr.int.dns:1521/svcproddev2.world'
connstr['IA'   ,'fra2prod'] = 'fra2prod/fra2prodia@intdbirisfr.int.dns:1521/svcprodint1.world'
connstr['UA'   ,'fra2prod'] = 'fra2prod/fra2prodpre@irisfrpx.int.dns:1523/SVCPRODPRE1.world'
connstr['clone','fra2prod'] = 'etudes_consult/IF5489rG@dbirisclone.int.dns:1521/svcprodclo1.world'

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


def get_AC(entnum, curs, typreq):
    """
    Selectionne les lignes d'une table à partir de critères

    :param entnum: numero entrep
    :param cursor: curseur ouvert sur le schéma auquel appartient la table
    :return: les lignes de la table sélectionnées
    """

    if typreq == 'dateff':
        # requete avec dateff dans l'order by du row_number()
        req = \
            """select
                  inf_entnum
                , case when inf_ac1mnt is not NULL then to_char(inf_ac1mnt) else inf_ac1com end
                , to_char(inf_dateff,'YYYY-MM-DD')
                , inf_ac1typcod
            from
            (
                select
                  inf_entnum
                , inf_ac1mnt
                , inf_ac1com
                , inf_dateff
                , inf_ac1typcod
                --, sco_etatcod
                --, sco_sup
                --, sco_seq_pk
                --, inf_seq_pk
                --, inf_datord
                , row_number() over (partition by inf_entnum order by decode(
                      sco_etatcod,'ACT',1,2) asc
                    , trunc(inf_dateff) desc
                    , inf_sco_seq desc
                    , inf_seq_pk desc) rn
                from fra2prod.ac1_infos, fra2prod.scores_rating
                where inf_sup is null
                and   sco_sup is null
                and   sco_etatcod = 'ACT'
                and   sco_seq_pk = inf_sco_seq
                and   sco_entnum_pk = inf_entnum
                and   sco_entnumtyp_pk = inf_entnumtyp
            )
            where rn <= 1
            and inf_entnum = :v1
            """
    elif typreq == 'datord':
        # requete avec datord dans l'order by du row_number()
        req = \
            """select
                  inf_entnum
                , case when inf_ac1mnt is not NULL then to_char(inf_ac1mnt) else inf_ac1com end
                , to_char(inf_dateff,'YYYY-MM-DD')
                , inf_ac1typcod
            from
            (
                select
                  inf_entnum
                , inf_ac1mnt
                , inf_ac1com
                , inf_dateff
                , inf_ac1typcod
                --, sco_etatcod
                --, sco_sup
                --, sco_seq_pk
                --, inf_seq_pk
                --, inf_datord
                , row_number() over (partition by inf_entnum order by decode(
                      sco_etatcod,'ACT',1,2) asc
                    , trunc(inf_datord) desc
                    , inf_sco_seq desc
                    , inf_seq_pk desc) rn
                from fra2prod.ac1_infos, fra2prod.scores_rating
                where inf_sup is null
                and   sco_sup is null
                and   sco_etatcod = 'ACT'
                and   sco_seq_pk = inf_sco_seq
                and   sco_entnum_pk = inf_entnum
                and   sco_entnumtyp_pk = inf_entnumtyp
            )
            where rn <= 1
            and inf_entnum = :v1
            """
    elif typreq == 'ihm_iris':
        # requete avec datord dans l'order by du row_number()
        req = \
            """
            select
                  inf_entnum
                , case when inf_ac1mnt is not NULL then to_char(inf_ac1mnt) else inf_ac1com end
                , to_char(inf_dateff,'YYYY-MM-DD')
                , inf_ac1typcod
            FROM (
              SELECT row_number() over (order by ac.inf_seq_pk desc) rn, ac.inf_entnum, ac.inf_ac1mnt, ac.inf_ac1com, ac.inf_dateff, ac.inf_ac1typcod 
              FROM fra2prod.ac1_infos ac
              WHERE ac.inf_entnumtyp = 0
              and ac.inf_entnum = :v1
              and ac.inf_sup is null
              and ac.inf_ac1statutcod = 'OK'
              and ac.inf_sco_seq in (
                select sco_seq_pk
                from fra2prod.scores_rating
                where sco_entnumtyp_pk = 0
                and sco_entnum_pk = :v1
                and sco_sup is null
                and sco_etatcod = 'ACT')
            )
            WHERE rn <= 1
            """
    else:
        raise(Exception('typreq inconnu:'+typreq))

    try:
        curs.execute(req, {'v1': entnum})
        row = curs.fetchone()
        logger.debug(row)
        return row
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,"entnum:"+str(entnum))
        mngtError(le)
        raise (le)


def format_siren(entnum):
    manque = 9-len(entnum)
    if manque >= 0:
        return '0' * manque + entnum
    else:
        return None

#
def enrich_AC(fileNameIn, fileNameOut, base_from, typreq):
    """
    Fonction qui copie les jugements disponibles dans une base Oracle vers une autre.
    Le schéma bileprod doit exister dans les deux bases et la base de destination doit être accessible en écriture.

    :param fileNameIn: [obligatoire] le siren pour les bilans à copier
    :param base_from: [obligatoire] object base de données d'origine
    :return: rien
    """
    conn_from = cx_Oracle.connect(connstr[base_from])
    curs_from = conn_from.cursor()
    f_in = open(fileNameIn, 'r')
    f_out = open(fileNameOut, 'w')
    reader = csv.reader(f_in, 'csvdefault')
    fieldnames = ['Siren', 'Raison Sociale', 'Auto', 'Montant', 'Date effet']
    writer = csv.DictWriter(f_out, fieldnames=fieldnames, dialect='csvdefault')
    i_line = 0
    writer.writeheader()
    with f_in, f_out, conn_from:
        logging.info('sysdate bdd from: '+ str(getSysdate(curs_from)))
        for f_line in reader:
            #logger.debug(f_line)
            i_line += 1
            entnum, deno = f_line
            if entnum == 'Siren':
                continue
            # reformatter le siren: zéros à gauche
            entnum = format_siren(entnum)
            ac_entnum, ac_val, ac_date, ac_auto = get_AC(entnum=entnum, curs=curs_from, typreq=typreq)
            writer.writerow(dict(zip(fieldnames, [ac_entnum, deno, ac_auto, str(ac_val), str(ac_date)])))
            if i_line%1000 == 0:
                logging.info('Lignes traitées: {}'.format(i_line))
            #if i_line >= 1000:
            #    break


#####################
# programme principal
#####################
if __name__ == "__main__":
    """
    Programme qui permet d'enrichir un fichier CSV à partir de données en bdd
    """
    # logging.basicConfig(filename='copyBilan.log', filemode='w', level=logging.DEBUG)
    logger = logging.getLogger('root')
    FORMAT = "[%(asctime)s:%(levelname)-7s:%(name)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    #logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    logging.info ('====================')
    logging.info ('BEGIN: ' + str(datetime.datetime.today()))
    logging.info ('plateforme = ' + sys.version)
    logging.info ('sys.path   = ')
    for p in sys.path:
        logging.info ('    '+p)
    logging.info ('====================')
    base_from   = 'clone', 'fra2prod'

    # enrichCSV (entnum='428278394', base_from=base_from, base_to=base_to)
    # enrich_AC(fileNameIn=r'C:\Users\emmanuel_barillot\Documents\Work\Manpower\2017-12-18\siren_manpower.csv'
    #             , fileNameOut = r'C:\Users\emmanuel_barillot\Documents\Work\Manpower\2017-12-18\siren_manpower_avec_AC_datord.csv'
    #             , base_from=base_from
    #             , typreq='datord')

    # enrich_AC(fileNameIn=r'C:\Users\emmanuel_barillot\Documents\Work\Manpower\2017-12-18\siren_manpower.csv'
    #             , fileNameOut = r'C:\Users\emmanuel_barillot\Documents\Work\Manpower\2017-12-18\siren_manpower_avec_AC_dateff.csv'
    #             , base_from=base_from
    #             , typreq = 'dateff')

    enrich_AC(fileNameIn=r'C:\Users\emmanuel_barillot\Documents\Work\Manpower\2017-12-21\siren_manpower.csv'
                , fileNameOut = r'C:\Users\emmanuel_barillot\Documents\Work\Manpower\2017-12-21\siren_manpower_avec_AC_ihm_iris.csv'
                , base_from=base_from
                , typreq = 'ihm_iris')



    logging.info ('====================')
    logging.info ('END: ' + str(datetime.datetime.today()))
    logging.info ('====================')
