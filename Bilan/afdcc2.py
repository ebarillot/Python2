# -*- coding: utf-8 -*-

##
## programme de simulation du calcul AFDCC2
##

import cx_Oracle
import math
import sys


##bilseq = 18980631
##bilseq = 19040714
##bilseq = 19054331
bilseq = 20936314
plateforme = 'UA'
##bilseq = 999999999

print ('====================')
print ('plateforme = ' + plateforme)
print ('====================')

## les connexions Oracle
connstr = dict()
connstr['IA'] = dict()
connstr['UA'] = dict()
connstr['IA']['ort2prod'] = \
'ort2prod/ort2prodia@\
    (DESCRIPTION=(ADDRESS_LIST=(\
        ADDRESS=(PROTOCOL=TCP)(HOST=intdbirisfr.int.dns)\
        (PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=SVCDIFFINT1.world)))'
connstr['IA']['bileprod'] = \
'bileprod/bileprodia@\
    (DESCRIPTION=(ADDRESS_LIST=(\
        ADDRESS=(PROTOCOL=TCP)(HOST=intdbirisfr.int.dns)\
        (PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=SVCPRODINT1.world)))'

connstr['UA']['ort2prod'] = \
'etudes_consult/etudes_consultpre@\
    (DESCRIPTION=(ADDRESS_LIST=(\
        ADDRESS=(PROTOCOL=TCP)(HOST=irisfrpx.int.dns)\
        (PORT=1523)))(CONNECT_DATA=(SERVICE_NAME=SVCDIFFPRE1.world)))'
connstr['UA']['bileprod'] = \
'etudes_consult/etudes_consultpre@\
    (DESCRIPTION=(ADDRESS_LIST=(\
        ADDRESS=(PROTOCOL=TCP)(HOST=irisfrpx.int.dns)\
        (PORT=1523)))(CONNECT_DATA=(SERVICE_NAME=SVCPRODPRE1.world)))'

conn = dict()
conn['ort2prod'] = cx_Oracle.connect(connstr[plateforme]['ort2prod'])
conn['bileprod'] = cx_Oracle.connect(connstr[plateforme]['bileprod'])
curs = dict()
curs['ort2prod'] = conn['ort2prod'].cursor()
curs['bileprod'] = conn['bileprod'].cursor()


## coefficients de pondération
coeff_pond = dict()
coeff_pond['ind'] = [-11.0070, +0.0262, +0.0000, +0.0000, +0.0000, +1.7355, -0.0032, +0.0000, -0.0086, +0.0000, +0.0000, +0.0725, +0.0000, +0.0000, +0.0000, +3.3176, +0.6802]
coeff_pond['btp'] = [ +0.5301, +0.0220, +0.0000, -0.0043, +0.0000, +1.6712, +0.0000, -0.0070, +0.0000, -0.0086, +0.0000, +0.0720, +0.0000, -0.4764, +0.0000, +0.0000, +0.0000]
coeff_pond['cde'] = [ -5.3424, +0.0238, +0.0000, +0.0000, +0.0000, +0.9523, -0.0084, +0.0000, +0.0000, +0.0000, +0.0000, +0.1081, +0.0000, -0.2927, +0.0000, +1.8284, +0.3856]
coeff_pond['cgr'] = [ -1.1111, +0.0228, +0.0000, +0.0000, +0.0000, +0.8653, -0.0084, +0.0000, +0.0000, +0.0000, +0.0000, +0.1111, +0.0000, -0.3317, +0.0000, +1.8712, +0.1625]
coeff_pond['hcr'] = [-13.2770, +0.0050, +0.0000, -0.0050, +0.0000, +0.2073, +0.0000, +0.0000, +0.0000, +0.0000, +0.0468, +0.0000, +0.0000, +0.0000, +0.0000, +0.0000, +0.8948]
coeff_pond['sce'] = [ +0.9950, +0.0218, +0.0000, +0.0000, +0.0046, +0.9445, +0.0000, -0.0080, -0.0136, +0.0000, +0.0000, +0.0632, +0.0000, -0.2210, +0.0000, +0.0000, +0.0000]
coeff_pond['tra'] = [ -7.6017, +0.0259, +0.0000, +0.0000, +0.0184, +0.0000, +0.0000, +0.0000, +0.0000, +0.0085, +0.0000, +0.0529, +0.0000, -0.3945, +0.0000, +0.2934, +0.4467]


