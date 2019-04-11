set timing on

--whenever SQLERROR exit 2 rollback
set echo on
set feedb on
show user

-- <sqlToIntegrate>

/*
  Package qui contient les fonctions qui permettent de calculer à la volée les chiffres clés
  à partir des données des bilans.
*/
  
create or replace package pkg_funaff_chiffrescles is

type TableauCHAINE is table of varchar2(500) index by binary_integer;

/*
  Fonction qui retourne les mêmes informations que son homonyme dans le package ort2prod.pkg_funaff_chiffrescles
  Mais elle prend en entrée le clipre + cliref
*/
function fun_aff_3bilseqCC (
    pMESSAGE        out varchar2,
    pENTNUMTYP      in  number default 0,
    pENTNUM         in  varchar2,
    pFORDATES       in  varchar2 default 'YYYYMMDD',
    pNBRLIGOUT      out number,
    pTAB            out TableauChaine,
    pLANCOD         in  varchar2 default 'FR',
    pDEVISEIN       in  varchar2 default '300',
    pUNITEIN        in  varchar2 default '0',
    pLIBELLE        in  varchar2 default 'O',
    pTYPEXECOD      in  varchar2 default 'SOC',
    pNBRANNEE       in  number   default -1,
    pACCES_CONF     in  varchar2 default 'N',
    pACCES_EVAL     in  varchar2 default 'N',
    pCLIPRE         in varchar2,
    pCLIREF         in varchar2
) return number;

end pkg_funaff_chiffrescles ;
/
show error



create or replace package body pkg_funaff_chiffrescles is

type t_chiffrescles is record (
  CA            varchar2(20),  -- chiffre d'affaire
  resnet        varchar2(20),  -- resultat net
  caExport      varchar2(20),  -- CA Export
  resExploit    varchar2(20),  -- Resutat d'exploitation
  rcai          varchar2(20),  -- RCAI
  fonds         varchar2(20),  -- Fonds propres
  caf           varchar2(20),  -- CAF
  endette       varchar2(20),  -- Endettement
  effectif      varchar2(20),  -- Effectif
  monAchats     varchar2(20),  -- Montant des achats
  dureeCli      varchar2(20),  -- Durée clients
  dureeFou      varchar2(20),  -- Durée fournisseurs
  fondsDedies   varchar2(20)  -- Fonds dédiés
);
type t_tab_chiffrescles is table of t_chiffrescles;


procedure ouput_chiffrescles(v_chiffrescles t_chiffrescles) is
begin
  dbms_output.put_line('chiffre d''affaire      '||   v_chiffrescles.CA            );
  dbms_output.put_line('resultat net            '||   v_chiffrescles.resnet        );
  dbms_output.put_line('CA Export               '||   v_chiffrescles.caExport      );
  dbms_output.put_line('Resutat d''exploitation '||   v_chiffrescles.resExploit    );
  dbms_output.put_line('RCAI                    '||   v_chiffrescles.rcai          );
  dbms_output.put_line('Fonds propres           '||   v_chiffrescles.fonds         );
  dbms_output.put_line('CAF                     '||   v_chiffrescles.caf           );
  dbms_output.put_line('Endettement             '||   v_chiffrescles.endette       );
  dbms_output.put_line('Effectif                '||   v_chiffrescles.effectif      );
  dbms_output.put_line('Montant des achats      '||   v_chiffrescles.monAchats     );
  dbms_output.put_line('Durée clients           '||   v_chiffrescles.dureeCli      );
  dbms_output.put_line('Durée fournisseurs      '||   v_chiffrescles.dureeFou      );
  dbms_output.put_line('Fonds dédiés            '||   v_chiffrescles.fondsDedies   );
end;


function recuperelibelle (  pFAM in varchar2,
                            pLAN in varchar2,
                            pCOD in varchar2)
return varchar2 is
    pLIB varchar2(2000) := null;
begin
    /*
    ** Recupere libellé
    */
    select LIB
    into   pLIB
    from   LIBDOM
    where  FAM = pFAM
    and    COD = pCOD
    and    LAN = pLAN;
    return pLIB;

exception
    when NO_DATA_FOUND then
        pLIB := null;
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction recuperelibelle : ('||sqlcode||') - '||sqlerrm);

end recuperelibelle;


function open_curs_SC(pbilseq number)
    return sys_refcursor
is
    curs_SC sys_refcursor;
begin
    open curs_SC for 'SELECT
        /* 01 caffbil       */      gm.SIG24
        /* 02 resnetbil     */    , gm.SIG6
        /* 03 caExportbil   */    , gm.SIG38
        /* 04 resExploitbil */    , gm.SIG4
        /* 05 rcaibil       */    , gm.SIG5
        /* 06 fondsbil      */    , nvl(sp.SCDL,0)+nvl(sp.SCDO,0)
        /* 07 cafbil        */    , ra.R11
        /* 08 endettebil    */    , nvl(sp.scds,0)+nvl(sp.scdt,0)+nvl(sp.scdu,0)+nvl(sp.scdv,0)+nvl(sa.scys,0)
        /* 09 effectifbil   */    , sa.scyp
        /* 10 monAchatsbil  */    , nvl(cr.scfs,0)+nvl(cr.scfu,0)+nvl(cr.scfw,0)
        /* 11 dureeClibil   */    , ra.R28
        /* 12 dureeFoubil   */    , ra.R29
        /* 13 fondsDedies   */    , null
         FROM gmsig gm, bilsc_cr cr, ratios ra, BILSC_PASSIF sp, BILSC_AFF sa
        WHERE gm.bilseq = :pbilseq
          AND gm.bilseq = cr.bilseq
          AND gm.bilseq = ra.bilseq
          AND gm.bilseq = sa.bilseq
          AND gm.bilseq = sp.bilseq'
          using pbilseq;
    return curs_SC;
end;


function open_curs_SC_EVAL(pbilseq number)
    return sys_refcursor
is
    curs_SC_EVAL sys_refcursor;
begin
    open curs_SC_EVAL for select
        /* 01 caff       */      case when an.adc_deval12_val = 'EVAL' then an.adc_deval12 else null end
        /* 02 resnet     */    , gm.SIG6
        /* 03 caExport   */    , null
        /* 04 resExploit */    , case when an.adc_deval6_val = 'EVAL' then an.adc_deval6 else null end
        /* 05 rcai       */    , case when an.adc_deval4_val = 'EVAL' then an.adc_deval4 else null end
        /* 06 fonds      */    , nvl(pas.SCDL,0)+nvl(pas.SCDO,0)
        /* 07 caf        */    , case when an.adc_deval11_val = 'EVAL' and an.adc_deval12_val = 'EVAL' and an.adc_deval12 > 0 then round(100*an.adc_deval11/an.adc_deval12,2) else null end
        /* 08 endette    */    , nvl(pas.scds,0)+nvl(pas.scdt,0)+nvl(pas.scdu,0)+nvl(pas.scdv,0)+nvl(aff.scys,0)
        /* 09 effectif   */    , aff.scyp
        /* 10 monAchats  */    , null
        /* 11 dureeCli   */    , case when an.adc_deval12_val != 'EVAL' or an.adc_deval12 is null or an.adc_deval12 = 0 then null else (((nvl(act.scbx,0)-nvl(pas.scdw,0))*bil.bilduree*30) / an.adc_deval12) end
        /* 12 dureeFou   */    , null
        /* 13 fondsDedies*/    , null
             from bileprod.bilan bil, bileprod.anadec an, bileprod.gmsig gm, bileprod.BILSC_ACTIF act, bileprod.BILSC_PASSIF pas, bileprod.BILSC_AFF aff
            where bil.bilseq = pbilseq
              and bil.bilseq = act.bilseq
              and bil.bilseq = pas.bilseq
              and bil.bilseq = aff.bilseq
              and bil.bilseq = an.adc_bilseq (+)
              and bil.bilseq = gm.bilseq;
    return curs_SC_EVAL;
