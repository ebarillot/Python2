# coding=UTF-8

from __future__ import print_function, unicode_literals

import cx_Oracle

# print(cx_Oracle.version)
# print(cx_Oracle.clientversion())

L_dbms_output_buffer = 1000000


# ##########################################################################
#
#  permet l'enregistrement des messages PL/SQL produits par dbms_output
#
# ##########################################################################
def dbms_output_enable(cur):
    print("dbms_output_enable")
    cur.callproc('dbms_output.enable', (L_dbms_output_buffer,))


# ***********************************************************************
# arrete l'enregistrement des messages PL/SQL produits par dbms_output
# ***********************************************************************
def dbms_output_disable(cur):
    print("dbms_output_disable")
    cur.callproc('dbms_output.disable')


# **********************************************************************
#  récupère les messages PL/SQL produits par dbms_output
#  Nécessite d'abord l'appel à dbms_output_enable()
# **********************************************************************
def get_dbms_output(cur):
    # pour recuperer les messages produits en PL/SQL par dbms_output
    # loc_dbms_output_buffer = ' ' * L_dbms_output_buffer
    # recuperation des messages dbms_output
    statement = """
        DECLARE
          l_line    varchar2(255) := '';
          l_done    number;
          l_buffer  long := '';
          n_lines   number := 0;
        BEGIN
          loop
            exit when length(l_buffer)+255 > :L_dbms_output_buffer OR l_done = 1;
            dbms_output.get_line(l_line, l_done);
            l_buffer := l_buffer || rtrim(l_line) || chr(10);
            n_lines := n_lines+1;
          end loop;
          :loc_dbms_output_buffer := l_buffer;
          :loc_n_lines := n_lines;
        END;
    """
    loc_dbms_output_buffer = cur.var(cx_Oracle.STRING)
    loc_n_lines = cur.var(cx_Oracle.NUMBER)
    cur.execute(statement,
                L_dbms_output_buffer=L_dbms_output_buffer,
                loc_dbms_output_buffer=loc_dbms_output_buffer,
                loc_n_lines=loc_n_lines)
    return loc_dbms_output_buffer.getvalue().rstrip(), loc_n_lines.getvalue()


