# coding=utf-8

from __future__ import print_function, unicode_literals

import cx_Oracle

# print(cx_Oracle.version)
# print(cx_Oracle.clientversion())

con = cx_Oracle.connect('bileprod/bileprod@devdbirisfr.int.dns:1521/svcproddev2.world')

cur = con.cursor()
pMESSAGE = cur.var(cx_Oracle.STRING)
pNBBILOUT = cur.var(cx_Oracle.NUMBER)
pNBRLIGOUT = cur.var(cx_Oracle.NUMBER)

tableTypeObj = con.gettype("PKG_FUNAFF_CHIFFRESCLES.TABLEAUCHAINE")
pTAB = tableTypeObj.newobject()
# cur.var(cx_Oracle.STRING, 500, 100)

res = cur.callfunc('pkg_funaff_bilan2.fun_aff_listebilan',
                   cx_Oracle.NUMBER,
                   #         RETURN NUMBER
                   (
                       pMESSAGE,            #         pMESSAGE              OUT VARCHAR2,
                       0,                   #         pENTNUMTYP         IN     NUMBER,
                       '482755741',         #         pENTNUM            IN     VARCHAR2,
                       '',                  #         pCLIPRE            IN     VARCHAR2 DEFAULT '',
                       '',                  #         pCLIREF            IN     VARCHAR2 DEFAULT '',
                       '',                  #         pREDACTCOD         IN     VARCHAR2 DEFAULT '',
                       '',                  #         pSERVICECOD        IN     VARCHAR2 DEFAULT '',
                       'SCSS',              #         pTYPBILCOD         IN     VARCHAR2 DEFAULT 'SCSS',
                       'INBL',              #         pORIBILCOD         IN     VARCHAR2 DEFAULT 'INBL',
                       '10',                #         pETACOD            IN     VARCHAR2 DEFAULT '10',
                       '89',                #         pVALCOD            IN     VARCHAR2 DEFAULT '89',
                       -1,                   #         pNBRANNEE          IN     NUMBER DEFAULT -1,
                       '0',                 #         pLISTEANNEEBILAN   IN     VARCHAR2 DEFAULT '0',
                       'O',                 #         pTROU              IN     VARCHAR2 DEFAULT 'O',
                       1,                   #         pNBRBILAN          IN     NUMBER DEFAULT 1,
                       pNBBILOUT,           #         pNBBILOUT             OUT NUMBER,
                       pNBRLIGOUT,          #         pNBRLIGOUT            OUT NUMBER,
                       pTAB,                #         pTAB                  OUT TableauCHAINE,
                       0,                   #         pORDRE_BILAN       IN     NUMBER DEFAULT 0,
                       'N'                  #         pACCES_CONF        IN     VARCHAR2 DEFAULT 'N')
                   ))

print('res: {}'.format(res))
print('pNBRLIGOUT: {}'.format(pNBRLIGOUT.getvalue()))

print(pTAB.type)
print(pTAB.size())
print(pTAB.aslist())
# for i in range(1, int(pNBRLIGOUT.getvalue()) + 1):
#     print(pTAB.getelement(i))

cur.close()
con.close()
