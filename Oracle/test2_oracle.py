import cx_Oracle

connstr='etudes_consult/IF5489rG@dbirisclone.int.dns:1521/svcprodclo1.world'
conn = cx_Oracle.connect(connstr)
curs = conn.cursor()
curs.execute('select count(*) from fra2prod.idcellixium_param')
for row in curs:
    print row
conn.close()
  