## les classes d'activités
def charge_APE(conn):
    ape = dict()
    curs = conn['bileprod'].cursor()
    req = dict()
    ## industrie
    req['ind'] = \
        "select cod from bileprod.libdom where fam='APE' and lan='FR'\
         and (   (cod >= '120Z' and cod <= '145Z') or (cod >= '151A' and cod <= '160Z')\
              or (cod >= '171A' and cod <= '183Z') or (cod >= '191Z' and cod <= '192Z')\
              or (cod  = '193Z')\
              or (cod >= '201A' and cod <= '205C') or (cod >= '211A' and cod <= '221L')\
              or (cod >= '221A' and cod <= '223E') or (cod >= '241A' and cod <= '247Z')\
              or (cod >= '251A' and cod <= '252H') or (cod >= '261A' and cod <= '268C')\
              or (cod >= '271Z' and cod <= '287P') or (cod >= '291A' and cod <= '297C')\
              or (cod >= '300A' and cod <= '323Z') or (cod >= '331A' and cod <= '335Z')\
              or (cod >= '341Z' and cod <= '355Z') or (cod >= '361A' and cod <= '372Z'))"
    ## BTP
    req['btp'] = \
          "select cod \
          from bileprod.libdom \
          where fam='APE' and lan='FR' \
          and ((cod >= '451A' and cod <= '455Z'))"
    ## commerce de détail
    req['cde'] = \
          "select cod \
          from bileprod.libdom \
          where fam='APE' and lan='FR' \
          and cod in ('501Z', '502Z', '503A', '503B', '504Z', '505Z', '521A', '521B', '521C', '521D', \
             '521E', '521F', '521H', '521J', '522A', '522C', '522E', '522G', '522J', '522L', \
             '522N', '522P', '523A', '523C', '523E', '524A', '524C', '524E', '524F', '524H', \
             '524L', '524N', '524P', '524R', '524T', '524U', '524V', '524W', '524X', '524Y', \
             '525Z', '526B', '526D', '526E', '526G', '526H')"
    ## commerce de gros
    req['cgr'] = \
          "select cod \
          from bileprod.libdom \
          where fam='APE' and lan='FR' \
          and (   (cod >= '511A' and cod <= '511U') or (cod >= '512A' and cod <= '512J') \
              or (cod >= '513A' and cod <= '513W') or (cod >= '514A' and cod <= '514S') \
              or (cod >= '515A' and cod <= '515Q') or (cod >= '516A' and cod <= '516N') \
              or (cod  = '517Z') \
              or (cod >= '527A' and cod <= '527H'))"
    ## hotellerie, cafés, restaurants
    req['hcr'] = \
          "select cod \
          from bileprod.libdom \
          where fam='APE' and lan='FR' \
          and cod in ('551A', '551C', '551D', '552C', '552E', '552F', '553A', '553B', \
             '554A', '554B', '555A', '555C', '555D')"
    ## services, hors transport
    req['sce'] = \
          "select cod \
          from bileprod.libdom \
          where fam='APE' and lan='FR' \
          and (   (cod >= '701A' and cod <= '701F') or (cod >= '701A' and cod <= '702C') \
              or (cod >= '703A' and cod <= '703E') or (cod  = '511Z') \
              or (cod >= '712A' and cod <= '721C') or (cod >= '713A' and cod <= '713G') \
              or (cod >= '714A' and cod <= '714D') \
              or (cod in ('721Z', '722Z', '723Z', '724Z', '725Z', '726Z', '731Z', '732Z')) \
              or (cod >= '741A' and cod <= '741J') or (cod >= '742A' and cod <= '742C') \
              or (cod >= '743A' and cod <= '743B') or (cod in ('746Z', '747Z')) \
              or (cod >= '748A' and cod <= '748K') \
              or (cod in ('745A', '745B', '801Z', '802A', '802B', '802C', '803Z', '852Z', '924Z')) \
              or (cod >= '804A' and cod <= '804D') or (cod >= '851A' and cod <= '851K') \
              or (cod >= '853A' and cod <= '853K') or (cod >= '921A' and cod <= '921J') \
              or (cod >= '922A' and cod <= '922C') or (cod >= '923A' and cod <= '923J') \
              or (cod >= '925A' and cod <= '925E') or (cod >= '926A' and cod <= '926C') \
              or (cod >= '927A' and cod <= '927C') or (cod >= '930A' and cod <= '930N'))"
    ## transport
    req['tra'] = \
          "select cod \
          from bileprod.libdom \
          where fam='APE' and lan='FR' \
          and (   (cod >= '602A' and cod <= '602P') \
              or (cod in ('601Z', '603Z', '611A', '611B', '612Z', '621Z4', '622Z', '623Z', '633Z')) \
              or (cod >= '631A' and cod <= '631E') or (cod >= '632A' and cod <= '632E') \
              or (cod >= '634A' and cod <= '634C'))"

    classe_liste = req.keys()

    for classe in classe_liste:
        ape[classe] = []
        curs.execute(req[classe])
        for row in curs:
            if len(str(row[0])) == 4:
                ##print str(row[0])
                ape[classe].append(str(row[0]))
    return ape