end;


function open_curs_SS(pbilseq number)
    return sys_refcursor
is
    curs_SS sys_refcursor;
begin
    open curs_SS for select
        /* 01 caffbil       */      gm.SIG24
        /* 02 resnetbil     */    , gm.SIG6
        /* 03 caExportbil   */    , gm.SIG38
        /* 04 resExploitbil */    , gm.SIG4
        /* 05 rcaibil       */    , gm.SIG5
        /* 06 fondsbil      */    , ss.SS142
        /* 07 cafbil        */    , null
        /* 08 endettebil    */    , ss.ss156
        /* 09 effectifbil   */    , cr.ss376
        /* 10 monAchatsbil  */    , nvl(cr.ss234,0)+nvl(cr.ss238,0)+nvl(cr.ss242,0)
        /* 11 dureeClibil   */    , ra.R28
        /* 12 dureeFoubil   */    , ra.R29
        /* 13 fondsDedies   */    , null
             from gmsig gm, bilss_cr cr, ratios ra, bilss ss
            where gm.bilseq = pbilseq
              and gm.bilseq = cr.bilseq
              and gm.bilseq = ra.bilseq
              and gm.bilseq = ss.bilseq;
    return curs_SS;
end;


function open_curs_SS_EVAL(pbilseq number)
    return sys_refcursor
is
    curs_SS_EVAL sys_refcursor;
begin
    open curs_SS_EVAL for select
        /* 01 caff       */      case when an.adc_deval12_val = 'EVAL' then an.adc_deval12 else null end
        /* 02 resnet     */    , gm.SIG6
        /* 03 caExport   */    , null
        /* 04 resExploit */    , case when an.adc_deval6_val = 'EVAL' then an.adc_deval6 else null end
        /* 05 rcai       */    , case when an.adc_deval4_val = 'EVAL' then an.adc_deval4 else null end
        /* 06 fonds      */    , ss.SS142
        /* 07 caf        */    , case when an.adc_deval11_val = 'EVAL' and an.adc_deval12_val = 'EVAL' and an.adc_deval12 > 0 then round(100*an.adc_deval11/an.adc_deval12,2) else null end
        /* 08 endette    */    , ss.ss156
        /* 09 effectif   */    , cr.ss376
        /* 10 monAchats  */    , null
        /* 11 dureeCli   */    , case when an.adc_deval12_val != 'EVAL' or an.adc_deval12 is null or an.adc_deval12 = 0 then null else ((nvl(ss.ss068,0)-nvl(ss.ss164,0)*bil.bilduree*30) / an.adc_deval12) end
        /* 12 dureeFou   */    , null
        /* 13 fondsDedies*/    , null
             from bilan bil, anadec an, gmsig gm, BILSS ss, bilss_cr cr
            where bil.bilseq = pbilseq
              and bil.bilseq = ss.bilseq
              and bil.bilseq = cr.bilseq
              and bil.bilseq = an.adc_bilseq (+)
              and bil.bilseq = gm.bilseq;
    return curs_SS_EVAL;
end;


function get_cursor_bilan(
    bilseq      number,
    typbilcod   varchar2,
    oribilcod   varchar2,
    crconf      varchar2
)
return sys_refcursor
is
    curs_bilan sys_refcursor;
begin
    if typbilcod = 'SC' then
        if crconf = 'OUI' and oribilcod not in ('EC','RC') then
            curs_bilan := open_curs_SC_EVAL(bilseq);
        else
            curs_bilan := open_curs_SC(bilseq);
        end if;
    elsif typbilcod = 'SS' then
        if crconf = 'OUI' and oribilcod not in ('EC','RC') then
            curs_bilan := open_curs_SS_EVAL(bilseq);
        else
            curs_bilan := open_curs_SS(bilseq);
        end if;
    end if;
    --    curs_bilan := open_curs_SC(bilseq);
    return curs_bilan;

end get_cursor_bilan;


function fetch_bilan (
    p_refcur    in out SYS_REFCURSOR
)
return t_chiffrescles
is
    v_chiffrescles  t_chiffrescles;
begin
    fetch p_refcur into v_chiffrescles;
    return v_chiffrescles;
end;


procedure close_refcur (
    p_refcur    in out SYS_REFCURSOR
)
is
begin
    close p_refcur;
end;


/************************************************************************************/
function fun_aff_3bilseqCC (
    pMESSAGE    out     varchar2,
    pENTNUMTYP  in      number default 0,
    pENTNUM     in      varchar2,
    pFORDATES   in      varchar2 default 'YYYYMMDD',
    pNBRLIGOUT  out     number,
    pTAB        out     TableauChaine,
    pLANCOD     in      varchar2 default 'FR',
    pDEVISEIN   in      varchar2 default '300',
    pUNITEIN    in      varchar2 default '0',
    pLIBELLE    in      varchar2 default 'O',
    pTYPEXECOD  in      varchar2 default 'SOC',
    pNBRANNEE   in      number   default -1,
    pACCES_CONF in      varchar2 default 'N',
    pACCES_EVAL in      varchar2 default 'N',
    pCLIPRE     in      varchar2,
    pCLIREF     in      varchar2)
