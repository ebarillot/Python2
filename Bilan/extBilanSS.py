#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# programme d'extraction des bilans SS
#

import cx_Oracle
import platform
import sys
import csv

connstr = dict()
connstr['IA'] = dict()
connstr['UA'] = dict()
connstr['clone'] = dict()

connstr['IA']['bileprod'] = 'bileprod/bileprodia@intdbirisfr.int.dns:1521/svcprodint1.world'
connstr['UA']['bileprod'] = 'etudes_consult/etudes_consultpre@irisfrpx.int.dns:1523/SVCPRODPRE1.world'
connstr['clone']['bileprod'] = 'etudes_consult/IF5489rG@dbirisclone.int.dns:1521/svcprodclo1.world'

csv.register_dialect('csvdefault', delimiter=';', quoting=csv.QUOTE_NONE, lineterminator='\n')


def getBilanCount(conn, annee):
    curs = conn.cursor()
    curs.execute("SELECT count(*) FROM bileprod.bilan WHERE typbilcod = :v1 and to_char(bildatclo,'YYYY') = :v2",
                 ('SS', annee))
    for row in curs:
        print(row)


# bilan : recherche avec bilseq
def getBilanFromBilseq(conn, bilseq):
    curs = conn.cursor()
    print "bilseq    = " + str(bilseq)
    req_bilss = 'select entrcs, bilseq from bileprod.bilan where bilseq = :bilseq'
    curs.execute(req_bilss, (bilseq,))
    for row in curs:
        entrcs, bilseq = row
        print('ss : ' + str(row))
        print('entrcs = ' + entrcs)
    try:
        entrcs
    except:
        print('Aucun entrcs pour bilseq = ' + str(bilseq))
        sys.exit(0)


def getSysdate(conn):
    curs = conn.cursor()
    curs.execute('select sysdate from dual')
    for row in curs:
        print(row)

def floatOrNoneToStr(a_float, a_format):
    return ("" if a_float is None else format(a_float,a_format))

# bilan : recherche des SS d'une année donnée
def getBilansSS(conn, annee, csv_writer, fieldnames, chunk):
    curs = conn.cursor()
    req_bilss = "select b.entrcs, b.bilseq, ss.ss156, ss.ss195 from bileprod.bilan b, bileprod.bilss ss" \
        + " where b.typbilcod = 'SS'" \
        + " and   to_char(b.bildatclo,'YYYY') = :annee" \
        + " and   b.bilseq = ss.bilseq"
        # + " and   rownum <= 100"
    curs.execute(req_bilss, (annee,))
    nb = 0
    for row in curs:
        nb += 1
        entrcs, bilseq, ss156, ss195 = row
        ss156_str = floatOrNoneToStr(ss156, ".0f")  # transformation des float en chaines sans décimales
        ss195_str = floatOrNoneToStr(ss195, ".0f")
        csv_writer.writerow({fieldnames[0]:entrcs, fieldnames[1]:bilseq, fieldnames[2]:ss156_str, fieldnames[3]:ss195_str})
        if nb % chunk == 0:
            print(str(nb)+" bilans lus")
    return nb


def main(annee=2013, outputFileName='output.txt', chunk=1000, envbdd='IA'):
    conn = cx_Oracle.connect(connstr[envbdd]['bileprod'])
    print("\nNouveau fichier: " + outputFileName)
    with conn:
        # getSysdate(conn)
        # getBilanCount(conn, annee)

        # bilseq = 19028573
        # getBilanFromBilseq(conn,bilseq)

        with open(outputFileName, "w") as outputFile:
            fieldnames = ['id_siren', 'bi_seq', '156', '195']
            csv_writer = csv.DictWriter(outputFile, fieldnames=fieldnames, dialect='csvdefault')
            csv_writer.writeheader()
            nbextract = getBilansSS(conn, annee, csv_writer, fieldnames, chunk)
    print ("nbextract = "+str(nbextract))

#####################
# programme principal
#####################
if __name__ == "__main__":
    pltf = platform.python_version()
    print ('====================')
    print ('plateforme = ' + pltf)
    print ('====================')
    envbdd = 'clone'
    # envbdd = 'IA'
    chunk  = 10000
    main('2013', 'extBilanSS_2013_'+envbdd+'.csv', chunk, envbdd)
    main('2014', 'extBilanSS_2014_'+envbdd+'.csv', chunk, envbdd)
