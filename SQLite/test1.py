#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

try:
    con = lite.connect(r'D:\Documents\Projets\Developpements\SQLite\Modeles\dbbilans2014_secteur157.sqlite')
    with con:
        cur = con.cursor()
        # version
        cur.execute('SELECT SQLITE_VERSION()')
        data = cur.fetchone()
        print "SQLite version: %s" % data

        # liste des tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        rows = cur.fetchall()
        for row in rows:
            print row[0]

        cur.execute("SELECT * FROM dbbilans2014_secteur157")
        rows = cur.fetchall()

except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
