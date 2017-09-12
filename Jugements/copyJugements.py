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
import csv
from itertools import chain
from traceback import print_exc, format_stack

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
    logging.error('Stack frame: '+call_stack())
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


def getTabColumns(curs, tabname):
    curs.execute("select COLUMN_NAME from user_tab_columns where table_name = :tab order by column_id asc",(tabname,))
    try:
        tupleOfTuples = curs.fetchall()
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,tabname)
        mngtError(le)
        raise (le)
    return [element for tupl in tupleOfTuples for element in tupl]


def getTabNonVirtualColumns(curs, tabname):
    curs.execute("select COLUMN_NAME from user_tab_cols" \
                    " where table_name = :tab" \
                    " and virtual_column = 'NO'" \
                    " order by column_id asc",(tabname,))
    try:
        tupleOfTuples = curs.fetchall()
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,tabname)
        mngtError(le)
        raise (le)
    return [element for tupl in tupleOfTuples for element in tupl]


def getTabColumnsCount(curs, tabname):
    curs.execute("select count(*) from user_tab_columns where table_name = :tab",(tabname,))
    try:
        (nb,) = curs.fetchone()
    except cx_Oracle.DatabaseError as e:
        mngtError(LocalError(e,tabname))
        raise
    return nb


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


def getRowsOtherTablesFromKey (curs, schema, tabname, cols, keycols, keyvals):
    """
    Selection d'une ligne dans une table de la famille "bilan"

    :param curs: curseur ouvert sur le schéma auquel appartient la table
    :param bilseq: la clé de la table
    :param tabname: le nom de la table
    :param cols: le nom des colonnes à extraire
    :return: la ligne selectionnée
    """
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
        row = curs.fetchone()
        return row
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,tabname+","+str(keyvals))
        mngtError(le)
        raise (le)


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


def insert_into(curs, row, tabname, cols):
    """
    Insertion des données dans une table de la famille bilan

    :param curs: curseur ouvert sur le schéma auquel appartient la table
    :param row: tuple qui contient les valeurs de la ligne à insérer
    :param tabname: le nom de la table
    :param cols: le nom des colonnes à insérer, leur nombre et leur ordre doit correspondre à ce qui est dans row
    :return: rien
    """
    colsToInsert = ','.join(cols)
    ph = ','.join([':'+str(elem) for elem in range(1,len(cols)+1)])
    ins_bil = "insert into " + tabname + " (" + colsToInsert + ") values (" + ph +")"
    try:
        curs.execute(ins_bil, row)
        logging.info(tabname+' insert OK : '+str(row[:4])+'...')   # TODO à améliorer
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        if error.code == 1:
            logging.warning('La ligne existe déjà : '+str(row[:4])+'...')   # TODO à améliorer
        else:
            le = LocalError("insert:"+str(row),e)
            mngtError(le)
            raise (le)


def insert_many_into(curs, schema, tabname, cols, rows):
    """
    Insertion de plusieurs lignes dans une table de la famille bilan
    Insertion des données en bloc

    :param curs: curseur ouvert sur le schéma auquel appartient la table
    :param schema: le nom du schema auquel appartient la table tabname
    :param tabname: le nom de la table
    :param cols: le nom des colonnes à insérer, leur nombre et leur ordre doit correspondre à ce qui est dans row
    :param rows: tuples qui contiennent les valeurs des lignes à insérer
    :return: rien
    """
    curs.bindarraysize = len(rows)
    colsToInsert = ','.join(cols)
    ph = ','.join([':'+str(elem) for elem in range(1,len(cols)+1)])
    ins_req = "insert into " + schema + '.' + tabname + " (" + colsToInsert + ") values (" + ph + ")"
    try:
        curs.executemany(ins_req, rows)
        for row in rows:
            logging.info(tabname+' insert OK : ' + str(row[:4])+'...')   # TODO à améliorer
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,tabname+" insert: " + tabname)
        mngtError(le)
        # en cas d'échec par bloc, on essaie ligne par ligne
        for row in rows:
            insert_into (curs=curs, row=row, tabname=tabname, cols=cols)


