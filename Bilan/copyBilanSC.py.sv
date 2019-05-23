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
    str = None
    if "inspect" not in globals().keys():
        import inspect
        stack = [frame[3] for frame in inspect.stack()
            if frame[3] not in [inspect.stack()[0][3],"<module>"]]
        str = '()->'.join(reversed(stack))
    return str


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


def getTabColumns(curs, tabname):
    curs.execute("select COLUMN_NAME from user_tab_columns where table_name = :tab order by column_id asc",(tabname,))
    try:
        tupleOfTuples = curs.fetchall()
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,tabname)
        mngtError(le)
        raise
    return [element for tupl in tupleOfTuples for element in tupl]


def getTabColumnsCount(curs, tabname):
    curs.execute("select count(*) from user_tab_columns where table_name = :tab",(tabname,))
    try:
        (nb,) = curs.fetchone()
    except cx_Oracle.DatabaseError as e:
        mngtError(LocalError(e,tabname))
        raise
    return nb


def getBilanCount(curs, entnum, annee, typbil):
    curs.execute("SELECT count(*) FROM bileprod.bilan" \
                 + " where typbilcod                 = :typbil" \
                 + " and   to_char(bildatclo,'YYYY') = :datclo" \
                 + " and   entrcs                    = :entnum",
                 {'typbil':typbil, 'datclo':annee, 'entnum':entnum})
    try:
        (nb,) = curs.fetchone()
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,entnum+","+annee+","+typbil)
        mngtError(le)
        raise
    return nb


def getBilanOtherTablesFromBilseq (curs, bilseq, tabname, cols):
    """
    Selection d'une ligne dans une table de la famille "bilan"

    :param curs: curseur ouvert sur le schéma auquel appartient la table
    :param bilseq: la clé de la table
    :param tabname: le nom de la table
    :param cols: le nom des colonnes à extraire
    :return: la ligne selectionnée
    """
    logging.debug("bilseq = " + str(bilseq))
    colsToSelect = ','.join(map(lambda (x,y) : x+y, zip(['b.']*len(cols), cols)))
    req_bil = "select " \
            + colsToSelect \
            + " from  bileprod." + tabname + " b" \
            + " where b.bilseq = :bilseq"
    try:
        curs.execute(req_bil, {'bilseq':bilseq,})
        row = curs.fetchone()
        return row
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,tabname+","+str(bilseq))
        mngtError(le)


def getBilanFromBilseq(curs, bilseq):
    logging.debug("bilseq = " + str(bilseq))
    req_bil = 'select entrcs, bilseq from bileprod.bilan where bilseq = :bilseq'
    try:
        curs.execute(req_bil, (bilseq,))
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,bilseq)
        mngtError(le)
        raise

    for row in curs:
        entrcs, bilseq = row
        logging.info('bilan : ' + str(row))
        logging.info('entrcs = ' + strOrNone(entrcs))
    try:
        entrcs
    except:
        logging.info('Aucun entrcs pour bilseq = ' + str(bilseq))


def getSysdate(curs):
    try:
        curs.execute('select sysdate from dual')
        the_sysdate, = curs.fetchone()
        return the_sysdate
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,"sysdate")
        mngtError(le)


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


def getBilans(curs, tabname, cols, entnum, annee=None, origine=None, typbil=None):
    """
    Selectionne les lignes d'une table de la famille bilan à partir du siren / entnum (en pratique table BILAN)

    :param curs: curseur ouvert sur le schéma auquel appartient la table
    :param tabname: la table à requêter
    :param cols: les colonnes attendues en sortie
    :param entnum: le siren qui sert de clé
    :param annee: annee de cloture du bilan
    :param origine: origine du bilan
    :param typbil: type de bilan
    :return: les lignes de la table seléctionnées
    """
    colsToSelect = ','.join(map(lambda (x,y) : x+y, zip(['b.']*len(cols), cols)))
    req_clause_annee    = ''
    req_clause_origine  = ''
    req_clause_typbil   = ''
    bind_vars = {'entnum':entnum}
    if entnum is None:
        raise ValueError('entnum non renseigné')
    if annee is not None:
        req_clause_annee  = " and to_char(b.bildatclo,'YYYY') = :annee"
        bind_vars.update({'annee':annee})
    if origine is not None:
        req_clause_origine  = " and b.oribilcod = :origine"
        bind_vars.update({'origine':origine})
    if typbil is not None:
        req_clause_typbil  = " and b.typbilcod = :typbil"
        bind_vars.update({'typbil':typbil})
    req_bil = "select " \
            + colsToSelect \
            + " from  bileprod." + tabname + " b" \
            + " where b.entrcs = :entnum" \
            + req_clause_annee \
            + req_clause_origine \
            + req_clause_typbil
    rows = None
    try:
        curs.execute(req_bil, bind_vars)
        rows = curs.fetchall()
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,"entnum:"+entnum)
        mngtError(le)
    return rows


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


