# coding=utf-8

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
    con = cx_Oracle.connect('bileprod/bileprod@devdbirisfr.int.dns:1521/svcproddev2.world')

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
    print('res: {}'.format(res))
    print('message: {}'.format(pMESSAGE.getvalue()))
    print('pNBRLIGOUT: {}'.format(pNBRLIGOUT.getvalue()))

    print(pTAB.type)
    print(pTAB.size())
    print(pTAB.aslist())

    output_buffer, n_lines = get_dbms_output(cur)
    dbms_output_disable(cur)
    print("dbms_output_buffer:")
    print(n_lines)
    print(output_buffer)
    print("-- dbms_output_buffer")
    cur.close()
    con.close()