return number
is
/*
** Tableau retourné :
** 1  montant dernier CA
**    date dernier CA
**    montant dernier resultat net
**    date dernier resultat net
** 5  duree du dernier exercice

**    montant avant dernier CA
**    date avant dernier CA
**    montant avant dernier resultat net
**    date avant dernier resultat net
** 10 duree avant dernier exercice

**    montant antepenultieme CA
**    date antepenultieme CA
**    montant antepenultieme resultat net
**    date antepenultieme resultat net
** 15 duree antepenultieme exercice

**    % variation du dernier CA
**    % variation avant dernier CA
**    % variation dernier resultat net
**    % variation avant dernier resultat net
**
**    ===> champs ajoutes
** 20 precision date du dernier exercice
**    code devise saisie du dernier CA/resultat net
**    libelle devise saisie du dernier CA/resultat net
**    unite monetaire saisie du dernier CA/resultat net
**    code devise demande du dernier CA/resultat net
** 25 libelle devise demande du dernier CA/resultat net
**    unite monetaire demande du dernier CA/resultat net
**    precision date de l'avant dernier exercice
**    code devise saisie avant dernier CA/resultat net
**    libelle devise saisie avant dernier CA/resultat net
** 30 unite monetaire saisie avant dernier CA/resultat net
**    code devise demande avant dernier CA/resultat net
**    libelle demande saisie avant dernier CA/resultat net
**    unite monetaire demande avant dernier CA/resultat net
**    precision date de l'antepenultieme exercice
** 35 code devise saisie antepenultieme CA/resultat net
**    libelle devise saisie antepenultieme CA/resultat net
**    unite monetaire saisie antepenultieme CA/resultat net
**    code devise demande antepenultieme CA/resultat net
**    libelle devise demande antepenultieme CA/resultat net
** 40 unite monetaire demande antepenultieme CA/resultat net

**    evolution dernier chiffres cles export
**    evolution avantdernier chiffres cles export
**    evolution dernier resultat exploitation
**    evolution avant dernier resultat exploitation
** 45 evolution dernier RCAI
**    evolution avant dernier RCAI
**    evolution dernier fond propre
**    evolution avant dernier fond propre
**    evolution dernier endettement
** 50 evolution avant dernier endettement
**    evolution dernier CAF
**    evolution avant dernier CAF
**    evolution dernier montant d'achats
**    evolution avant dernier montant d'achats

** 55 dernier CA export
**    dernier resultat exploitation
**    dernier RCAI
**    dernier fond propre
**    dernier endettement
** 60 dernier CAF
**    dernier montant achats
**    derniere duree clients
**    derniere duree fournisseurs
**    dernier effectif

** 65 avant dernier CA export
**    avant dernier resultat exploitation
**    avant dernier RCAI
**    avant dernier fond propre
**    avant dernier endettement
** 70 avant dernier CAF
**    avant dernier montant achats
**    avant derniere duree clients
**    avant derniere duree fournisseurs
**    avant dernier effectif

** 75 antepenultieme CA export
**    antepenultieme resultat exploitation
**    antepenultieme RCAI
**    antepenultieme fond propre
**    antepenultieme endettement
** 80 antepenultieme CAF
**    antepenultieme montant achats
**    antepenultieme duree clients
**    antepenultieme duree fournisseurs
**    antepenultieme effectif

** 85 provenance
**    provenance N-1
** 87 provenance N-2

** 88 type
**    type N-1
** 90 type N-2

** 91 lib Type
**    lib Type N-1
** 93 lib Type N-2

** 94 tranche de CA
**    tranche de CA N-1
** 96 tranche de CA N-2

** 97 Libelle tranche de CA
**    Libelle tranche de CA N-1
** 99 Libelle tranche de CA N-2


*/
    i                               binary_integer  := 1;
    ret                             number(10);
    compteur                        number(2)       := 0;
    pourcent                        number(18,2);

    Vccldevisecod                   varchar2(12);
    Vcclexpunm                      varchar2(2);
    Vnbrannee                       number(2);

    VcclcaEUR                       number(15)      := null;
    VcclresEUR                      number(15)      := null;
    DernierCAEUR                    number(15)      := null;
    DernierResEUR                   number(15)      := null;
    AvDernierCAEUR                  number(15)      := null;
    AvDernierResEUR                 number(15)      := null;
    AnteCAEUR                       number(15)      := null;
    AnteResEUR                      number(15)      := null;

    Vcclca                          varchar2(15)    := null;
    Vccldateexe                     varchar2(50)    := null;
    Vcclres                         varchar2(15)    := null;
    Vccldurexe                      varchar2(2)     := null;
    Vccldateexepre                  varchar2(1)     := null;

    vDEVISEIN                       varchar2(12)    := null;
    vUNITEIN                        varchar2(12)    := null;
    DeviseSaisie                    varchar2(12)    := null;
    UniteSaisie                     varchar2(12)    := null;
    DeviseRetour                    varchar2(12)    := null;
    UniteRetour                     varchar2(12)    := null;
    fonction_err                    varchar2(200)   := null;
    CAretourne                      varchar2(15)    := null;
    RNretourne                      varchar2(15)    := null;
    UniteDemande                    varchar2(12)    := null;
    DeviseDemande                   varchar2(12)    := null;
    CAFretourne                     varchar2(15)    := null;
    Vccldeviscodsaisie              varchar2(12)    := null;
	
    Vcclcaexport                    number(15)      := null;
    Vcclresultatexploit             number(15)      := null;
    Vcclrcai                        number(15)      := null;
    Vcclfondspropres                number(15)      := null;
    Vcclendettement                 number(15)      := null;
    Vcclcaf                         number(23,2)    := null;
    Vcclmontantachats               number(15)      := null;
    Vccldureeclients                number(23)      := null;
    Vccldureefournisseurs           number(23)      := null;
    Vccleffectif                    number(15)      := null;
    Vccltypmoncod                   varchar2(12)    := null;
    Vcclsup                         varchar2(12)    := null;
    Vcclcrconf                      varchar2(12)    := null;
    Vccltype                        varchar2(12)    := null;
    Vccllibtype                     varchar2(500)   := null;

    VcclcaexportEUR                 number(15)      := null;
    VcclresultatexploitEUR          number(15)      := null;
    VcclrcaiEUR                     number(15)      := null;
    VcclfondspropresEUR             number(15)      := null;
    VcclendettementEUR              number(15)      := null;
    VcclcafEUR                      number(23,2)    := null;
    VcclmontantachatsEUR            number(15)      := null;


    CAexportretourne                number(15)      := null;
    RESexploitretourne              number(15)      := null;
    RCAIretourne                    number(15)      := null;
    FPretourne                      number(15)      := null;
    ENDETTretourne                  number(15)      := null;
    CAF2retourne                    number(23,2)    := null;
    MONTANTachatsretourne           number(15)      := null;

    VDernierCAexportretourne        number(15)      := null;
    VDernierRESexploitretourne      number(15)      := null;
    VDernierRCAIretourne            number(15)      := null;
    VDernierFPretourne              number(15)      := null;
    VDernierENDETTretourne          number(15)      := null;
    VDernierMONTANTachatsretourne   number(15)      := null;

    VAvDernierCAexportretourne      number(15)      := null;
    VAvDernierRESexploitretourne    number(15)      := null;
    VAvDernierRCAIretourne          number(15)      := null;
    VAvDernierFPretourne            number(15)      := null;
    VAvDernierENDETTretourne        number(15)      := null;
    VAvDernierMONTANTachatsretour   number(15)      := null;

    VAnteCAexportretourne           number(15)      := null;
    VAnteRESexploitretourne         number(15)      := null;
    VAnteRCAIretourne               number(15)      := null;
    VAnteFPretourne                 number(15)      := null;
    VAnteENDETTretourne             number(15)      := null;
    VAnteMONTANTachatsretourne      number(15)      := null;

    DernierCA                       number(15)      := null;
    DernierRes                      number(15)      := null;
    VDerniercclcaexport             number(15)      := null;
    VDerniercclresultatexploit      number(15)      := null;
    VDerniercclrcai                 number(15)      := null;
    VDerniercclfondspropres         number(15)      := null;
    VDerniercclendettement          number(15)      := null;
    VDerniercclcaf                  number(23,2)    := null;
    VDerniercclmontantachats        number(15)      := null;
    VDernierccldureeclients         number(23)      := null;
    VDernierccldureefournisseurs    number(23)      := null;
    VDERNIERCCLEFFECTIF             number(15)      := null;
    VDERNIERPRECDATE                varchar2(1)     := null;
    VDERNIERDEVISESAISIE            varchar2(12)    := null;
    VLIBDERNIERDEVISESAISIE         varchar2(500)   := null;
    VDERNIERUNITESAISIE             varchar2(2)     := null;
    VDERNIERDEVISERETOUR            varchar2(12)    := null;
    VLIBDERNIERDEVISERETOUR         varchar2(500)   := null;
    VDERNIERUNITERETOUR             varchar2(2)     := null;
    VDERNIEREPROVENANCE             varchar2(12)    := null;
    VDernierType                    varchar2(12)    := null;
    VDernierlibType                 varchar2(500)   := null;


    AVDERNIERCA                     number(15)      := null;
    AVDERNIERRES                    number(15)      := null;
    VAVDERNIERCCLCAEXPORT           number(15)      := null;
    VAVDERNIERCCLRESULTATEXPLOIT    number(15)      := null;
    VAVDERNIERCCLRCAI               number(15)      := null;
    VAvDerniercclfondspropres       number(15)      := null;
    VAvDerniercclendettement        number(15)      := null;
    VAvDerniercclcaf                number(23,2)    := null;
    VAvDerniercclmontantachats      number(15)      := null;
    VAvDernierccldureeclients       number(23)      := null;
    VAvDernierccldureefournisseurs 	number(23)      := null;
    VAvDernierccleffectif           number(15)      := null;
    VAvDernierprecdate             	varchar2(1)     := null;
    VAvDernierDeviseSaisie          varchar2(12)    := null;
    VlibAvDernierDeviseSaisie       varchar2(500)   := null;
    VAvDernierUniteSaisie           varchar2(2)     := null;
    VAvDernierDeviseRetour          varchar2(12)    := null;
    VlibAvDernierDeviseRetour       varchar2(500)   := null;
    VAvDernierUniteRetour           varchar2(2)     := null;
    VAvDerniereProvenance           varchar2(12)    := null;
    VAvDernierType                  varchar2(12)    := null;
    VAvDernierlibType               varchar2(500)   := null;


    AnteCA                          number(15)      := null;
    AnteRes                         number(15)      := null;
    VAntecclcaexport                number(15)      := null;
    VAntecclresultatexploit         number(15)      := null;
    VAntecclrcai                    number(15)      := null;
    VAntecclfondspropres            number(15)      := null;
    VAntecclendettement             number(15)      := null;
    VAntecclcaf                     number(23,2)    := null;
    VAntecclmontantachats           number(15)      := null;
    VAnteccldureeclients            number(23)      := null;
    VAnteccldureefournisseurs       number(23)      := null;
    VAnteccleffectif                number(15)      := null;
    VAnteprecdate                   varchar2(1)     := null;
    VAnteDeviseSaisie               varchar2(12)    := null;
    VlibAnteDeviseSaisie            varchar2(500)   := null;
    VAnteUniteSaisie                varchar2(2)     := null;
    VAnteDeviseRetour               varchar2(12)    := null;
    VlibAnteDeviseRetour            varchar2(500)   := null;
    VAnteUniteRetour                varchar2(2)     := null;
    VAnteProvenance                 varchar2(12)    := null;
    VAnteType                       varchar2(12)    := null;
    VAntelibType                    varchar2(500)   := null;


    Vcclcatramoncod                 number(12)      := null;
    VDerniercclcatramoncod          number(12)      := null;
    VAvDerniercclcatramoncod        number(12)      := null;
    VAntecclcatramoncod             number(12)      := null;

    VLibDerniercclcatramoncod       varchar2(500)   := null;
    VLibAvDerniercclcatramoncod     varchar2(500)   := null;
    VLibAntecclcatramoncod          varchar2(500)   := null;

    type type_curs is ref cursor;
    c_chiffrescles type_curs;

    vNBBILOUT_BILSEQ    number;
    vNBRLIGOUT_BILSEQ   number;
    vTAB_BILSEQ         pkg_funaff_bilan2.TableauCHAINE;

    v_chiffrescles                  t_tab_chiffrescles;