def insert_many_into(curs, rows, tabname, cols):
    """
    Insertion de plusieurs lignes dans une table de la famille bilan
    Insertion des données en bloc

    :param curs: curseur ouvert sur le schéma auquel appartient la table
    :param rows: tuples qui contiennent les valeurs des lignes à insérer
    :param tabname: le nom de la table
    :param cols: le nom des colonnes à insérer, leur nombre et leur ordre doit correspondre à ce qui est dans row
    :return: rien
    """
    curs.bindarraysize = len(rows)
    colsToInsert = ','.join(cols)
    ph = ','.join([':'+str(elem) for elem in range(1,len(cols)+1)])
    ins_bil = "insert into " + tabname + " (" + colsToInsert + ") values (" + ph +")"
    try:
        curs.executemany(ins_bil, rows)
        for row in rows:
            logging.info(tabname+' insert OK : '+str(row[:4])+'...')   # TODO à améliorer
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,tabname+" insert: "+tabname)
        mngtError(le)
        # en cas d'échec par bloc, on essaie ligne par ligne
        for row in rows:
            insert_into (curs=curs, row=row, tabname=tabname, cols=cols)


# copie d'un bilan d'une base à l'autre
def copyBilan (entnum, annee, origine, typbil, base_from, base_to):
    """
    Fonction qui copie les bilans disponibles dans une base Oracle vers une autre.
    Le schéma bileprod doit exister dans les deux bases et la base de destination doit être accessible en écriture.

    :param entnum: [obligatoire] le siren pour les bilans à copier
    :param annee: [facultatif] année des bilans à copier
    :param origine: [facultatif] origine des bilans à copier
    :param typbil:  [facultatif] type des bilans à copier
    :param base_from: [obligatoire] object base de données d'origine
    :param base_to:  [obligatoire] object base de données de destination
    :return: rien
    """
    conn_from = cx_Oracle.connect(connstr[base_from])
    curs_from = conn_from.cursor()
    conn_to = cx_Oracle.connect(connstr[base_to])
    curs_to = conn_to.cursor()
    columns = {}
    tabnames = {'BILAN':('BILSC_ACTIF'
                         ,'BILSC_PASSIF'
                         ,'BILSC_CR'
                         ,'BILSC_AFF'
                         ,'GMSIG'
                         ,'RATIOS'
                         ,'ANAFIN_INTRAPROD'
                         ,'MOTIFS_NONSAISI'
                         ,'ANADEC'
                         ,'HISTOIRE_DU_BILAN')
                }
    with conn_from, conn_to:
        logging.info('sysdate bdd from: '+str(getSysdate(curs_from)))
        logging.info('sysdate bdd to: '  +str(getSysdate(curs_to  )))
        # pour toutes les tables de niveau 1
        # c'est à dire dont le nom est une clé du dict des tables
        for tabname_1 in tabnames.iterkeys():
            nb = getTabColumnsCount(curs_to, tabname_1)
            logging.info('Table ' + tabname_1 + ' : ' + str(nb) + ' colonnes')
            columns[tabname_1] = getTabColumns(curs_to, tabname_1)
            logging.debug(','.join(columns[tabname_1]))
            bilan_count_from = getBilanCount (curs=curs_from, entnum=entnum, annee=annee, typbil=typbil)
            logging.info ("entnum="+entnum+", annee="+strOrNone(annee)+", typbil="+strOrNone(typbil)+", bilan_count_from = " + str(bilan_count_from))
            rows = getBilans (curs=curs_from, entnum=entnum, annee=annee, origine=origine, typbil=typbil, tabname=tabname_1, cols=columns[tabname_1])
            logging.info("Extraction : %d rows" % len(rows))
            insert_many_into (curs=curs_to, rows=rows, tabname=tabname_1, cols=columns[tabname_1])
            for row_1 in rows:
                bilseq = row_1[columns[tabname_1].index('BILSEQ')]
                # pour toutes les tables de niveau 2
                # c'est à dire dont le nom est une valeur du tuple du dict des tables
                for tabname_2 in tabnames[tabname_1]:
                    nb = getTabColumnsCount(curs_to, tabname_2)
                    logging.info('Table ' + tabname_2 + ' : ' + str(nb) + ' colonnes')
                    columns[tabname_2] = getTabColumns(curs_to, tabname_2)
                    logging.debug(','.join(columns[tabname_2]))
                    row_2 = getBilanOtherTablesFromBilseq (curs=curs_from, bilseq=bilseq, tabname=tabname_2, cols=columns[tabname_2])
                    if row_2 is not None:
                        logging.info("Extraction : %d fields" % len(row_2))
                        insert_into (curs=curs_to, row=row_2, tabname=tabname_2, cols=columns[tabname_2])
                    else:
                        logging.warning("Extraction : aucune ligne dans %s pour bilseq = %s", tabname_2, str(bilseq))
        try:
            curs_from.close()
            curs_to.close()
        except cx_Oracle.DatabaseError as e:
            le = LocalError(e,str(entnum)+","+str(annee)+","+str(origine)+","+str(typbil))
            mngtError(le)


