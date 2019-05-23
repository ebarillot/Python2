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


def callfunc(cur, oribilcod, crconf):
    # dbms_output_enable(cur)
    res = cur.callfunc('pkg_funaff_chiffrescles.get_ccltype',
                       cx_Oracle.STRING,
                       keywordParameters=dict(
                           v_oribilcod=oribilcod,
                            v_crconf=crconf,
                       ))
    # output_buffer, n_lines = get_dbms_output(cur)
    # dbms_output_disable(cur)
    # print("dbms_output_buffer:")
    # print(n_lines)
    # print(output_buffer.decode('UTF-8'))
    # print(output_buffer.decode('utf8'))
    # print(output_buffer.decode('iso-8859-15'))
    # print(output_buffer)
    # print("-- dbms_output_buffer")
    print("** Valeur retournée  (oribilcod: {}, crconf: {}) => {}".format(oribilcod, crconf, res))


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
    callfunc(cur, oribilcod='CO', crconf='OUI')
    callfunc(cur, oribilcod='CO', crconf='NON')

    callfunc(cur, oribilcod='EC', crconf='OUI')
    callfunc(cur, oribilcod='EC', crconf='NON')
    callfunc(cur, oribilcod='RC', crconf='OUI')
    callfunc(cur, oribilcod='RC', crconf='NON')

    callfunc(cur, oribilcod='CS', crconf='NON')
    callfunc(cur, oribilcod='CS', crconf='OUI')
    callfunc(cur, oribilcod='BL', crconf='NON')
    callfunc(cur, oribilcod='BL', crconf='OUI')
    callfunc(cur, oribilcod='IN', crconf='NON')
    callfunc(cur, oribilcod='IN', crconf='OUI')
    callfunc(cur, oribilcod='AL', crconf='NON')
    callfunc(cur, oribilcod='AL', crconf='OUI')

    callfunc(cur, oribilcod='AP', crconf='NON')
    callfunc(cur, oribilcod='AP', crconf='OUI')
    callfunc(cur, oribilcod='CM', crconf='NON')
    callfunc(cur, oribilcod='CM', crconf='OUI')

    cur.close()
    con.close()