begin

    /*--------------------------------------------*/

    if pDEVISEIN is null then
        vDEVISEIN := 'SOURCE';
    else
        vDEVISEIN := pDEVISEIN;
    end if;
    if pUNITEIN  is null then
        vUNITEIN  := 'SOURCE';
    else
        vUNITEIN :=  pUNITEIN;
    end if;
    if (pNBRANNEE is null) or (pNBRANNEE = '') then
        Vnbrannee := -1;
    else
        Vnbrannee := pNBRANNEE;
    end if;

    dbms_output.put_line('-- avant pkg_funaff_bilan2.fun_aff_listebilan');
    declare
        vMESSAGE    varchar2(500);
    begin
        -- on va d'abord chercher les bons bilseq
        /*
        **  Tableau retourné :
        **      BILSEQ
        **      DATE DE CLOTURE
        **      Duree
        **      Type de bilan
        **      Origine du bilan		-- utilise pour trt des CCL (action E.Barillot)
        **      Sous-Origine du bilan	-- utilise pour trt des CCL (action E.Barillot)
        **      CRCONF					-- utilise pour trt des CCL (action E.Barillot)
        */
        ret := pkg_funaff_bilan2.fun_aff_listebilan (
            pMESSAGE          => pMESSAGE,
            pENTNUMTYP        => pENTNUMTYP,
            pENTNUM           => pENTNUM,
            pCLIPRE           => pCLIPRE,
            pCLIREF           => pCLIREF,
            pREDACTCOD        => '',
            pSERVICECOD       => '',
            pTYPBILCOD        => 'SCSS',
            pORIBILCOD        => 'COECRCCSBLIN',
            pETACOD           => '10',
            pVALCOD           => '89',
            pNBRANNEE         => pNBRANNEE,
            pLISTEANNEEBILAN  => '0',
            pTROU             => 'O',
            pNBRBILAN         => 3,   -- TODO à vérifier
            pNBBILOUT         => vNBBILOUT_BILSEQ,
            pNBRLIGOUT        => vNBRLIGOUT_BILSEQ,
            pTAB              => vTAB_BILSEQ,
            pORDRE_BILAN      => 0,   -- TODO à vérifier
            pACCES_CONF       => pACCES_CONF);
        if ret != 0 then
            pMESSAGE := vMESSAGE;
            return ret;
        end if;
    exception
        when others then
            raise;
    end;
    dbms_output.put_line('ret: '||ret);
    dbms_output.put_line('pMESSAGE: '||pMESSAGE);
    dbms_output.put_line('vNBBILOUT_BILSEQ: '||vNBBILOUT_BILSEQ);
    dbms_output.put_line('vNBRLIGOUT_BILSEQ: '||vNBRLIGOUT_BILSEQ);
    dbms_output.put_line('Liste bilans:');
    for i in 0..2 loop
        dbms_output.put_line('Bilan i: ' ||(i+1));
        declare
            j binary_integer := i*7;
        begin
            j := j+1; dbms_output.put_line('  BILSEQ               ['||j||']: '||vTAB_BILSEQ(j));
            j := j+1; dbms_output.put_line('  DATE DE CLOTURE      ['||j||']: '||vTAB_BILSEQ(j));
            j := j+1; dbms_output.put_line('  Duree                ['||j||']: '||vTAB_BILSEQ(j));
            j := j+1; dbms_output.put_line('  Type de bilan        ['||j||']: '||vTAB_BILSEQ(j));
            j := j+1; dbms_output.put_line('  Origine du bilan     ['||j||']: '||vTAB_BILSEQ(j));
            j := j+1; dbms_output.put_line('  Sous-Origine du bilan['||j||']: '||vTAB_BILSEQ(j));
            j := j+1; dbms_output.put_line('  CRCONF               ['||j||']: '||vTAB_BILSEQ(j));
        exception
            when others then
                dbms_output.put_line(sqlerrm(sqlcode));
                raise;
        end;
        --dbms_output.put_line('vTAB_BILSEQ('||i||'): '||vTAB_BILSEQ(i));
    end loop;
    dbms_output.put_line('-- apres pkg_funaff_bilan2.fun_aff_listebilan');

    -- initialisation en dehors de la boucle; indispensable
    v_chiffrescles := t_tab_chiffrescles();
    for ibil in 1..3 loop
        dbms_output.put_line('Bilan i: ' ||ibil);
        declare
            j               binary_integer := (ibil-1)*7;
            curs_bilan      sys_refcursor;
            v_bilseq        varchar2(20) := vTAB_BILSEQ(j+1);
            v_typbilcod     varchar2(20) := vTAB_BILSEQ(j+4);
            v_oribilcod     varchar2(20) := vTAB_BILSEQ(j+5);
            v_crconf        varchar2(20) := vTAB_BILSEQ(j+7);
            vv_chiffrescles  t_chiffrescles;
        begin
            dbms_output.put_line('j: ' ||j);
            curs_bilan := get_cursor_bilan(v_bilseq, v_typbilcod, v_oribilcod, v_crconf);
            dbms_output.put_line('ibil: ' ||ibil);
            vv_chiffrescles := fetch_bilan(curs_bilan);
            dbms_output.put_line('ibil: ' ||ibil);
            ouput_chiffrescles(vv_chiffrescles);
            close_refcur(curs_bilan);
            v_chiffrescles.extend();
            v_chiffrescles(ibil) := vv_chiffrescles;
        exception
            when others then
                pMESSAGE := sqlerrm(sqlcode);
                ret := sqlcode;
                dbms_output.put_line(pMESSAGE);
                raise;
        end;
    end loop;


    -- boucle sur le curseur qui parcourt la table des CCL