def delete_row(curs, row, tabname, keycols):
    """
    Suppression d'une ligne
    :param curs: curseur ouvert sur le schéma auquel appartient la table
    :param row: les valeurs de la clé
    :param tabname: le nom de la table
    :param keycols: le nom des colonnes de la clé
    :return: rien
    """
    ph = ' and '.join([col +'=:' + col for col in keycols])
    del_bil = "delete from " + tabname + " where " + ph
    try:
        curs.execute(del_bil, row)
        # logging.info(tabname+' delete OK : '+str(row[:4])+'...')   # TODO à améliorer
        logging.info(tabname+' delete OK : '+str(zip(keycols,row[:4]))+'...')   # TODO à améliorer
    except cx_Oracle.DatabaseError as e:
        le = LocalError(e,tabname+","+str(row))
        mngtError(le)


def delete_many_rows (curs, rows, tabname, keycols):
    """
    Suppression de plusieurs lignes
    :param curs: curseur ouvert sur le schéma auquel appartient la table
    :param rows: les valeurs de la clé des différentes lignes
    :param tabname: le nom de la table
    :param keycols: le nom des colonnes de la clé
    :return: rien
    """
    for row in rows:
        delete_row(curs, row, tabname, keycols)


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
    tabnames = {'BILAN':('BILSC_ACTIF'
                         ,'BILSC_PASSIF'
                         ,'BILSC_CR'
                         ,'BILSC_AFF'
                         ,'GMSIG'
                         ,'RATIOS'
                         ,'ANAFIN_INTRAPROD'
                         ,'MOTIFS_NONSAISI'
                         ,'ANADEC'
                         ,'HISTOIRE_DU_BILAN')
                }
    tabkeys = {   'BILAN'               :[('BILSEQ')]
                , 'BILSC_ACTIF'         :[('BILSEQ')]
                , 'BILSC_PASSIF'        :[('BILSEQ')]
                , 'BILSC_CR'            :[('BILSEQ')]
                , 'BILSC_AFF'           :[('BILSEQ')]
                , 'GMSIG'               :[('BILSEQ')]
                , 'RATIOS'              :[('BILSEQ')]
                , 'ANAFIN_INTRAPROD'    :[('BILSEQ')]
                , 'MOTIFS_NONSAISI'     :[('BILSEQ')]
                , 'ANADEC'              :[('ADC_BILSEQ')]
                , 'HISTOIRE_DU_BILAN'   :[('BILSEQ')]
               }
    with conn_to:
        logging.info('sysdate bdd to: '  +str(getSysdate(curs_to)))
        # pour toutes les tables de niveau 1
        # c'est à dire dont le nom est une clé du dict des tables
        for tabname_1 in tabnames.iterkeys():
            bilan_count_from = getBilanCount (curs=curs_to, entnum=entnum, annee=annee, typbil=typbil)
            logging.info ("entnum="+entnum+", annee="+strOrNone(annee)+", typbil="+strOrNone(typbil)+", bilan_count_from = "+str(bilan_count_from))
            rows = getBilans (curs=curs_to, entnum=entnum, annee=annee, origine=origine, typbil=typbil, tabname=tabname_1, cols=tabkeys[tabname_1])
            logging.info("Extraction : %d rows" % len(rows))
            for row_1 in rows:
                bilseq = row_1[tabkeys[tabname_1].index('BILSEQ')]
                # bilseq = row_1[0]  # TODO à rendre générique en fonction du nb de colonnes dans la clé
                # pour toutes les tables de niveau 2
                # c'est à dire dont le nom est une valeur du tuple du dict des tables
                for tabname_2 in tabnames[tabname_1]:
                    row_2 = getBilanOtherTablesFromBilseq (curs=curs_to, bilseq=bilseq, tabname=tabname_2, cols=tabkeys[tabname_2])
                    if row_2 is not None:
                        logging.info("tabname="+tabname_2+", bilseq="+str(bilseq)+", Extraction : " + str(row_2))
                        delete_row (curs=curs_to, row=row_2, tabname=tabname_2, keycols=tabkeys[tabname_2])
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
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logging.info ('====================')
    logging.info ('BEGIN: ' + str(datetime.datetime.today()))
    logging.info ('plateforme = ' + sys.version)
    logging.info ('sys.path   = ')
    for p in sys.path:
     logging.info ('    '+p)
    logging.info ('====================')
    base_from   = 'clone', 'bileprod'
    # base_to     = 'DEV', 'bileprod'
    base_to     = 'IA', 'bileprod'
    # base_to     = 'UA', 'bileprod'

    # copyBilan (entnum='482755741', annee='2014', origine='IN', typbil='SC', base_from=base_from, base_to=base_to)
    # copyBilan (entnum='015950033', annee='2014', origine=None, typbil=None, base_from=base_from, base_to=base_to)
    # copyBilan (entnum='015950033', annee=None, origine=None, typbil=None, base_from=base_from, base_to=base_to)
    # copyBilan (entnum='301160750', annee=None, origine=None, typbil=None, base_from=base_from, base_to=base_to)
    # copyBilan (entnum='482755741', annee=None, origine=None, typbil=None, base_from=base_from, base_to=base_to)
    # copyBilan (entnum='005450119', annee=None, origine=None, typbil=None, base_from=base_from, base_to=base_to)
    # copyBilan (entnum='393956511', annee=None, origine=None, typbil=None, base_from=base_from, base_to=base_to)
    # copyBilan (entnum='005750385', annee=None, origine=None, typbil=None, base_from=base_from, base_to=base_to)
    # copyBilan (entnum='007080757', annee=None, origine=None, typbil=None, base_from=base_from, base_to=base_to)
    # deleteBilan (entnum='007080757', annee=None, origine=None, typbil=None, base_to=base_to)

    # deleteBilan (entnum='007280605', annee=None, origine=None, typbil=None, base_to=base_to)
    # copyBilan (entnum='007280605', annee=None, origine=None, typbil=None, base_from=base_from, base_to=base_to)

    deleteBilan(entnum='334300100', annee=None, origine=None, typbil=None, base_to=base_to)
    copyBilan(entnum='334300100', annee=None, origine=None, typbil=None, base_from=base_from, base_to=base_to)

    logging.info('====================')
    logging.info('END: ' + str(datetime.datetime.today()))
    logging.info('====================')
