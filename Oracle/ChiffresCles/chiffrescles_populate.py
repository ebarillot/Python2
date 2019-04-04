# coding=utf-8

from __future__ import print_function, unicode_literals

import cx_Oracle

print(cx_Oracle.version)
print(cx_Oracle.clientversion())

con = cx_Oracle.connect('ort2prod/ort2prod@devdbirisfr.int.dns:1521/svcdiffdev2.world')
cur = con.cursor()

cur.execute('select * from chiffrescles order by cclentnum_pk')
rows = cur.fetchmany(10)
# res = cur.fetchall()

for row in rows:
    print(row)

cur.close()
con.close()
