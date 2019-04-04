SELECT CCLENTNUM_PK, cclseq_pk,
	 decode(ccltypexecod,'-1',NULL,'RIEN',NULL,ccltypexecod),
	 to_char(ccldateexercice,'YYYY/MM/DD'), ccldateexepre, ccldureeexercice,
         decode(cclcatramoncod,'-1',NULL,'RIEN',NULL,cclcatramoncod),
         decode(cclrntramoncod,'-1',NULL,'RIEN',NULL,cclrntramoncod),
	 decode(ccltypmoncod,'-1',NULL,'RIEN',NULL,'COMM','REEL','BILAN','REEL',ccltypmoncod),
	 cclrn,
	 decode(ccldevisecod,'-1','0',NULL,'0',ccldevisecod), nvl(cclexpunm,0),
         cclsup,
         to_char(cclhisdateff,'YYYY/MM/DD'), cclhiseffpre,
         cclhispoidateff,
	 decode(cclhisoricod,'-1',NULL,'RIEN',NULL,cclhisoricod),
	 decode(cclhissupportcod,'-1',NULL,'RIEN',NULL,cclhissupportcod),
         cclhisnumsupport, cclhisnuminf,
	 to_char(cclhisdatpub,'YYYY/MM/DD'), cclhispubpre,
	 to_char(ccldatord,'YYYY/MM/DD'),
	 cclca,
         cclcaexport, cclresultatexploit,
	 cclrcai, cclfondspropres, cclcaf, cclendettement,
         ccleffectif, cclmontantachats,
         ccldureeclients, ccldureefournisseurs,
         cclbilseq
    FROM CHIFFRESCLES, ENTREP, SCORES_RATING
    WHERE CCLENTNUMTYP_PK   = 0
--    AND   CCLENTNUM_PK      = pENTNUM
    AND   to_char(ccldateexercice,'YYYY') >= to_char(sysdate,'YYYY')-3
    AND   CCLENTNUMTYP_PK = ENTNUMTYP
    AND   CCLENTNUM_PK    = ENTNUM
    AND   CCLENTNUMTYP_PK = SCO_ENTNUMTYP_PK
    AND   CCLENTNUM_PK    = SCO_ENTNUM_PK
    AND   SCO_ETATCOD      = 'ACT'
    AND SCO_HISDATORD   = ( SELECT max(SCO_HISDATORD) FROM SCORES_RATING
				WHERE   CCLENTNUMTYP_PK = SCO_ENTNUMTYP_PK AND
					SCO_ENTNUM_PK    = CCLENTNUM_PK AND
				        SCO_ETATCOD   = 'ACT')
    AND  ((CCLTYPMONCOD like 'EST%' and
         SCO_SCORE_10 not in (0,99,50)     and
         to_char(ENTDATCRE,'YYYY') < to_char(sysdate,'YYYY')-1)
        OR
        (CCLTYPMONCOD not like 'EST%'))
    AND CCLETATCOD='ACT'
    AND CCLSUP is NULL
    ORDER BY ccldateexercice DESC,
             decode (CCLTYPEXECOD||CCLTYPMONCOD,'CONSBILAN',1 , 'CONSCOMM', 2, 'SOCBILAN', 3, 'SOCCOMM', 4, 'SOCEST1', 5, 'SOCEST2', 6, 7) asc
/


select power(10,3) from dual;