## bilan N-1 : recherche du bilseq
def getN1(conn,bilseq):
    curs = conn['bileprod'].cursor()
    oribilcod = ''
    typbilcod = ''
    req1 = "select oribilcod, typbilcod \
             from bileprod.bilan \
             where bilseq = :bilseq"

    req2 = "select bilseq \
            from bileprod.bilan \
            where (entrcs,bildatclo) = \
              (select entrcs,nvl(bildatclon1,add_months(bildatclo,-bilduree)) \
               from bilan \
               where bilseq=:v1) \
            and typbilcod = :v2 \
            and oribilcod = :v3 \
            and valcod in ('9','8')"

    req3 = "select bilseq \
            from bileprod.bilan \
            where (entrcs,bildatclo) = \
              (select entrcs,nvl(bildatclon1,add_months(bildatclo,-bilduree)) \
               from bileprod.bilan \
               where bilseq=:v1) \
            and typbilcod = :v2 \
            and valcod in ('9','8')"
    curs.execute(req1,(bilseq,))
    for row in curs:
        (oribilcod, typbilcod) = row
    bilseq_N1 = None
    curs.execute(req2,(bilseq,typbilcod,'IN'))
    for row in curs:
        (bilseq_N1,) = row
    if bilseq_N1 is None:
        curs.execute(req2,(bilseq,typbilcod,'BL'))
        for row in curs:
            (bilseq_N1,) = row
    if (bilseq_N1 is None) & (oribilcod not in ['IN','BL']):
        curs.execute(req3,(bilseq,typbilcod))
        for row in curs:
            (bilseq_N1,) = row
    return bilseq_N1



## les données en base pour le bilan
## TODO : decouper le code qui suit en fonctions dont une launch_tests()

curs['bileprod'].execute('select sysdate from dual')
for row in curs['bileprod']:
    print(row)

print ("Chargement des classes d'APE ...")
ape = charge_APE(conn)
print ("... OK")

bilseq_N1 = getN1(conn,bilseq)
print "bilseq    = " + str(bilseq)
print "bilseq_N1 = " + str(bilseq_N1)

if bilseq_N1 is None:
    print ("Pas de bilan N1 pour bilseq = "+str(bilseq))
    sys.exit(0)

## recherche du RCS dans bilan
curs['bileprod'].execute('SELECT ENTRCS FROM bileprod.bilan WHERE bilseq=:bilseqA',(bilseq,))
for row in curs['bileprod']:
    entrcs = str(row[0])
    print('entrcs = '+ entrcs)