/*
    loop
        Vccldevisecod  := null;
        Vcclexpunm     := null;

        fetch c_chiffrescles
            into Vcclca,               Vccldateexe,                       Vcclres,              Vccldurexe,
                Vccldevisecod,                                           Vcclexpunm,           Vccldateexepre,   Vcclcaexport,
                Vcclresultatexploit,  Vcclrcai,                          Vcclfondspropres,     Vcclendettement,
                Vcclcaf,        Vcclmontantachats,  Vccldureeclients,    Vccldureefournisseurs,Vccleffectif,     Vccltypmoncod, Vcclsup, Vcclcrconf, Vcclcatramoncod;
        if c_chiffrescles%notfound then
            exit;
        end if;



        -- 19/07/2012 - J. BEDU - Ajout d'un paramètre pour n'extraire que x années de chiffres clés
        -- Comme les données sont triées par date, si on a dépassé le seuil, on quitte la fonction
        if (Vnbrannee > 0 and (to_number(to_char(to_date(Vccldateexe,pFORDATES),'YYYY')) <= (to_number(to_char(sysdate,'YYYY'))-Vnbrannee))) then
            exit;
        end if;

        --mise en forme type de CCL
        if Vcclsup ='MACRON' then
            if Vcclcrconf='OUI' then
                Vccltype :='CRCONF';
            else
                Vccltype :='CONF';
            end if;
        elsif Vcclsup ='EVAL' then
            if Vcclcrconf='OUI' then
                Vccltype :='EVALCRCONF';
            end if;
        else
            if Vcclcrconf='OUI' then
                Vccltype:='CRCONF';
            else
                if Vccltypmoncod='BILAN' then
                    Vccltype:='BILAN';
                elsif Vccltypmoncod='COMM' then
                    Vccltype:='COMM';
                else
                    Vccltype:=null;
                end if;
            end if;
        end if ;


        Vccllibtype := recuperelibelle('TYPCC',pLANCOD,Vccltype);

        --ok
        if (Vccldevisecod<>'300' and Vccldevisecod<>'EUR') then
            if Vcclca is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclca,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>'300',
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>VcclcaEUR,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclcaEUR := null;
            end if;
            if Vcclres is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclres,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>'300',
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>VcclresEUR,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    return ret;
                end if;
            else VcclresEUR := null;
            end if;
            if Vcclcaexport is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclcaexport,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>'300',
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>VcclcaexportEUR,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    return ret;
                end if;
            else VcclcaexportEUR := null;
            end if;
            if Vcclresultatexploit is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclresultatexploit,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>'300',
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>VcclresultatexploitEUR,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    return ret;
                end if;
            else VcclresultatexploitEUR := null;
            end if;
            if Vcclrcai is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclrcai,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>'300',
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>VcclrcaiEUR,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclrcaiEUR := null;
            end if;
            if Vcclfondspropres is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclfondspropres,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>'300',
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>VcclfondspropresEUR,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclfondspropresEUR := null;
            end if;
            if Vcclendettement is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclendettement,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>'300',
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>VcclendettementEUR,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclendettementEUR := null;
            end if;

            -- 12/03/12 - J. BEDU CAF en jours => Pas de conversion
            if Vcclmontantachats is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclmontantachats,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>'300',
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>VcclmontantachatsEUR,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclmontantachatsEUR := null;
            end if;
        else
            VcclcaEUR              := Vcclca;
            VcclresEUR             := Vcclres;
            VcclcaexportEUR	   := Vcclcaexport;
            VcclresultatexploitEUR := Vcclresultatexploit;
            VcclrcaiEUR            := Vcclrcai;
            VcclfondspropresEUR    := Vcclfondspropres;
            VcclendettementEUR     := Vcclendettement;
        --    VcclcafEUR             := Vcclcaf;
            VcclmontantachatsEUR   := Vcclmontantachats;
        end if;

        --ok
        if vDEVISEIN='SOURCE' or vDEVISEIN=Vccldevisecod then
            DeviseSaisie      := Vccldevisecod;
            DeviseRetour      := Vccldevisecod;
            CAretourne        := Vcclca;
            RNretourne        := Vcclres;
            CAexportretourne  := Vcclcaexport;
            RESexploitretourne:= Vcclresultatexploit;
            RCAIretourne      := Vcclrcai;
            FPretourne        := Vcclfondspropres;
            ENDETTretourne    := Vcclendettement;
    --      CAF2retourne      := Vcclcaf;
            MONTANTachatsretourne:= Vcclmontantachats;
        elsif vDEVISEIN='300' or vDEVISEIN='EUR' then
            DeviseSaisie := Vccldevisecod;
            DeviseRetour := '300';
            CAretourne   := VcclcaEUR;
            RNretourne   := VcclresEUR;
            CAexportretourne:= VcclcaexportEUR;
            RESexploitretourne:= VcclresultatexploitEUR;
            RCAIretourne:= VcclrcaiEUR;
            FPretourne := VcclfondspropresEUR;
            ENDETTretourne:= VcclendettementEUR;
    --      CAF2retourne:= VcclcafEUR;
            MONTANTachatsretourne:= VcclmontantachatsEUR;
        else
            DeviseSaisie := Vccldevisecod;
            DeviseRetour := vDEVISEIN;
            CAretourne   := null;
            RNretourne   := null;
            CAexportretourne:= null;
            RESexploitretourne:= null;
            RCAIretourne:= null;
            FPretourne := null;
            ENDETTretourne:= null;
    --        CAF2retourne:= NULL;
            MONTANTachatsretourne:= null;
            if Vcclca is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclca,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>vDEVISEIN,
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>CAretourne,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclcaEUR := null;
            end if;
            if Vcclres is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclres,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>vDEVISEIN,
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>RNretourne,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclresEUR := null;
            end if;
            if Vcclcaexport is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclcaexport,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>vDEVISEIN,
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>CAexportretourne,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclcaexportEUR := null;
            end if;
            if Vcclresultatexploit is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclresultatexploit,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>vDEVISEIN,
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>RESexploitretourne,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclresultatexploitEUR := null;
            end if;
            if Vcclrcai is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclrcai,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>vDEVISEIN,
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>RCAIretourne,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclrcaiEUR := null;
            end if;
            if Vcclfondspropres is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclfondspropres,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>vDEVISEIN,
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>FPretourne,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclfondspropresEUR := null;
            end if;
            if Vcclendettement is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclendettement,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>vDEVISEIN,
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>ENDETTretourne,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclendettementEUR := null;
            end if;
            -- 19/03/12 - J. BEDU - Capacité d'autofin. en jours, pas de conversion à effectuer
            -- if Vcclcaf is not null then
            --       ret := fun_conv_euro (
            -- 		    pORIMONTANT=>Vcclcaf,
            -- 		    pORIDEVISECOD=>Vccldevisecod,
            -- 		    pORIEXPUNM=>0,
            -- 		    pRESDEVISECOD=>vDEVISEIN,
            -- 		    pRESEXPUNM=>0,
            -- 		    pRESNBRDEC=>2,
            -- 		    pRESMONTANT=>VcclcafEUR,
            -- 		    pfonction_err=>fonction_err,
            -- 		    pmessage=>pMESSAGE);
            --     if ret<>0 then
            --       close c_chiffrescles;
            --         pNBRLIGOUT := 0;
            --         return ret;
            --       end if;
            --     else VcclcafEUR := NULL;
            --     end if;
            if Vcclmontantachats is not null then
                ret := fun_conv_euro (
                    pORIMONTANT=>Vcclmontantachats,
                    pORIDEVISECOD=>Vccldevisecod,
                    pORIEXPUNM=>0,
                    pRESDEVISECOD=>vDEVISEIN,
                    pRESEXPUNM=>0,
                    pRESNBRDEC=>0,
                    pRESMONTANT=>MONTANTachatsretourne,
                    pfonction_err=>fonction_err,
                    pmessage=>pMESSAGE);
                if ret<>0 then
                    close c_chiffrescles;
                    pNBRLIGOUT := 0;
                    return ret;
                end if;
            else VcclmontantachatsEUR := null;
            end if;
        end if;

        --ok
        if vUNITEIN='SOURCE' or vUNITEIN='0' then
            UniteSaisie := '0';
            UniteRetour := '0';
        elsif vUNITEIN<>'0' then
            UniteSaisie := '0';
            UniteRetour := vUNITEIN;
            CAretourne  := round(CAretourne/power(10,vUNITEIN));
            RNretourne  := round(RNretourne/power(10,vUNITEIN));
            CAexportretourne:= round(CAexportretourne/power(10,vUNITEIN));
            RESexploitretourne:= round(RESexploitretourne/power(10,vUNITEIN));
            RCAIretourne:= round(RCAIretourne/power(10,vUNITEIN));
            FPretourne := round(FPretourne/power(10,vUNITEIN));
            ENDETTretourne:= round(ENDETTretourne/power(10,vUNITEIN));
    --        CAF2retourne:= round(CAF2retourne/(10**vUNITEIN)); -- J. BEDU - 12/03/13 - CAF en jours dans la BDD
            MONTANTachatsretourne:= round(MONTANTachatsretourne/power(10,vUNITEIN));
        end if;




        pTAB(i):=CAretourne;  */
