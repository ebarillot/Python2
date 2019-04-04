# coding=utf-8

from __future__ import print_function, unicode_literals

import cx_Oracle

print(cx_Oracle.version)
print(cx_Oracle.clientversion())

con = cx_Oracle.connect('ort2prod/ort2prod@devdbirisfr.int.dns:1521/svcdiffdev2.world')

cur = con.cursor()
pMESSAGE = cur.var(cx_Oracle.STRING)
pNBRLIGOUT = cur.var(cx_Oracle.NUMBER)

tableTypeObj = con.gettype("PKG_FUNAFF_CHIFFRESCLES.TABLEAUCHAINE")
pTAB = tableTypeObj.newobject()

# ##########################################################################
#
res = cur.callfunc('pkg_funaff_chiffrescles.fun_aff_3bilseqCC',
                   cx_Oracle.NUMBER,
                   (
                       pMESSAGE,
                       0,
                       '313464455',
                       'DD/MM/YYYY',
                       pNBRLIGOUT,
                       pTAB,
                       'FR',
                       '300',
                       '0',
                       'O',
                       'SOC',
                       -1,
                       'N',
                       'N'
                   ))
print('res: {}'.format(res))
print('pNBRLIGOUT: {}'.format(pNBRLIGOUT.getvalue()))

print(pTAB.type)
print(pTAB.size())
print(pTAB.aslist())

#     pMESSAGE    OUT VARCHAR2,
#     pENTNUMTYP  IN NUMBER DEFAULT 0,
#     pENTNUM     IN VARCHAR2,
#     pFORDATES   IN VARCHAR2 DEFAULT 'YYYYMMDD',
#     pNBRLIGOUT  OUT NUMBER,
#     pTAB        OUT TableauChaine,
#     pLANCOD     IN VARCHAR2 DEFAULT 'FR',
#     pDEVISEIN   IN VARCHAR2 DEFAULT '300',
#     pUNITEIN    IN VARCHAR2 DEFAULT '0',
#     pLIBELLE    IN VARCHAR2 DEFAULT 'O',
#     pTYPEXECOD  IN VARCHAR2 DEFAULT 'SOC',
#     pNBRANNEE   IN NUMBER   DEFAULT -1,
#     pACCES_CONF  IN VARCHAR2 DEFAULT 'N',
#     pACCES_EVAL  IN VARCHAR2 DEFAULT 'N'


cur.close()
con.close()
