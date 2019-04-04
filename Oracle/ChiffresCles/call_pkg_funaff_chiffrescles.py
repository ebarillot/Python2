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
# cur.var(cx_Oracle.STRING, 500, 100)

res = cur.callfunc('pkg_funaff_chiffrescles.fun_aff_chiffrescles',
                   cx_Oracle.NUMBER,
                   (
                       pMESSAGE,
                       0,
                       '313464455',
                       'FR',
                       'DD/MM/YYYY',
                       'O',
                       '300',
                       '0',
                       pNBRLIGOUT,
                       pTAB,
                       'N',
                       'N'
                   ))

# pMESSAGE    OUT VARCHAR2,
# pENTNUMTYP  IN NUMBER DEFAULT 0,
# pENTNUM     IN VARCHAR2,
# pLANCOD     IN VARCHAR2 DEFAULT 'FR',
# pFORDATES   IN VARCHAR2 DEFAULT 'DD/MM/YYYY',
# pLIBELLE    IN VARCHAR2 DEFAULT 'O',
# pDEVISEIN   IN VARCHAR2 DEFAULT '300',
# pUNITEIN    IN VARCHAR2 DEFAULT '0',
# pNBRLIGOUT  OUT NUMBER,
# pTAB        OUT TableauCHAINE,
# pACCES_CONF  IN VARCHAR2 DEFAULT 'N',
# pACCES_EVAL  IN VARCHAR2 DEFAULT 'N'

print('res: {}'.format(res))
print('pNBRLIGOUT: {}'.format(pNBRLIGOUT.getvalue()))

print(pTAB.type)
print(pTAB.size())
print(pTAB.aslist())
# for i in range(1, int(pNBRLIGOUT.getvalue()) + 1):
#     print(pTAB.getelement(i))


cur.close()
con.close()