###########################################################################
#
if __name__ == '__main__':
    con = cx_Oracle.connect('bileprod/bileprod@devdbirisfr.int.dns:1521/svcproddev2.world',
                            encoding='UTF-8',
                            nencoding='UTF-8')
    # encoding='iso-8859-15',
    # nencoding='iso-8859-15')
    print('Connection encoding: {}'.format(con.encoding))
    print('national character set: {}'.format(con.nencoding))

    cursor = con.cursor()
    cursor.execute("""select 'DB: ' || value as db_charset from nls_database_parameters where parameter = 'NLS_CHARACTERSET'
    union
    select distinct 'Client: ' || client_charset from v$session_connect_info where sid = sys_context('USERENV', 'SID')""")
    v = cursor.fetchall()
    print(v)
    cursor.close()

    cur = con.cursor()
    pMESSAGE = cur.var(cx_Oracle.STRING)
    pNBRLIGOUT = cur.var(cx_Oracle.NUMBER)
    tableTypeObj = con.gettype("PKG_FUNAFF_CHIFFRESCLES.TABLEAUCHAINE")
    pTAB = tableTypeObj.newobject()

    dbms_output_enable(cur)
    res = cur.callfunc('pkg_funaff_chiffrescles.fun_aff_3bilseqCC',
                       cx_Oracle.NUMBER,
                       keywordParameters=dict(
                           pMESSAGE=pMESSAGE,
                           pENTNUMTYP=0,
                           pENTNUM='482755741',
                           pFORDATES='DD/MM/YYYY',
                           pNBRLIGOUT=pNBRLIGOUT,
                           pTAB=pTAB,
                           pLANCOD='FR',
                           pDEVISEIN='300',
                           pUNITEIN='0',
                           pLIBELLE='O',
                           pTYPEXECOD='SOC',
                           pNBRANNEE=-1,
                           pACCES_CONF='N',
                           pACCES_EVAL='N',
                           pCLIPRE='',
                           pCLIREF='',
                       ))
    output_buffer, n_lines = get_dbms_output(cur)
    dbms_output_disable(cur)
    print("dbms_output_buffer:")
    print(n_lines)
    # print(output_buffer.decode('utf8'))
    print(output_buffer.decode('UTF-8'))
    # print(output_buffer.decode('iso-8859-15'))
    # print(output_buffer.decode('cp1252'))
    # print(output_buffer)
    print("-- dbms_output_buffer")
    cur.close()
    con.close()

    print('res: {}'.format(res))
    print('message: {}'.format(pMESSAGE.getvalue()))
    print('pNBRLIGOUT: {}'.format(pNBRLIGOUT.getvalue()))

    print(pTAB.type)
    print(pTAB.size())
    print(pTAB.aslist())

    print("** Tableau retourné:")
    pTabLib = [
        "** 1  montant dernier CA",
        "**    date dernier CA",
        "**    montant dernier resultat net",
        "**    date dernier resultat net",
        "** 5  duree du dernier exercice",
        "**    montant avant dernier CA",
        "**    date avant dernier CA",
        "**    montant avant dernier resultat net",
        "**    date avant dernier resultat net",
        "** 10 duree avant dernier exercice",
        "**    montant antepenultieme CA",
        "**    date antepenultieme CA",
        "**    montant antepenultieme resultat net",
        "**    date antepenultieme resultat net",
        "** 15 duree antepenultieme exercice",
        "**    % variation du dernier CA",
        "**    % variation avant dernier CA",
        "**    % variation dernier resultat net",
        "**    % variation avant dernier resultat net",
        "** 20 precision date du dernier exercice",
        "**    code devise saisie du dernier CA/resultat net",
        "**    libelle devise saisie du dernier CA/resultat net",
        "**    unite monetaire saisie du dernier CA/resultat net",
        "**    code devise demande du dernier CA/resultat net",
        "** 25 libelle devise demande du dernier CA/resultat net",
        "**    unite monetaire demande du dernier CA/resultat net",
        "**    precision date de l'avant dernier exercice",
        "**    code devise saisie avant dernier CA/resultat net",
        "**    libelle devise saisie avant dernier CA/resultat net",
        "** 30 unite monetaire saisie avant dernier CA/resultat net",
        "**    code devise demande avant dernier CA/resultat net",
        "**    libelle demande saisie avant dernier CA/resultat net",
        "**    unite monetaire demande avant dernier CA/resultat net",
        "**    precision date de l'antepenultieme exercice",
        "** 35 code devise saisie antepenultieme CA/resultat net",
        "**    libelle devise saisie antepenultieme CA/resultat net",
        "**    unite monetaire saisie antepenultieme CA/resultat net",
        "**    code devise demande antepenultieme CA/resultat net",
        "**    libelle devise demande antepenultieme CA/resultat net",
        "** 40 unite monetaire demande antepenultieme CA/resultat net",
        "**    evolution dernier chiffres cles export",
        "**    evolution avantdernier chiffres cles export",
        "**    evolution dernier resultat exploitation",
        "**    evolution avant dernier resultat exploitation",
        "** 45 evolution dernier RCAI",
        "**    evolution avant dernier RCAI",
        "**    evolution dernier fond propre",
        "**    evolution avant dernier fond propre",
        "**    evolution dernier endettement",
        "** 50 evolution avant dernier endettement",
        "**    evolution dernier CAF",
        "**    evolution avant dernier CAF",
        "**    evolution dernier montant d'achats",
        "**    evolution avant dernier montant d'achats",
        "** 55 dernier CA export",
        "**    dernier resultat exploitation",
        "**    dernier RCAI",
        "**    dernier fond propre",
        "**    dernier endettement",
        "** 60 dernier CAF",
        "**    dernier montant achats",
        "**    derniere duree clients",
        "**    derniere duree fournisseurs",
        "**    dernier effectif",
        "** 65 avant dernier CA export",
        "**    avant dernier resultat exploitation",
        "**    avant dernier RCAI",
        "**    avant dernier fond propre",
        "**    avant dernier endettement",
        "** 70 avant dernier CAF",
        "**    avant dernier montant achats",
        "**    avant derniere duree clients",
        "**    avant derniere duree fournisseurs",
        "**    avant dernier effectif",
        "** 75 antepenultieme CA export",
        "**    antepenultieme resultat exploitation",
        "**    antepenultieme RCAI",
        "**    antepenultieme fond propre",
        "**    antepenultieme endettement",
        "** 80 antepenultieme CAF",
        "**    antepenultieme montant achats",
        "**    antepenultieme duree clients",
        "**    antepenultieme duree fournisseurs",
        "**    antepenultieme effectif",
        "** 85 provenance",
        "**    provenance N-1",
        "** 87 provenance N-2",
        "** 88 type",
        "**    type N-1",
        "** 90 type N-2",
        "** 91 lib Type",
        "**    lib Type N-1",
        "** 93 lib Type N-2",
        "** 94 tranche de CA",
        "**    tranche de CA N-1",
        "** 96 tranche de CA N-2",
        "** 97 Libelle tranche de CA",
        "**    Libelle tranche de CA N-1",
        "** 99 Libelle tranche de CA N-2"
    ]
    for (lib, val) in zip(pTabLib, pTAB.aslist()):
        print('{}: {}'.format(lib, val))