/*i=1,6,11*//*
    i:=i+1;
        pTAB(i):=Vccldateexe; */
/*i=2,7,12*//*
    i:=i+1;
        pTAB(i):=RNretourne;  */
/*i=3,8,13*//*
    i:=i+1;
        pTAB(i):=Vccldateexe; */
/*i=4,9,14*//*
    i:=i+1;
        pTAB(i):=Vccldurexe;  */
/*i=5,10,15*//*
   i:=i+1;

        compteur := compteur+1;
        if compteur=1 then
            VDernierDeviseSaisie         := DeviseSaisie;
            VDernierDeviseRetour         := DeviseRetour;
            VDernierUniteSaisie          := UniteSaisie;
            VDernierUniteRetour          := UniteRetour;
            VDernierprecdate             := Vccldateexepre;
            DernierCA                    := VcclcaEUR;
            DernierRes                   := VcclresEUR;
            -- J. BEDU - 12/03 - On stocke les montant en euros pour calculer le %
            VDerniercclcaexport          := VcclcaexportEUR;
            VDerniercclresultatexploit   := VcclresultatexploitEUR;
            VDerniercclrcai              := VcclrcaiEUR;
            VDerniercclfondspropres      := VcclfondspropresEUR;
            VDerniercclendettement       := VcclendettementEUR;
            VDerniercclcaf               := Vcclcaf;
            VDerniercclmontantachats     := VcclmontantachatsEUR;
            VDernierccldureeclients      := Vccldureeclients;
            VDernierccldureefournisseurs := Vccldureefournisseurs;
            -- J. BEDU - 12/°3 - On stocke aussi les montants à retourner
            VDernierCAexportretourne     := CAexportretourne;
            VDernierRESexploitretourne   := RESexploitretourne;
            VDernierRCAIretourne         := RCAIretourne;
            VDernierFPretourne           := FPretourne;
            VDernierENDETTretourne       := ENDETTretourne;
            VDernierMONTANTachatsretourne:= MONTANTachatsretourne;
            VDernierccleffectif          := Vccleffectif;
            VDerniereProvenance          := Vccltypmoncod;
            VDernierType                 := Vccltype;
            VDernierlibType              := Vccllibtype;
            VDerniercclcatramoncod       := Vcclcatramoncod;

        elsif compteur=2 then
            VAvDernierDeviseSaisie         := DeviseSaisie;
            VAvDernierDeviseRetour         := DeviseRetour;
            VAvDernierUniteSaisie          := UniteSaisie;
            VAvDernierUniteRetour          := UniteRetour;
            VAvDernierprecdate             := Vccldateexepre;
            AvDernierCA                    := VcclcaEUR;
            AvDernierRes                   := VcclresEUR;
            VAvDerniercclcaexport          := VcclcaexportEUR;
            VAvDerniercclresultatexploit   := VcclresultatexploitEUR;
            VAvDerniercclrcai              := VcclrcaiEUR;
            VAvDerniercclfondspropres      := VcclfondspropresEUR;
            VAvDerniercclendettement       := VcclendettementEUR;
            VAvDerniercclcaf               := Vcclcaf;
            VAvDerniercclmontantachats     := VcclmontantachatsEUR;
            VAvDernierccldureeclients      := Vccldureeclients;
            VAvDernierccldureefournisseurs := Vccldureefournisseurs;
            VAvDernierCAexportretourne     := CAexportretourne;
            VAvDernierRESexploitretourne   := RESexploitretourne;
            VAvDernierRCAIretourne         := RCAIretourne;
            VAvDernierFPretourne           := FPretourne;
            VAvDernierENDETTretourne       := ENDETTretourne;
            VAvDernierMONTANTachatsretour  := MONTANTachatsretourne;
            VAvDernierccleffectif          := Vccleffectif;
            VAvDerniereProvenance          := Vccltypmoncod;
            VAvDernierType                 := Vccltype;
            VAvDernierlibType              := Vccllibtype;
            VAvDerniercclcatramoncod       := Vcclcatramoncod;

        elsif compteur=3 then
            VAnteDeviseSaisie              := DeviseSaisie;
            VAnteDeviseRetour              := DeviseRetour;
            VAnteUniteSaisie               := UniteSaisie;
            VAnteUniteRetour               := UniteRetour;
            VAnteprecdate                  := Vccldateexepre;
            AnteCA                         := VcclcaEUR;
            AnteRes                        := VcclresEUR;
            VAntecclcaexport               := VcclcaexportEUR;
            VAntecclresultatexploit        := VcclresultatexploitEUR;
            VAntecclrcai                   := VcclrcaiEUR;
            VAntecclfondspropres           := VcclfondspropresEUR;
            VAntecclendettement            := VcclendettementEUR;
            VAntecclcaf                    := Vcclcaf;
            VAntecclmontantachats          := VcclmontantachatsEUR;
            VAnteccldureeclients           := Vccldureeclients;
            VAnteccldureefournisseurs      := Vccldureefournisseurs;
            VAnteCAexportretourne          := CAexportretourne;
            VAnteRESexploitretourne        := RESexploitretourne;
            VAnteRCAIretourne              := RCAIretourne;
            VAnteFPretourne                := FPretourne;
            VAnteENDETTretourne            := ENDETTretourne;
            VAnteMONTANTachatsretourne     := MONTANTachatsretourne;
            VAnteccleffectif               := Vccleffectif;
            VAnteProvenance                := Vccltypmoncod;
            VAnteType                      := Vccltype;
            VAntelibType                   := Vccllibtype;
            VAntecclcatramoncod            := Vcclcatramoncod;
        end if;
        exit when compteur=3;
    end loop;

    close c_chiffrescles;
*/


