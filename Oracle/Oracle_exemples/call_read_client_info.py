# coding=utf-8

from __future__ import print_function, unicode_literals
import cx_Oracle

###########################################################################
#
if __name__ == '__main__':
    con = cx_Oracle.connect('fra2prod/fra2prod@devdbirisfr.int.dns:1521/svcproddev2.world')

    cur = con.cursor()
    client_info = cur.var(cx_Oracle.STRING)

    cur.callproc('dbms_application_info.set_client_info',
                 keywordParameters=dict(client_info="appareillage=yes;surveillance=no",))

    cur.callproc('pkg_client_info.call_read_client_info',
                 keywordParameters=dict(client_info=client_info, ))

    # cur.callproc('dbms_application_info.read_client_info',
    #              keywordParameters=dict(client_info=client_info, ))

    print('client_info: {}'.format(client_info.getvalue()))

    cur.close()
    con.close()
