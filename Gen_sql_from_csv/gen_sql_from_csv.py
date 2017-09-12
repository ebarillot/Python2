#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

csv.register_dialect('csvdefault', delimiter=';', quoting=csv.QUOTE_NONE, lineterminator='\n')

with open('bilseq_UA.csv', 'rb') as f:
    with open('delete_chiffrescles.sql', 'wb') as outfile:
        reader = csv.reader(f, 'csvdefault')
        for row in reader:
            # print row
            if "siren" not in row:
                del_ccl_hism_stmt = "delete from chiffrescles_hism h" \
                      " where exists" \
                      " (select * from chiffrescles c" \
                      " where cclentnum_pk = '{}'" \
                      " and cclbilseq = {}" \
                      " and c.cclentnum_pk = h.cclhisentnum_pk" \
                      " and c.cclentnumtyp_pk = h.cclhisentnumtyp_pk" \
                      " and c.cclseq_pk = h.cclhisseq_pk);".format(row[1], row[0])
                del_ccl_stmt = "delete from chiffrescles c" \
                      " where cclentnum_pk = '{}'" \
                      " and cclbilseq = {};".format(row[1], row[0])
                outfile.write(del_ccl_hism_stmt)
                outfile.write("\n")
                outfile.write(del_ccl_stmt)
                outfile.write("\n")