# copie d'un bilan d'une base à l'autre
def copyJugement (entnum, base_from, base_to):
    """
    Fonction qui copie les jugements disponibles dans une base Oracle vers une autre.
    Le schéma bileprod doit exister dans les deux bases et la base de destination doit être accessible en écriture.

    :param entnum: [obligatoire] le siren pour les bilans à copier
    :param base_from: [obligatoire] object base de données d'origine
    :param base_to:  [obligatoire] object base de données de destination
    :return: rien
    """
    conn_from = cx_Oracle.connect(connstr[base_from])
    curs_from = conn_from.cursor()
    conn_to = cx_Oracle.connect(connstr[base_to])
    curs_to = conn_to.cursor()
    columns = {}
    tabnames = {'JUGEMENT':['JUGHISM']}
    tabschema = {'JUGEMENT':'fra2prod',
                 'JUGHISM' :'fra2prod'}
    tabkeys = {   'JUGEMENT'    :('JUGENTNUM','JUGENTNUMTYP','JUGSEQ')
                , 'JUGHISM'     :('JUGHISENTNUM','JUGHISENTNUMTYP','JUGHISJUGSEQ')
               }
    with conn_from, conn_to:
        logging.info('sysdate bdd from: '+ str(getSysdate(curs_from)))
        logging.info('sysdate bdd to: '  + str(getSysdate(curs_to  )))
        # pour toutes les tables de niveau 1
        # c'est à dire dont le nom est une clé du dict des tables
        for tabname_1 in tabnames.iterkeys():
            nb = getTabColumnsCount(curs_to, tabname_1)
            logging.info('Table ' + tabname_1 + ' : ' + str(nb) + ' colonnes')
            columns[tabname_1] = getTabNonVirtualColumns(curs_to, tabname_1)
            logging.debug(','.join(columns[tabname_1]))
            count_from = getCount(curs=curs_from, schema=tabschema[tabname_1],tabname=tabname_1, keycols=('jugentnum',), keyvals=(entnum,))
            logging.info (tabname_1+" entnum="+entnum+", count_from = " + str(count_from))
            rows = getRows(curs=curs_from, schema=tabschema[tabname_1], tabname=tabname_1, cols=columns[tabname_1], keycols=('jugentnum',), keyvals=(entnum,))
            logging.info(tabname_1+" Extraction : %d rows" % len(rows))
            insert_many_into (curs=curs_to, schema=tabschema[tabname_1], tabname=tabname_1, cols=columns[tabname_1], rows=rows)
            for row_1 in rows:
                # row_1_key = tuple([row_1[columns[tabname_1].index(keylib)] for keylib in list(chain.from_iterable(tabkeys[tabname_1]))])
                row_1_key = tuple([row_1[columns[tabname_1].index(keylib)] for keylib in tabkeys[tabname_1]])
                # pour toutes les tables de niveau 2
                # c'est à dire dont le nom est une valeur du tuple du dict des tables
                for tabname_2 in tabnames[tabname_1]:
                    nb = getTabColumnsCount(curs=curs_to, tabname=tabname_2)
                    logging.info('Table ' + tabname_2 + ' : ' + str(nb) + ' colonnes')
                    columns[tabname_2] = getTabNonVirtualColumns(curs_to, tabname_2)
                    logging.debug(','.join(columns[tabname_2]))
                    rows_2 = getRows (curs=curs_from
                                    , schema=tabschema[tabname_2]
                                    , tabname=tabname_2
                                    , cols=columns[tabname_2]
                                    , keycols=tabkeys[tabname_2]
                                    , keyvals=row_1_key)
                    if rows_2 is not None:
                        logging.info("Extraction : %d fields" % len(rows_2))
                        insert_many_into (curs=curs_to, schema=tabschema[tabname_2], tabname=tabname_2, cols=columns[tabname_2], rows=rows_2)
                    else:
                        logging.warning("Extraction : aucune ligne dans %s pour jugseq = %s", tabname_2, str(row_1_key))
        try:
            curs_from.close()
            curs_to.close()
        except cx_Oracle.DatabaseError as e:
            le = LocalError(e,str(entnum))
            mngtError(le)


def delete_row(curs, schema, tabname, keycols, keyvals):
    """
    Suppression d'une ligne
    :param curs: curseur ouvert sur le schéma auquel appartient la table
    :param tabname: le nom de la table
    :param keycols: le nom des colonnes de la clé
    :param keyvals: les valeurs de la clé
    :return: rien
    """
    ph = ' and '.join([col +'=:' + col for col in keycols])
    del_bil = "delete from " + schema + '.' + tabname + " where " + ph
    try:
        curs.execute(del_bil, keyvals)
        # logging.info(tabname+' delete OK : '+str(row[:4])+'...')   # TODO à améliorer
        logging.info(tabname + ' delete OK : ' + str(zip(keycols, keyvals[:4])) + '...')   # TODO à améliorer
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e, tabname + "," + str(keyvals))
        mngtError(le)
    return None


def delete_many_rows (curs, schema, tabname, keycols, rows):
    """
    Suppression de plusieurs lignes
    :param curs: curseur ouvert sur le schéma auquel appartient la table
    :param rows: les valeurs de la clé des différentes lignes
    :param tabname: le nom de la table
    :param keycols: le nom des colonnes de la clé
    :return: rien
    """
    for row in rows:
        delete_row(curs, schema, tabname, keycols, row)