try:
    entrcs
except:
    print('Aucun entrcs pour bilseq = '+ str(bilseq))
    sys.exit(0)

## ape dans ort2prod
curs['ort2prod'].execute('SELECT ENTAPECOD FROM ort2prod.entrep WHERE entnumtyp=0 and entnum=:ENTNUM',(entrcs,))
for row in curs['ort2prod']:
    entape = str(row[0])
    print('entape = '+ entape)
try:
    entape
except:
    print('Aucun entape pour entrcs = '+ entrcs)
    sys.exit(0)
## la classe associée à l'entreprise à laquelle appartient le bilseq
classe_liste = ape.keys()
the_classe = ''
for classe in classe_liste:
    if entape in ape[classe]:
        the_classe = classe
        break
print ('classe = '+the_classe)


req_bilsc_actif = 'select scaa, scbj, scbk, scbl, scbn, scbp, scbr, scbt, scbx, scch,\
                          scci, sccj, scck, sccl, sccm, sccn, sccu\
                          from bileprod.bilsc_actif where bilseq = :entbilseq'
curs['bileprod'].execute(req_bilsc_actif,(bilseq,))
for row in curs['bileprod']:
    scaa, scbj, scbk, scbl, scbn, scbp, scbr, scbt, scbx, scch, scci, sccj, scck, sccl, sccm, sccn, sccu = (row)
    print('actif : ' + str(row))


req_bilsc_passif = 'select scdh, scdj, scdl, scdo, scdr, scds, scdt, scdu, scdv, scdw,\
                           scdx, scdy, scdz, scea, sceb, scec, sced, sceh\
                           from bileprod.bilsc_passif where bilseq = :entbilseq'
curs['bileprod'].execute(req_bilsc_passif,(bilseq,))
for row in curs['bileprod']:
    scdh, scdj, scdl, scdo, scdr, scds, scdt, scdu, scdv, scdw, scdx, scdy, scdz, scea, sceb, scec, sced, sceh  = (row)
    print('passif : ' + str(row))


req_bilsc_cr = 'select scfl, scfm, scfn, scfo, scfp, scfs, scft, scfu, scfv, scfw,\
                       scfx, scfy, scfz, scga, scgb, scgc, scgd, scgm, scgq, scgr,\
                       scgw, scha, sche, schj, schk\
                       from bileprod.bilsc_cr where bilseq = :entbilseq'
curs['bileprod'].execute(req_bilsc_cr,(bilseq,))
for row in curs['bileprod']:
    scfl, scfm, scfn, scfo, scfp, scfs, scft, scfu, scfv, scfw, scfx, scfy, scfz, scga, scgb, scgc, scgd, scgm, scgq, scgr, scgw, scha, sche, schj, schk = (row)
    print('cr : ' + str(row))

req_bilsc_cr_N1 = 'select scfl from bileprod.bilsc_cr where bilseq = :bilseq'
curs['bileprod'].execute(req_bilsc_cr_N1,(bilseq_N1,))
for row in curs['bileprod']:
    scfl_N1, = row
    print('cr N-1 : ' + str(row))

req_bilsc_aff = 'select scys, scyy, scyz from bileprod.bilsc_aff where bilseq = :entbilseq'
curs['bileprod'].execute(req_bilsc_aff,(bilseq,))
for row in curs['bileprod']:
    scys, scyy, scyz = (row)
    print('aff : ' + str(row))

conn['bileprod'].close()
conn['ort2prod'].close()


