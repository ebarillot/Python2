#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Emmanuel Barillot'


# hiérarchie des tables: BILAN comme table dont dépendent toutes les autres
tabnames = \
    {
        'BILAN': (  'BILSC_ACTIF'
                  , 'BILSC_PASSIF'
                  , 'BILSC_CR'
                  , 'BILSC_AFF'
                  , 'GMSIG'
                  , 'RATIOS'
                  , 'ANAFIN_INTRAPROD'
                  , 'MOTIFS_NONSAISI'
                  , 'ANADEC'
                  , 'HISTOIRE_DU_BILAN')
    }
# la clé de chacune des tables, sous forme d'un tuple de noms de colonnes
tabkeys = \
    {
          'BILAN'               : ('BILSEQ',)
        , 'BILSC_ACTIF'         : ('BILSEQ',)
        , 'BILSC_PASSIF'        : ('BILSEQ',)
        , 'BILSC_CR'            : ('BILSEQ',)
        , 'BILSC_AFF'           : ('BILSEQ',)
        , 'GMSIG'               : ('BILSEQ',)
        , 'RATIOS'              : ('BILSEQ',)
        , 'ANAFIN_INTRAPROD'    : ('BILSEQ',)
        , 'MOTIFS_NONSAISI'     : ('BILSEQ',)
        , 'ANADEC'              : ('ADC_BILSEQ',)
        , 'HISTOIRE_DU_BILAN'   : ('BILSEQ',)
    }

for tabname_1 in tabnames.iterkeys():
    print ("tabname_1: {}".format(tabname_1))
    print ("tabkeys[tabname_1]: {}".format(tabkeys[tabname_1]))
    print ("tabkeys[tabname_1].index('BILSEQ'): {}".format(tabkeys[tabname_1].index('BILSEQ')))
    for tabname_2 in tabnames[tabname_1]:
        print ("tabname_2: {}".format(tabname_2))
        print ("  tabkeys[tabname_2][0]: {}".format(tabkeys[tabname_2][0]))
