# coding=UTF-8

from __future__ import print_function, unicode_literals

import cx_Oracle


L_dbms_output_buffer = 1000000


class Oracle(object):

    def __init__(self, username, password, hostname, port, servicename):
        # type: (unicode, unicode, unicode, unicode, unicode) -> None
        try:
            self.db = cx_Oracle.connect(username, password, hostname + ':' + port + '/' + servicename)
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 1017:
                print('Please check your credentials.')
            else:
                print('Database connection error: %s'.format(e))
            # Very important part!
            raise
        # If the database connection succeeded create the cursor
        # we-re going to use.
        self.cursor = self.db.cursor()

    @staticmethod
    def connect(username, password, hostname, port, servicename):
        # type: (unicode, unicode, unicode, unicode, unicode) -> Oracle
        """ Connect to the database. """
        return Oracle(username, password, hostname, port, servicename)

    def disconnect(self):
        """
        Disconnect from the database. If this fails, for instance
        if the connection instance doesn't exist we don't really care.
        """
        try:
            self.cursor.close()
            self.db.close()
        except cx_Oracle.DatabaseError:
            pass

    def execute(self, sql, bindvars=None, commit=False):
        """
        Execute whatever SQL statements are passed to the method;
        commit if specified. Do not specify fetchall() in here as
        the SQL statement may not be a select.
        bindvars is a dictionary of variables you pass to execute.
        """
        try:
            reqres = None
            if not bindvars:
                reqres = self.cursor.execute(sql)
            else:
                reqres = self.cursor.execute(sql, bindvars)
            # Only commit if it-s necessary.
            if commit:
                self.db.commit()
            return reqres
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 955:
                print('Table already exists')
            elif error.code == 1031:
                print("Insufficient privileges")
            print(error.code)
            print(error.message)
            print(error.context)
            self.db.rollback()
            # Raise the exception.
            raise

    def callfunc(self, fun_name, params, dbms_output_bool=False):
        # type: (unicode, dict, bool) -> unicode
        if dbms_output_bool:
            self.dbms_output_enable()
        res = self.cursor.callfunc(fun_name, cx_Oracle.STRING, keywordParameters=params)
        if dbms_output_bool:
            output_buffer, n_lines = self.get_dbms_output()
            self.dbms_output_disable()
            print("dbms_output_buffer [{}}:".format(n_lines))
            # print(output_buffer.decode('UTF-8'))
            # print(output_buffer.decode('iso-8859-15'))
            print(output_buffer)
            print("-- dbms_output_buffer")
        return res

    def dbms_output_enable(self):
        """
        Permet l'enregistrement des messages PL/SQL produits par dbms_output
        """
        print("dbms_output_enable")
        self.cursor.callproc('dbms_output.enable', (L_dbms_output_buffer,))

    def dbms_output_disable(self):
        """
        Arrete l'enregistrement des messages PL/SQL produits par dbms_output
        """
        print("dbms_output_disable")
        self.cursor.callproc('dbms_output.disable')

    def get_dbms_output(self):
        """
         Récupère les messages PL/SQL produits par dbms_output
         Nécessite d'abord l'appel à dbms_output_enable()

        :return: le buffer des messages PL/SQL formé de lignes concaténées
        """
        # Requête pour recuperer les messages produits en PL/SQL par dbms_output
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
        loc_dbms_output_buffer = self.cursor.var(cx_Oracle.STRING)
        loc_n_lines = self.cursor.var(cx_Oracle.NUMBER)
        self.cursor.execute(statement,
                            L_dbms_output_buffer=L_dbms_output_buffer,
                            loc_dbms_output_buffer=loc_dbms_output_buffer,
                            loc_n_lines=loc_n_lines)
        return loc_dbms_output_buffer.getvalue().rstrip(), loc_n_lines.getvalue()


if __name__ == "__main__":

    username, password, hostname, port, servicename = \
        'bileprod', 'bileprod', 'devdbirisfr.int.dns', '1521', 'svcproddev2.world'
    oracle = None
    try:
        oracle = Oracle.connect(username, password, hostname, port, servicename)
        # No commit as you don-t need to commit DDL.
        # ddl_statements = 'create table mytab (id number, data varchar2(20))'
        # oracle.execute('')

        # No commit as you don-t need to commit select.
        select_statement = 'select sysdate from dual'
        oracle.execute(select_statement)
        for row in oracle.cursor:
            print(row)
    except Exception as e:
        print('Connextion error: {}'.format(e))
        exit(-1)
    finally:
        oracle.disconnect()