## les formules des ratios AFDCC2
r0 = 1.
r1 = 100. * (scdl + scdo) / (scdl + scdo + scdr + scds + scdt + scdu + scdv - sceh + sced + scbk - scaa - sccm)
r2 = (scdl + scdo + scdr + scds + scdt + scdu + scdv - sceh + sced + scbk - scaa - sccm) / (scbj + sccl + sccn)
r3 = 360. * (scec - sceb + scys) / scfl
r4 = 360. * (scdl + scdo + scdr + scds + scdt + scdu + scdv - sceh + sced + scbk - scbj - scaa - sccl - sccm - sccn) / scfl
r5 = (sccj - scch - scck - sccl) / (scdw + scdx + scdy + scdz + scea + sceh)
r6 = 360. * scdx / (scfs + scfu + scfw + scyz)
r7 = 360. * (scbx + scys) / (scfl + scyy)
r8 = 360. * (scbl + scbn + scbp + scbr + scbt) / scfl
r9 = 360. * scbj / scfl
r10 = 100. * (scfl + scfm + scfn - scfs - scft - scfu - scfv - scfw) / scfl
r11 = 100. * (scfl + scfm + scfn + scfo - scfs - scft - scfu - scfv - scfw - scfx - scfy - scfz) / (scfl + scfo)
r12 = (scds + scdt + scdu + scdv - sceh) / (scgw - scfp + scga + scgb + scgc + scgd - scgm + scgq + scha - sche - schj - schk)
r13 = 100. * scgr / scfl
r14 = 100. * (scgw - scfp + scga + scgb + scgc + scgd - scgm + scgq + scha - sche - schj - schk) / (scfl + scfm + scfn - scfs - scft - scfu - scfv - scfw)
r15 = (scfl - scfl_N1) / scfl_N1
r16 = math.log10(scfl)

ratios = list()
ratios = [r0,r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16]

for i in range(len(ratios)):
    print('r'+str(i)+' = '  + str(ratios[i]))


## bornes
def bornage(ratios,num):
    if num == 1:
        if ratios[num] < -100.0:
            ratios[num] = -100.0
        elif ratios[num] > 100.0:
            ratios[num] = 100.0
    if num == 2:
        if ratios[num] > 10.0:
            ratios[num] = 10.0
    if num == 3:
        if ratios[num] > 500.0:
            ratios[num] = 500.0
    if num == 4:
        if ratios[num] > 360.0:
            ratios[num] = 360.0
        elif ratios[num] < 0.0:
            ratios[num] = 0.0
    if num == 5:
        if ratios[num] > 6.0:
            ratios[num] = 6.0
        elif ratios[num] < 0.0:
            ratios[num] = 0.0
    if num == 6:
        if ratios[num] > 500.0:
            ratios[num] = 500.0
    if num == 7:
        if ratios[num] > 500.0:
            ratios[num] = 500.0
    if num == 8:
        if ratios[num] > 360.0:
            ratios[num] = 360.0
        elif ratios[num] < 0.0:
            ratios[num] = 0.0
    if num == 9:
        if ratios[num] > 1500.0:
            ratios[num] = 1500.0
        elif ratios[num] < 10.0:
            ratios[num] = 0.0
    if num == 10:
        if ratios[num] > 100.0:
            ratios[num] = 100.0
        elif ratios[num] < -100.0:
            ratios[num] = -100.0
    if num == 11:
        if ratios[num] > 35.0:
            ratios[num] = 35.0
        elif ratios[num] < -30.0:
            ratios[num] = -30.0
    if num == 12:
        if ratios[num] > 50.0:
            ratios[num] = 50.0
        elif ratios[num] < -100.0:
            ratios[num] = -100.0
    if num == 13:
        if ratios[num] > 5.0:
            ratios[num] = 5.0
    if num == 15:
        if ratios[num] > 2.0:
            ratios[num] = 2.0
        elif ratios[num] < -2.0:
            ratios[num] = -2.0


## les ratios pondérés
print ('===============================')
## calcul des ratios pondérés et du score
if the_classe != '':
    the_pond = coeff_pond[the_classe]
    ratios_pond = list()
    score = 0.
    for i in range(len(ratios)):
        bornage(ratios,i)
        ratios_pond.append(ratios[i] * the_pond[i])
    ## affichage
    for i in range(len(ratios)):
        print('rp'+str(i)+' = '  + str(round(ratios_pond[i],2)))
        score += ratios_pond[i]
    print ('score = '+str(round(score,2)))
else:
    print ('Pas de classe trouvée pour ape = '+entape)