def deleteBilan (entnum, annee, origine, typbil, base_to):
    """
    Fonction qui supprime les bilans disponibles dans une base Oracle.
    La base de destination doit être accessible en écriture.

    :param entnum: [obligatoire] le siren pour les bilans à copier
    :param annee: [facultatif] année des bilans à copier
    :param origine: [facultatif] origine des bilans à copier
    :param typbil:  [facultatif] type des bilans à copier
    :param base_to:  [obligatoire] object base de données de travail
    :return: rien
    """
    conn_to = cx_Oracle.connect(connstr[base_to])
    curs_to = conn_to.cursor()
    tabnames = {'JUGEMENT':('JUGHISM')}
    tabschema = {'JUGEMENT':'fra2prod',
                 'JUGHISM' :'fra2prod'}
    tabkeys = {   'JUGEMENT'    :[('JUGENTNUM','JUGENTNUMTYP','JUGSEQ')]
                , 'JUGHISM'     :[('JUGHISENTNUM','JUGHISENTNUMTYP','JUGHISJUGSEQ','JUGHISDATORD')]
               }
    with conn_to:
        logging.info('sysdate bdd to: '  +str(getSysdate(curs_to)))
        # pour toutes les tables de niveau 1
        # c'est à dire dont le nom est une clé du dict des tables
        for tabname_1 in tabnames.iterkeys():
            bilan_count_from = getCount(curs=curs_to, entnum=entnum, annee=annee, typbil=typbil)
            logging.info ("entnum="+entnum+", annee="+strOrNone(annee)+", typbil="+strOrNone(typbil)+", bilan_count_from = "+str(bilan_count_from))
            rows = getRows (curs=curs_to, entnum=entnum, annee=annee, origine=origine, typbil=typbil, tabname=tabname_1, cols=tabkeys[tabname_1])
            logging.info("Extraction : %d rows" % len(rows))
            for row_1 in rows:
                bilseq = row_1[tabkeys[tabname_1].index('BILSEQ')]
                # bilseq = row_1[0]  # TODO à rendre générique en fonction du nb de colonnes dans la clé
                # pour toutes les tables de niveau 2
                # c'est à dire dont le nom est une valeur du tuple du dict des tables
                for tabname_2 in tabnames[tabname_1]:
                    row_2 = getRowsOtherTablesFromKey (curs=curs_to, bilseq=bilseq, tabname=tabname_2, cols=tabkeys[tabname_2])
                    if row_2 is not None:
                        logging.info("tabname="+tabname_2+", bilseq="+str(bilseq)+", Extraction : " + str(row_2))
                        delete_row (curs=curs_to, keyvals=row_2, tabname=tabname_2, keycols=tabkeys[tabname_2])
                    else:
                        logging.warning("Extraction : aucune ligne dans %s pour bilseq = %s", tabname_2, str(bilseq))
            # on supprime à la fin la ligne de la table de 1er niveau
            delete_many_rows (curs=curs_to, rows=rows, tabname=tabname_1, keycols=tabkeys[tabname_1])

        try:
            curs_to.close()
        except cx_Oracle.DatabaseError as e:
            le = LocalError(e,entnum+","+annee+","+origine+","+typbil)
            mngtError(le)

#####################
# programme principal
#####################
if __name__ == "__main__":
    """
    Programme qui fournit des exemples d'appel de la fonction copyBilan ()
    """
    # logging.basicConfig(filename='copyBilan.log', filemode='w', level=logging.DEBUG)
    logger = logging.getLogger('root')
    FORMAT = "[%(asctime)s:%(levelname)-7s:%(name)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    # logging.basicConfig(format=FORMAT, level=logging.INFO)
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    logging.info ('====================')
    logging.info ('BEGIN: ' + str(datetime.datetime.today()))
    logging.info ('plateforme = ' + sys.version)
    logging.info ('sys.path   = ')
    for p in sys.path:
     logging.info ('    '+p)
    logging.info ('====================')
    base_from   = 'clone', 'fra2prod'
    base_to     = 'DEV', 'fra2prod'
    # base_to     = 'IA', 'bileprod'
    # base_to     = 'UA', 'bileprod'

    # enrichCSV (entnum='428278394', base_from=base_from, base_to=base_to)
    copyJugement (entnum='519428650', base_from=base_from, base_to=base_to)

#
#519428650

    logging.info ('====================')
    logging.info ('END: ' + str(datetime.datetime.today()))
    logging.info ('====================')
