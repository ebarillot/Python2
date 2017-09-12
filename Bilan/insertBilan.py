#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Emmanuel Barillot'

import cx_Oracle

con = cx_Oracle.connect('bileprod/bileprod@devdbirisfr.int.dns:1521/svcproddev2.world')


cursddl = con.cursor()
try:
    cursddl.execute("drop table mytab")
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print('Database error: {}'.format(e))

try:
    cursddl.execute("create table mytab (id number, data varchar2(20))")
    cursddl.execute("comment on column mytab.id is 'identifiant'")
    cursddl.execute("comment on column mytab.data is 'data'")
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print('Database error: {}'.format(e))
    raise

cursddl.close()

rows = [ (1, "First" ),
         (2, "Second" ),
         (3, "Third" ),
         (4, "Fourth" ),
         (5, "Fifth" ),
         (6, "Sixth" ),
         (7, "Seventh" ) ]

cur = con.cursor()
cur.bindarraysize = 7
cur.setinputsizes(int, 20)
cur.executemany("insert into mytab(id, data) values (:1, :2)", rows)

# This is uncommented in the next step
#con.commit()

# Now query the results back

cur2 = con.cursor()
cur2.execute('select * from mytab')
res = cur2.fetchall()
print res

cur.close()
cur2.close()
con.close()
