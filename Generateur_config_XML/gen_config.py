# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 10:56:22 2016

@author: emmanuel_barillot
"""

liste_tables = [
"BILE_BILAN",
"BILE_BILSC_ACTIF",
"BILE_BILSC_AFF",
"BILE_BILSC_AMO",
"BILE_BILSC_CR",
"BILE_BILSC_ECH",
"BILE_BILSC_IMM",
"BILE_BILSC_PASSIF",
"BILE_BILSC_PRO",
"BILE_BILSS",
"BILE_BILSS_CR",
"BILE_GMSIG",
"BILE_RATIOS",
"FRA2_BOUHISM",
"FRA2_CAPHISM",
"FRA2_CCLES_HISM",
"FRA2_CJUHISM",
"FRA2_DENHISM",
"FRA2_DIRHISM",
"FRA2_EFFHISM",
"FRA2_ENAHISM",
"FRA2_ENTHISM",
"FRA2_ETAHISM",
"FRA2_EVLX_HISM",
"FRA2_IFNHISMS",
"FRA2_PERHISM",
"FRA2_PRIHISM",
"FRA2_PRLHISM",
"FRA2_ROLHISM"
]


# génération des objets
for t in liste_tables:
    print ('    <file action="create" object="table_%s">' % t)
    print ('      <input_file>cre_tab_CDC_%s.sql</input_file>' % t)
    print ('    </file>')
    print ('    <file action="alter" object="table_%s">' % t)
    print ('      <input_file>alt_tab_CDC_%s.sql</input_file>' % t)
    print ('    </file>')
    print ('    <file action="create" object="index_%s">' % t)
    print ('      <input_file>cre_idx_CDC_%s.sql</input_file>' % t)
    print ('    </file>')
    print ('    <file action="create" object="trigger_%s">' % t)
    print ('      <input_file>cre_trg_CDC_%s.sql</input_file>' % t)
    print ('    </file>')
    print ('')



# génération des drops des tables et des triggers
for t in liste_tables:
    print ('    <file action="drop" object="table_%s" backup="true">' % t)
    print ('      <input_file>drop_tab_CDC_%s.sql</input_file>' % t)
    print ('    </file>')
    print ('    <file action="drop" object="trg_%s" backup="true">' % t)
    print ('      <input_file>drop_trg_CDC_%s.sql</input_file>' % t)
    print ('    </file>')
    print ('')


liste_grants = [
"CDCPROD_BILE",
"CDCPROD_FRA2"
]

for g in liste_grants:
    print ('    <file action="grant" object="%s">' % g)
    print ('      <input_file>grant_%s.sql</input_file>' % g)
    print ('    </file>')
    print ('')