/*
    if (compteur < 3) then
        loop
            pTAB(i):=null; */
/*i=1, 6,11*//*
 i:=i+1;
            pTAB(i):=null; */
/*i=2, 7,12*//*
 i:=i+1;
            pTAB(i):=null; */
/*i=3, 8,13*//*
 i:=i+1;
            pTAB(i):=null; */
/*i=4, 9,14*//*
 i:=i+1;
            pTAB(i):=null; */
/*i=5,10,15*//*
 i:=i+1;

            compteur:=compteur+1;

            exit when compteur=3;
        end loop;
    end if;
    --i=16
    if DernierCA is null or AvDernierCA is null or
        DernierCA = 0 or AvDernierCA = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((DernierCA-AvDernierCA)/abs(AvDernierCA))*100;
        pTAB(i):=pourcent;  i:=i+1;
    end if;
    --i=17
    if AvDernierCA is null or AnteCA is null or
        AvDernierCA = 0 or AnteCA = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((AvDernierCA-AnteCA)/abs(AnteCA))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=18
    if DernierRes is null or AvDernierRes is null or
        DernierRes = 0 or AvDernierRes = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((DernierRes-AvDernierRes)/abs(AvDernierRes))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=19
    if AvDernierRes is null or AnteRes is null or
        AvDernierRes = 0 or AnteRes = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((AvDernierRes-AnteRes)/abs(AnteRes))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=20
    if pLIBELLE = 'O' then
        VLibDernierdeviseSaisie    := recuperelibelle('DEVISE',pLANCOD,VDernierDeviseSaisie);
        VLibAvDernierdeviseSaisie  := recuperelibelle('DEVISE',pLANCOD,VAvDernierDeviseSaisie);
        VLibAnteDeviseSaisie       := recuperelibelle('DEVISE',pLANCOD,VAnteDeviseSaisie);
        VLibDernierDeviseRetour    := recuperelibelle('DEVISE',pLANCOD,VDernierDeviseRetour);
        VLibAvDernierDeviseRetour  := recuperelibelle('DEVISE',pLANCOD,VAvDernierDeviseRetour);
        VLibAnteDeviseRetour       := recuperelibelle('DEVISE',pLANCOD,VAnteDeviseRetour);
    end if;


    pTAB(i):=VDernierprecdate;             i:=i+1; --i=21
    pTAB(i):=VDernierDeviseSaisie;         i:=i+1; --i=22
    pTAB(i):=VlibDernierDeviseSaisie;      i:=i+1; --i=23
    pTAB(i):=VDernierUniteSaisie;          i:=i+1; --i=24
    pTAB(i):=VDernierDeviseRetour;         i:=i+1; --i=25
    pTAB(i):=VlibDernierDeviseRetour;      i:=i+1; --i=26
    pTAB(i):=VDernierUniteRetour;          i:=i+1; --i=27
    pTAB(i):=VAvDernierprecdate;           i:=i+1; --i=28
    pTAB(i):=VAvDernierDeviseSaisie;       i:=i+1; --i=29
    pTAB(i):=VlibAvDernierDeviseSaisie;    i:=i+1; --i=30
    pTAB(i):=VAvDernierUniteSaisie;        i:=i+1; --i=31
    pTAB(i):=VAvDernierDeviseRetour;       i:=i+1; --i=32
    pTAB(i):=VlibAvDernierDeviseRetour;    i:=i+1; --i=33
    pTAB(i):=VAvDernierUniteRetour;        i:=i+1; --i=34

    pTAB(i):=VAnteprecdate;                i:=i+1; --i=35
    pTAB(i):=VAnteDeviseSaisie;            i:=i+1; --i=36
    pTAB(i):=VlibAnteDeviseSaisie;         i:=i+1; --i=37
    pTAB(i):=VAnteUniteSaisie;             i:=i+1; --i=38
    pTAB(i):=VAnteDeviseRetour;            i:=i+1; --i=39
    pTAB(i):=VlibAnteDeviseRetour;         i:=i+1; --i=40
    pTAB(i):=VAnteUniteRetour;             i:=i+1; --i=41

    -- Ajout 18/11/2011


    --i=41
    if VDerniercclcaexport is null or VAvDerniercclcaexport is null or
        VDerniercclcaexport = 0 or VAvDerniercclcaexport = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VDerniercclcaexport-VAvDerniercclcaexport)/abs(VAvDerniercclcaexport))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=42
    if VAvDerniercclcaexport is null or VAntecclcaexport is null or
        VAvDerniercclcaexport = 0 or VAntecclcaexport = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VAvDerniercclcaexport-VAntecclcaexport)/abs(VAntecclcaexport))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=43
    if VDerniercclresultatexploit is null or VAvDerniercclresultatexploit is null or
        VDerniercclresultatexploit = 0 or VAvDerniercclresultatexploit = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VDerniercclresultatexploit-VAvDerniercclresultatexploit)/abs(VAvDerniercclresultatexploit))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=44
    if VAvDerniercclresultatexploit is null or VAntecclresultatexploit is null or
        VAvDerniercclresultatexploit = 0 or VAntecclresultatexploit = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VAvDerniercclresultatexploit-VAntecclresultatexploit)/abs(VAntecclresultatexploit))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;

    --i=45
    if VDerniercclrcai is null or VAvDerniercclrcai is null or
        VDerniercclrcai = 0 or VAvDerniercclrcai = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VDerniercclrcai-VAvDerniercclrcai)/abs(VAvDerniercclrcai))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=46
    if VAvDerniercclrcai is null or VAntecclrcai is null or
        VAvDerniercclrcai = 0 or VAntecclrcai = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VAvDerniercclrcai-VAntecclrcai)/abs(VAntecclrcai))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=47
    if VDerniercclfondspropres is null or VAvDerniercclfondspropres is null or
        VDerniercclfondspropres = 0 or VAvDerniercclfondspropres = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VDerniercclfondspropres-VAvDerniercclfondspropres)/abs(VAvDerniercclfondspropres))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=48
    if VAvDerniercclfondspropres is null or VAntecclfondspropres is null or
        VAvDerniercclfondspropres = 0 or VAntecclfondspropres = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VAvDerniercclfondspropres-VAntecclfondspropres)/abs(VAntecclfondspropres))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=49
    if VDerniercclendettement is null or VAvDerniercclendettement is null or
        VDerniercclendettement = 0 or VAvDerniercclendettement = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VDerniercclendettement-VAvDerniercclendettement)/abs(VAvDerniercclendettement))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=50
    if VAvDerniercclendettement is null or VAntecclendettement is null or
        VAvDerniercclendettement = 0 or VAntecclendettement = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VAvDerniercclendettement-VAntecclendettement)/abs(VAntecclendettement))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=51
    if VDerniercclcaf is null or VAvDerniercclcaf is null or
        VDerniercclcaf = 0 or VAvDerniercclcaf = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VDerniercclcaf-VAvDerniercclcaf)/abs(VAvDerniercclcaf))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=52
    if VAvDerniercclcaf is null or VAntecclcaf is null or
        VAvDerniercclcaf = 0 or VAntecclcaf = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VAvDerniercclcaf-VAntecclcaf)/abs(VAntecclcaf))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=53
    if VDerniercclmontantachats is null or VAvDerniercclmontantachats is null or
        VDerniercclmontantachats = 0 or VAvDerniercclmontantachats = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VDerniercclmontantachats-VAvDerniercclmontantachats)/abs(VAvDerniercclmontantachats))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;
    --i=54
    if VAvDerniercclmontantachats is null or VAntecclmontantachats is null or
        VAvDerniercclmontantachats = 0 or VAntecclmontantachats = 0 then
        pTAB(i):=null; i:=i+1;
    else
        pourcent:=((VAvDerniercclmontantachats-VAntecclmontantachats)/abs(VAntecclmontantachats))*100;
        pTAB(i):=pourcent; i:=i+1;
    end if;

    pTAB(i):=VDernierCAexportretourne;       i:=i+1; --i=55
    pTAB(i):=VDernierRESexploitretourne;     i:=i+1; --i=56
    pTAB(i):=VDernierRCAIretourne;           i:=i+1; --i=57
    pTAB(i):=VDernierFPretourne;             i:=i+1; --i=58
    pTAB(i):=VDernierENDETTretourne;         i:=i+1; --i=59
    pTAB(i):=VDerniercclcaf;                 i:=i+1; --i=60
    pTAB(i):=VDernierMONTANTachatsretourne;  i:=i+1; --i=61
    pTAB(i):=VDernierccldureeclients;        i:=i+1; --i=62
    pTAB(i):=VDernierccldureefournisseurs;   i:=i+1; --i=63
    pTAB(i):=VDernierccleffectif;            i:=i+1; --i=64

    pTAB(i):=VAvDernierCAexportretourne;     i:=i+1; --i=65
    pTAB(i):=VAvDernierRESexploitretourne;   i:=i+1; --i=66
    pTAB(i):=VAvDernierRCAIretourne;         i:=i+1; --i=67
    pTAB(i):=VAvDernierFPretourne;           i:=i+1; --i=68
    pTAB(i):=VAvDernierENDETTretourne;       i:=i+1; --i=69
    pTAB(i):=VAvDerniercclcaf;               i:=i+1; --i=70
    pTAB(i):=VAvDernierMONTANTachatsretour;  i:=i+1; --i=71
    pTAB(i):=VAvDernierccldureeclients;      i:=i+1; --i=72
    pTAB(i):=VAvDernierccldureefournisseurs; i:=i+1; --i=73
    pTAB(i):=VAvDernierccleffectif;          i:=i+1; --i=74

    pTAB(i):=VAnteCAexportretourne;          i:=i+1; --i=75
    pTAB(i):=VAnteRESexploitretourne;        i:=i+1; --i=76
    pTAB(i):=VAnteRCAIretourne;              i:=i+1; --i=77
    pTAB(i):=VAnteFPretourne;                i:=i+1; --i=78
    pTAB(i):=VAnteENDETTretourne;            i:=i+1; --i=79
    pTAB(i):=VAntecclcaf;                    i:=i+1; --i=80
    pTAB(i):=VAnteMONTANTachatsretourne;     i:=i+1; --i=81
    pTAB(i):=VAnteccldureeclients;           i:=i+1; --i=82
    pTAB(i):=VAnteccldureefournisseurs;      i:=i+1; --i=83
    pTAB(i):=VAnteccleffectif;               i:=i+1; --i=84

    pTAB(i):=VDerniereProvenance;            i:=i+1; --i=85
    pTAB(i):=VAvDerniereProvenance;          i:=i+1; --i=86
    pTAB(i):=VAnteProvenance;                i:=i+1; --i=87
    pTAB(i):=VDernierType;                   i:=i+1; --i=88
    pTAB(i):=VAvDernierType;                 i:=i+1; --i=89
    pTAB(i):=VAnteType;                      i:=i+1; --i=90
    pTAB(i):=VDernierlibType;                   i:=i+1; --i=91
    pTAB(i):=VAvDernierlibType;                 i:=i+1; --i=92
    pTAB(i):=VAntelibType;                      i:=i+1; --i=93


    pTAB(i):=VDerniercclcatramoncod;         i:=i+1; --i=94
    pTAB(i):=VAvDerniercclcatramoncod;       i:=i+1; --i=95
    pTAB(i):=VAntecclcatramoncod;            i:=i+1; --i=96

    --if pLIBELLE = 'O' then
    VLibDerniercclcatramoncod    := recuperelibelle('TRACA',pLANCOD,VDerniercclcatramoncod);
    VLibAvDerniercclcatramoncod  := recuperelibelle('TRACA',pLANCOD,VAvDerniercclcatramoncod);
    VLibAntecclcatramoncod       := recuperelibelle('TRACA',pLANCOD,VAntecclcatramoncod);
    --end if;

    pTAB(i):=VLibDerniercclcatramoncod;     i:=i+1; --i=97
    pTAB(i):=VLibAvDerniercclcatramoncod;   i:=i+1; --i=98
    pTAB(i):=VLibAntecclcatramoncod;        i:=i+1; --i=99

    pNBRLIGOUT:=i-1;
*/
    return 0;

exception
    when NO_DATA_FOUND then
        if c_chiffrescles%isopen then
            close c_chiffrescles;
        end if;

        pNBRLIGOUT:=0;
        return 0;
    when others then
        if c_chiffrescles%isopen then
            close c_chiffrescles;
        end if;

        pNBRLIGOUT := 0;
        pMESSAGE := sqlerrm(sqlcode);
        return sqlcode;
 
end fun_aff_3bilseqCC;

/************************************************************************************/


end pkg_funaff_chiffrescles ;
/

-- </sqlToIntegrate>
show error
