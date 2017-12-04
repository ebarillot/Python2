# coding=utf-8

import cx_Oracle

connstr='etudes_consult/IF5489rG@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=dbirisclone.int.dns)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=svcprodclo1.world)))'
conn = cx_Oracle.connect(connstr)
curs = conn.cursor()
curs.execute('select count(*) from fra2prod.idcellixium_param')
for row in curs:
    print row
conn.close()
