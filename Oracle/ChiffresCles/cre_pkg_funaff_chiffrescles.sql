set timing on
--alter session set nls_numeric_characters = '. ';
ALTER SESSION SET NLS_LANGUAGE='FRENCH';
ALTER SESSION SET NLS_TERRITORY='FRANCE';

--whenever SQLERROR exit 2 rollback
set echo on
set feedb on
show user

-- <sqlToIntegrate>

create or replace package pkg_funaff_chiffrescles is

/*
  Package qui contient les fonctions qui permettent de calculer à la volée les chiffres clés
  à partir des données des bilans.
*/


type TableauCHAINE is table of varchar2(500) index by binary_integer;

function get_ccltype(
    v_oribilcod varchar2,
    v_crconf varchar2
    )
return varchar2;

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
    pCLIPRE         in  varchar2,
    pCLIREF         in  varchar2
) return number;

end pkg_funaff_chiffrescles ;
/
show error



--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
create or replace package body pkg_funaff_chiffrescles is

--------------------------------------------------------------------------------

FUN_AFF_LISTEBILAN_CHUNK_SIZE constant number  := 4;

--------------------------------------------------------------------------------
type t_bilanmetadata is record (
    bilseq          number(8,0),
    typbilcod       varchar2(12),
    entrcs          varchar2(10),
    oribilcod       varchar2(12),
    unimoncod       varchar2(12),
    etacod          varchar2(12),
    valcod          varchar2(12),
    bildatclo       date,
    bilclopre       varchar2(3),
    bildatclon1     date,
    bilduree        number(2,0),
    sstypbilcod     varchar2(12),
    crconf          varchar2(12),
    ssoribilcod     varchar2(12),
    clipre          varchar2(16),
    cliref          varchar2(16)
);
type t_tab_bilanmetadata is table of t_bilanmetadata;


--------------------------------------------------------------------------------
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


--------------------------------------------------------------------------------
function get_bilan_metadata(pbilseq in number) return t_bilanmetadata is
    bilanmetadata   t_bilanmetadata;
begin
    select
        bilseq, typbilcod, entrcs, oribilcod, unimoncod, etacod, valcod, bildatclo, nvl(bilclopre, 'J'),
        bildatclon1, bilduree, sstypbilcod, crconf, ssoribilcod, clipre, cliref
    into bilanmetadata
    from BILAN
    where bilseq = pbilseq;
    return bilanmetadata;
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction get_bilan_metadata: ('||sqlcode||') - '||sqlerrm);
end;


--------------------------------------------------------------------------------
procedure dbms_ouput_bilanmetadata(v_bilanmetadata t_bilanmetadata) is
begin
    dbms_output.put_line('------------------------');
    dbms_output.put_line('bilseq         : '|| v_bilanmetadata.bilseq          ); --number(8,0),
    dbms_output.put_line('typbilcod      : '|| v_bilanmetadata.typbilcod       ); --varchar2(12),
    dbms_output.put_line('entrcs         : '|| v_bilanmetadata.entrcs          ); --varchar2(10),
    dbms_output.put_line('oribilcod      : '|| v_bilanmetadata.oribilcod       ); --varchar2(12),
    dbms_output.put_line('unimoncod      : '|| v_bilanmetadata.unimoncod       ); --varchar2(12),
    dbms_output.put_line('etacod         : '|| v_bilanmetadata.etacod          ); --varchar2(12),
    dbms_output.put_line('valcod         : '|| v_bilanmetadata.valcod          ); --varchar2(12),
    dbms_output.put_line('bildatclo      : '|| v_bilanmetadata.bildatclo       ); --date,
    dbms_output.put_line('bilclopre      : '|| v_bilanmetadata.bilclopre       ); --varchar2(3),
    dbms_output.put_line('bildatclon1    : '|| v_bilanmetadata.bildatclon1     ); --date,
    dbms_output.put_line('bilduree       : '|| v_bilanmetadata.bilduree        ); --number(2,0),
    dbms_output.put_line('sstypbilcod    : '|| v_bilanmetadata.sstypbilcod     ); --varchar2(12),
    dbms_output.put_line('crconf         : '|| v_bilanmetadata.crconf          ); --varchar2(12),
    dbms_output.put_line('ssoribilcod    : '|| v_bilanmetadata.ssoribilcod     ); --varchar2(12),
    dbms_output.put_line('clipre         : '|| v_bilanmetadata.clipre          ); --varchar2(16),
    dbms_output.put_line('cliref         : '|| v_bilanmetadata.cliref          ); --varchar2(16)
    dbms_output.put_line('------------------------');
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction dbms_ouput_chiffrescles: ('||sqlcode||') - '||sqlerrm);
end;


--------------------------------------------------------------------------------
procedure dbms_output_fun_aff_listebilan(
    ret                 number,
    pMESSAGE            varchar2,
    pNBBILOUT_BILSEQ    number,
    pNBRLIGOUT_BILSEQ   number,
    pTAB_BILSEQ         pkg_funaff_bilan2.TableauCHAINE) is
begin
    dbms_output.put_line('ret: '||ret);
    dbms_output.put_line('pMESSAGE: '||pMESSAGE);
    dbms_output.put_line('vNBBILOUT_BILSEQ: '||pNBBILOUT_BILSEQ);
    dbms_output.put_line('vNBRLIGOUT_BILSEQ: '||pNBRLIGOUT_BILSEQ);
    dbms_output.put_line('Liste bilans:');
    for ibil in 0..2 loop
        dbms_output.put_line('Bilan ibil: ' ||(ibil+1));
        declare
            j binary_integer := ibil*FUN_AFF_LISTEBILAN_CHUNK_SIZE;
        begin
            j := j+1; dbms_output.put_line('  BILSEQ               ['||j||']: '||pTAB_BILSEQ(j));
            j := j+1; dbms_output.put_line('  DATE DE CLOTURE      ['||j||']: '||pTAB_BILSEQ(j));
            j := j+1; dbms_output.put_line('  Duree                ['||j||']: '||pTAB_BILSEQ(j));
            j := j+1; dbms_output.put_line('  Type de bilan        ['||j||']: '||pTAB_BILSEQ(j));
--            j := j+1; dbms_output.put_line('  Origine du bilan     ['||j||']: '||pTAB_BILSEQ(j));
--            j := j+1; dbms_output.put_line('  Sous-Origine du bilan['||j||']: '||pTAB_BILSEQ(j));
--            j := j+1; dbms_output.put_line('  CRCONF               ['||j||']: '||pTAB_BILSEQ(j));
        exception
            when others then
                dbms_output.put_line(sqlerrm(sqlcode));
                raise;
        end;
        --dbms_output.put_line('pTAB_BILSEQ('||ibil||'): '||pTAB_BILSEQ(ibil));
    end loop;
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction dbms_output_fun_aff_listebilan : ('||sqlcode||') - '||sqlerrm);
end;


--------------------------------------------------------------------------------
procedure dbms_ouput_chiffrescles(v_chiffrescles t_chiffrescles) is
begin
    dbms_output.put_line('------------------------');
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
    dbms_output.put_line('------------------------');
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction dbms_ouput_chiffrescles: ('||sqlcode||') - '||sqlerrm);
end;


--------------------------------------------------------------------------------
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


--------------------------------------------------------------------------------
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
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction open_curs_SC: ('||sqlcode||') - '||sqlerrm);
end;


--------------------------------------------------------------------------------
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
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction open_curs_SC_EVAL: ('||sqlcode||') - '||sqlerrm);
end;


--------------------------------------------------------------------------------
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
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction open_curs_SS: ('||sqlcode||') - '||sqlerrm);
end;


--------------------------------------------------------------------------------
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
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction open_curs_SS_EVAL: ('||sqlcode||') - '||sqlerrm);
end;

--------------------------------------------------------------------------------
--
-- détermination de la bonne requête en fonction des caractéristiques
-- intrinsèques du bilan
--
--------------------------------------------------------------------------------
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
    return curs_bilan;
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction get_cursor_bilan: ('||sqlcode||') - '||sqlerrm);
end get_cursor_bilan;


--------------------------------------------------------------------------------
--
-- détermination de la bonne requête en fonction des choix de l'appelant
-- on retourne le curseur sur les données d'EVALuation si et seulement si
-- le parametre acces_eval est à OUI, ce qui indique le droit d'y accéder.
--
--------------------------------------------------------------------------------
function get_cursor_bilan(
    bilseq      number,
    typbilcod   varchar2,
    acces_eval  varchar2
)
return sys_refcursor
is
    curs_bilan sys_refcursor;
begin
    if typbilcod = 'SC' then
        if acces_eval = 'OUI' then
            curs_bilan := open_curs_SC_EVAL(bilseq);
        else
            curs_bilan := open_curs_SC(bilseq);
        end if;
    elsif typbilcod = 'SS' then
        if acces_eval = 'OUI' then
            curs_bilan := open_curs_SS_EVAL(bilseq);
        else
            curs_bilan := open_curs_SS(bilseq);
        end if;
    end if;
    return curs_bilan;
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction get_cursor_bilan: ('||sqlcode||') - '||sqlerrm);
end get_cursor_bilan;


--------------------------------------------------------------------------------
function fetch_bilan (
    p_refcur    in out SYS_REFCURSOR
)
return t_chiffrescles
is
    v_chiffrescles  t_chiffrescles;
begin
    fetch p_refcur into v_chiffrescles;
    return v_chiffrescles;
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction fetch_bilan: ('||sqlcode||') - '||sqlerrm);
end;


--------------------------------------------------------------------------------
procedure close_refcur (
    p_refcur    in out SYS_REFCURSOR
)
is
begin
    if p_refcur%isopen then
        close p_refcur;
    end if;
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction close_refcur: ('||sqlcode||') - '||sqlerrm);
end;


--------------------------------------------------------------------------------
function evol_percent(num2 number, num1 number) return number is
    ret number(18,2) := null;
begin
    if not (num2 is null or num1 is null or num2 = 0 or num1 = 0) then
        ret := ((num2-num1)/abs(num1))*100;
    end if;
    return ret;
exception
    when others then
        RAISE_APPLICATION_ERROR (20001,'Probleme dans la fonction evol_percent: ('||sqlcode||') - '||sqlerrm);
end;


--------------------------------------------------------------------------------
-- fonction interne pour calculer la valeur ccltype
--------------------------------------------------------------------------------
function get_ccltype(
    v_oribilcod varchar2,
    v_crconf varchar2
    )
return varchar2 is
    Vccltype        varchar2(12) := '';
    Vcclsup         varchar2(12) := '';
    Vcclcrconf      varchar2(12) := v_crconf;
begin

    if false then
    -----------------------------------------------------
    -- 1ere méthode
    -- Règles similaires à celles qui sont codées dans la FUN_TAB_CHIFFRESCLES dans laquelle
    -- CCLSUP est déterminé quand les CCL sont créés à partir des bilans.
    --
    -- génère Vccltype à partir des métadonnées dont on dispose sur le bilan:
    -- v_oribilcod
    -- v_crconf
    -- en déterminant au préalable
    -- Vcclsup, Vcclcrconf

    -- détermination de Vcclsup
    if v_oribilcod in ('EC', 'RC') then
        Vcclsup := 'MACRON';
    else
        if v_crconf = 'OUI' then
            Vcclsup := 'EVAL';
        else
            Vcclsup := '';
        end if;
    end if;

    -- mise en forme type de CCL
    -- à partir des valeurs intermédiaires juste calculées
    if Vcclsup = 'MACRON' then
        if Vcclcrconf = 'OUI' then
            Vccltype := 'CRCONF';
        else
            Vccltype := 'CONF';
        end if;
    elsif Vcclsup = 'EVAL' then
        if Vcclcrconf = 'OUI' then
            Vccltype := 'EVALCRCONF';
        end if;
    else
        if Vcclcrconf = 'OUI' then
            Vccltype := 'CRCONF';
        else
            Vccltype := 'BILAN';
        end if;
    end if;
    dbms_output.put_line('ccltype (1er calcul): '||Vccltype);
    end if;

    -----------------------------------------------------
    -- 2eme méthode
    -- mise en forme type de CCL
    -- à partir des metadonnées du bilan
    if v_oribilcod in ('EC', 'RC') then     -- CCLSUP = 'MACRON'
        if v_crconf = 'OUI' then
            Vccltype := 'CRCONF';
        else
            Vccltype := 'CONF';
        end if;
    elsif v_oribilcod not in ('EC', 'RC') and v_crconf = 'OUI' then -- CCLSUP = 'EVAL'
        Vccltype := 'EVALCRCONF';
    else
        if v_crconf = 'OUI' then
            Vccltype := 'CRCONF';
        else
            Vccltype := 'BILAN';
        end if;
    end if;
    dbms_output.put_line('ccltype (2eme calcul): '||Vccltype);

    return Vccltype;
end;

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
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
return number is
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
    ret                             number(10);
    itab                            binary_integer;
    compteur                        number(2)       := 0;

    Vnbrannee                       number(2);

    vUNITEIN                        varchar2(12)    := null;
    DeviseSaisie                    varchar2(12)    := '300';
    UniteSaisie                     varchar2(12)    := '0';
    DeviseRetour                    varchar2(12)    := '300';
    UniteRetour                     varchar2(12)    := null;
    CAretourne                      varchar2(15)    := null;
    RNretourne                      varchar2(15)    := null;

    Vccltypmoncod                   varchar2(12)    := 'BILAN'; -- tous les CCL retournés par cette fun proviennent d'un bilan
    Vccltype                        varchar2(12)    := null;
    Vccllibtype                     varchar2(500)   := null;

    CAexportretourne                number(15)      := null;
    RESexploitretourne              number(15)      := null;
    RCAIretourne                    number(15)      := null;
    FPretourne                      number(15)      := null;
    ENDETTretourne                  number(15)      := null;
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

    vNBBILOUT_BILSEQ                number          := 0;
    vNBRLIGOUT_BILSEQ               number          := 0;
    vTAB_BILSEQ                     pkg_funaff_bilan2.TableauCHAINE;

begin

    /*--------------------------------------------*/

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
        **      DATE DE CLOTURE au format DD/MM/YYYY
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
    dbms_output_fun_aff_listebilan(ret, pMESSAGE, vNBBILOUT_BILSEQ, vNBRLIGOUT_BILSEQ, vTAB_BILSEQ);
    dbms_output.put_line('-- apres pkg_funaff_bilan2.fun_aff_listebilan');

    -- initialisation en dehors de la boucle; indispensable
    itab := 1;
    compteur := 0;  -- nb de bilans effectifs utilisables
    for ibil in 1..vNBBILOUT_BILSEQ loop
        dbms_output.put_line('Bilan ibil: '||ibil);
        declare
            j                   binary_integer  := (ibil-1)*FUN_AFF_LISTEBILAN_CHUNK_SIZE;
            curs_bilan          sys_refcursor;
            v_bilseq            varchar2(20)    := vTAB_BILSEQ(j+1);
            v_bilanmetadata     t_bilanmetadata;
            v_chiffrescles      t_chiffrescles;
        begin
            dbms_output.put_line('j: ' ||j);
            v_bilanmetadata := get_bilan_metadata(v_bilseq);
            dbms_ouput_bilanmetadata(v_bilanmetadata);

            curs_bilan := get_cursor_bilan(v_bilseq, v_bilanmetadata.typbilcod, pACCES_EVAL);
            dbms_output.put_line('ibil: ' ||ibil);

            v_chiffrescles := fetch_bilan(curs_bilan);
            dbms_output.put_line('ibil: ' ||ibil);
            dbms_ouput_chiffrescles(v_chiffrescles);
            close_refcur(curs_bilan);

            -- 19/07/2012 - J. BEDU - Ajout d'un paramètre pour n'extraire que x années de chiffres clés
            -- Comme les données sont triées par date, si on a dépassé le seuil, on quitte la fonction
            if (Vnbrannee > 0 and (to_number(to_char(v_bilanmetadata.bildatclo,'YYYY')) <= (to_number(to_char(sysdate,'YYYY'))-Vnbrannee))) then
                exit;
            end if;


            Vccltype    := get_ccltype(v_bilanmetadata.oribilcod, v_bilanmetadata.crconf);
            Vccllibtype := recuperelibelle('TYPCC',pLANCOD,Vccltype);
            CAretourne              := v_chiffrescles.CA;
            RNretourne              := v_chiffrescles.resnet;
            CAexportretourne        := v_chiffrescles.caExport;
            RESexploitretourne      := v_chiffrescles.resExploit;
            RCAIretourne            := v_chiffrescles.rcai;
            FPretourne              := v_chiffrescles.fonds;
            ENDETTretourne          := v_chiffrescles.endette;
            MONTANTachatsretourne   := v_chiffrescles.monAchats;

            -- calcul des tranches de montant pour CA
            declare
                NomFct      fra2prod.CTL_ERR_ENT.FCTERR%type;
                NoErr       fra2prod.CTL_ERR_ENT.NOERR%type;
                Message     fra2prod.CTL_ERR_ENT.MESSAGE%type;
                TypeErr     fra2prod.CTL_ERR_ENT.TYPEERR%type;
            begin
                ret := fra2prod.pkg_funcol.FUN_COL_TRACAE(Vcclcatramoncod, v_chiffrescles.CA, NomFct, NoErr, Message, TypeErr);
                -- les erreurs applicatives sont sans importance => non blocantes
                -- on ne relève que les erreurs techniques Oracle notamment
            exception
                when others then
                    raise;
            end;

            if vUNITEIN = 'SOURCE' or vUNITEIN = '0' then
                UniteRetour := '0';
            elsif vUNITEIN<>'0' then
                UniteRetour             := vUNITEIN;
                CAretourne              := round(CAretourne/power(10,vUNITEIN));
                RNretourne              := round(RNretourne/power(10,vUNITEIN));
                CAexportretourne        := round(CAexportretourne/power(10,vUNITEIN));
                RESexploitretourne      := round(RESexploitretourne/power(10,vUNITEIN));
                RCAIretourne            := round(RCAIretourne/power(10,vUNITEIN));
                FPretourne              := round(FPretourne/power(10,vUNITEIN));
                ENDETTretourne          := round(ENDETTretourne/power(10,vUNITEIN));
                MONTANTachatsretourne   := round(MONTANTachatsretourne/power(10,vUNITEIN));
            end if;

            pTAB(itab) := CAretourne;
            --i=1,6,11
            itab:=itab+1;
            pTAB(itab) := to_char(v_bilanmetadata.bildatclo, pFORDATES);
            --i=2,7,12
            itab:=itab+1;
            pTAB(itab) := RNretourne;
            --i=3,8,13
            itab:=itab+1;
            pTAB(itab) := to_char(v_bilanmetadata.bildatclo, pFORDATES);
            --i=4,9,14
            itab:=itab+1;
            pTAB(itab) := v_bilanmetadata.bilduree;
            --i=5,10,15
            itab:=itab+1;

            compteur := compteur+1;
            if compteur = 1 then
                VDernierDeviseSaisie            := DeviseSaisie;
                VDernierDeviseRetour            := DeviseRetour;
                VDernierUniteSaisie             := UniteSaisie;
                VDernierUniteRetour             := UniteRetour;
                VDernierprecdate                := v_bilanmetadata.bilclopre;
                DernierCA                       := v_chiffrescles.CA;
                DernierRes                      := v_chiffrescles.resnet;
                -- J. BEDU - 12/03 - On stocke les montant en euros pour calculer le %
                VDerniercclcaexport             := v_chiffrescles.caExport;
                VDerniercclresultatexploit      := v_chiffrescles.resExploit;
                VDerniercclrcai                 := v_chiffrescles.rcai;
                VDerniercclfondspropres         := v_chiffrescles.fonds;
                VDerniercclendettement          := v_chiffrescles.endette;
                VDerniercclcaf                  := v_chiffrescles.caf;
                VDerniercclmontantachats        := v_chiffrescles.monAchats;
                VDernierccldureeclients         := v_chiffrescles.dureeCli;
                VDernierccldureefournisseurs    := v_chiffrescles.dureeFou;
                -- J. BEDU - 12/°3 - On stocke aussi les montants à retourner
                VDernierCAexportretourne        := CAexportretourne;
                VDernierRESexploitretourne      := RESexploitretourne;
                VDernierRCAIretourne            := RCAIretourne;
                VDernierFPretourne              := FPretourne;
                VDernierENDETTretourne          := ENDETTretourne;
                VDernierMONTANTachatsretourne   := MONTANTachatsretourne;
                VDernierccleffectif             := v_chiffrescles.effectif;
                VDerniereProvenance             := Vccltypmoncod;
                VDernierType                    := Vccltype;
                VDernierlibType                 := Vccllibtype;
                VDerniercclcatramoncod          := Vcclcatramoncod;

            elsif compteur = 2 then
                VAvDernierDeviseSaisie          := DeviseSaisie;
                VAvDernierDeviseRetour          := DeviseRetour;
                VAvDernierUniteSaisie           := UniteSaisie;
                VAvDernierUniteRetour           := UniteRetour;
                VAvDernierprecdate              := v_bilanmetadata.bilclopre;
                AvDernierCA                     := v_chiffrescles.CA;
                AvDernierRes                    := v_chiffrescles.resnet;
                VAvDerniercclcaexport           := v_chiffrescles.caExport;
                VAvDerniercclresultatexploit    := v_chiffrescles.resExploit;
                VAvDerniercclrcai               := v_chiffrescles.rcai;
                VAvDerniercclfondspropres       := v_chiffrescles.fonds;
                VAvDerniercclendettement        := v_chiffrescles.endette;
                VAvDerniercclcaf                := v_chiffrescles.caf;
                VAvDerniercclmontantachats      := v_chiffrescles.monAchats;
                VAvDernierccldureeclients       := v_chiffrescles.dureeCli;
                VAvDernierccldureefournisseurs  := v_chiffrescles.dureeFou;
                VAvDernierCAexportretourne      := CAexportretourne;
                VAvDernierRESexploitretourne    := RESexploitretourne;
                VAvDernierRCAIretourne          := RCAIretourne;
                VAvDernierFPretourne            := FPretourne;
                VAvDernierENDETTretourne        := ENDETTretourne;
                VAvDernierMONTANTachatsretour   := MONTANTachatsretourne;
                VAvDernierccleffectif           := v_chiffrescles.effectif;
                VAvDerniereProvenance           := Vccltypmoncod;
                VAvDernierType                  := Vccltype;
                VAvDernierlibType               := Vccllibtype;
                VAvDerniercclcatramoncod        := Vcclcatramoncod;

            elsif compteur = 3 then
                VAnteDeviseSaisie               := DeviseSaisie;
                VAnteDeviseRetour               := DeviseRetour;
                VAnteUniteSaisie                := UniteSaisie;
                VAnteUniteRetour                := UniteRetour;
                VAnteprecdate                   := v_bilanmetadata.bilclopre;
                AnteCA                          := v_chiffrescles.CA;
                AnteRes                         := v_chiffrescles.resnet;
                VAntecclcaexport                := v_chiffrescles.caExport;
                VAntecclresultatexploit         := v_chiffrescles.resExploit;
                VAntecclrcai                    := v_chiffrescles.rcai;
                VAntecclfondspropres            := v_chiffrescles.fonds;
                VAntecclendettement             := v_chiffrescles.endette;
                VAntecclcaf                     := v_chiffrescles.caf;
                VAntecclmontantachats           := v_chiffrescles.monAchats;
                VAnteccldureeclients            := v_chiffrescles.dureeCli;
                VAnteccldureefournisseurs       := v_chiffrescles.dureeFou;
                VAnteCAexportretourne           := CAexportretourne;
                VAnteRESexploitretourne         := RESexploitretourne;
                VAnteRCAIretourne               := RCAIretourne;
                VAnteFPretourne                 := FPretourne;
                VAnteENDETTretourne             := ENDETTretourne;
                VAnteMONTANTachatsretourne      := MONTANTachatsretourne;
                VAnteccleffectif                := v_chiffrescles.effectif;
                VAnteProvenance                 := Vccltypmoncod;
                VAnteType                       := Vccltype;
                VAntelibType                    := Vccllibtype;
                VAntecclcatramoncod             := Vcclcatramoncod;
            end if;
            exit when compteur=3;

        exception
            when others then
                close_refcur(curs_bilan);
                pMESSAGE := sqlerrm(sqlcode);
                ret := sqlcode;
                dbms_output.put_line(pMESSAGE);
                raise;
        end;
    end loop;

    -- on complete les exercices inexistants avec des null
    if (compteur < 3) then
        loop
            pTAB(itab) := null;
            --i=1, 6,11
            itab:=itab+1;
            pTAB(itab) := null;
            --i=2, 7,12
            itab:=itab+1;
            pTAB(itab) := null;
            --i=3, 8,13
            itab:=itab+1;
            pTAB(itab) := null;
            --i=4, 9,14
            itab:=itab+1;
            pTAB(itab) := null;
            --i=5,10,15
            itab:=itab+1;
            compteur := compteur+1;
            exit when compteur = 3;
        end loop;
    end if;

    --i=16
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => DernierCA, num1 => AvDernierCA);  itab:=itab+1;
    --i=17
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => AvDernierCA, num1 => AnteCA); itab:=itab+1;
    --i=18
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => DernierRes, num1 => AvDernierRes); itab:=itab+1;
    --i=19
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => AvDernierRes, num1 => AnteRes); itab:=itab+1;
    --i=20
    if pLIBELLE = 'O' then
        VLibDernierdeviseSaisie    := recuperelibelle('DEVISE',pLANCOD,VDernierDeviseSaisie);
        VLibAvDernierdeviseSaisie  := recuperelibelle('DEVISE',pLANCOD,VAvDernierDeviseSaisie);
        VLibAnteDeviseSaisie       := recuperelibelle('DEVISE',pLANCOD,VAnteDeviseSaisie);
        VLibDernierDeviseRetour    := recuperelibelle('DEVISE',pLANCOD,VDernierDeviseRetour);
        VLibAvDernierDeviseRetour  := recuperelibelle('DEVISE',pLANCOD,VAvDernierDeviseRetour);
        VLibAnteDeviseRetour       := recuperelibelle('DEVISE',pLANCOD,VAnteDeviseRetour);
    end if;


    pTAB(itab) := VDernierprecdate;             itab:=itab+1; --i=21
    pTAB(itab) := VDernierDeviseSaisie;         itab:=itab+1; --i=22
    pTAB(itab) := VlibDernierDeviseSaisie;      itab:=itab+1; --i=23
    pTAB(itab) := VDernierUniteSaisie;          itab:=itab+1; --i=24
    pTAB(itab) := VDernierDeviseRetour;         itab:=itab+1; --i=25
    pTAB(itab) := VlibDernierDeviseRetour;      itab:=itab+1; --i=26
    pTAB(itab) := VDernierUniteRetour;          itab:=itab+1; --i=27
    pTAB(itab) := VAvDernierprecdate;           itab:=itab+1; --i=28
    pTAB(itab) := VAvDernierDeviseSaisie;       itab:=itab+1; --i=29
    pTAB(itab) := VlibAvDernierDeviseSaisie;    itab:=itab+1; --i=30
    pTAB(itab) := VAvDernierUniteSaisie;        itab:=itab+1; --i=31
    pTAB(itab) := VAvDernierDeviseRetour;       itab:=itab+1; --i=32
    pTAB(itab) := VlibAvDernierDeviseRetour;    itab:=itab+1; --i=33
    pTAB(itab) := VAvDernierUniteRetour;        itab:=itab+1; --i=34

    pTAB(itab) := VAnteprecdate;                itab:=itab+1; --i=35
    pTAB(itab) := VAnteDeviseSaisie;            itab:=itab+1; --i=36
    pTAB(itab) := VlibAnteDeviseSaisie;         itab:=itab+1; --i=37
    pTAB(itab) := VAnteUniteSaisie;             itab:=itab+1; --i=38
    pTAB(itab) := VAnteDeviseRetour;            itab:=itab+1; --i=39
    pTAB(itab) := VlibAnteDeviseRetour;         itab:=itab+1; --i=40
    pTAB(itab) := VAnteUniteRetour;             itab:=itab+1; --i=41

    -- les pourcentages d'évolution
    --i=41
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VDerniercclcaexport, num1 => VAvDerniercclcaexport);  itab:=itab+1;
    --i=42
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VAvDerniercclcaexport, num1 => VAntecclcaexport);  itab:=itab+1;
    --i=43
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VDerniercclresultatexploit, num1 => VAvDerniercclresultatexploit);  itab:=itab+1;
    --i=44
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VAvDerniercclresultatexploit, num1 => VAntecclresultatexploit);  itab:=itab+1;
    --i=45
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VDerniercclrcai, num1 => VAvDerniercclrcai);  itab:=itab+1;
    --i=46
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VAvDerniercclrcai, num1 => VAntecclrcai);  itab:=itab+1;
    --i=47
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VDerniercclfondspropres, num1 => VAvDerniercclfondspropres);  itab:=itab+1;
    --i=48
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VAvDerniercclfondspropres, num1 => VAntecclfondspropres);  itab:=itab+1;
    --i=49
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VDerniercclendettement, num1 => VAvDerniercclendettement);  itab:=itab+1;
    --i=50
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VAvDerniercclendettement, num1 => VAntecclendettement);  itab:=itab+1;
    --i=51
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VDerniercclcaf, num1 => VAvDerniercclcaf);  itab:=itab+1;
    --i=52
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VAvDerniercclcaf, num1 => VAntecclcaf);  itab:=itab+1;
    --i=53
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VDerniercclmontantachats, num1 => VAvDerniercclmontantachats);  itab:=itab+1;
    --i=54
    pragma inline(evol_percent, 'YES');
    pTAB(itab) := evol_percent(num2 => VAvDerniercclmontantachats, num1 => VAntecclmontantachats);  itab:=itab+1;
    --
    pTAB(itab) := VDernierCAexportretourne;       itab:=itab+1; --i=55
    pTAB(itab) := VDernierRESexploitretourne;     itab:=itab+1; --i=56
    pTAB(itab) := VDernierRCAIretourne;           itab:=itab+1; --i=57
    pTAB(itab) := VDernierFPretourne;             itab:=itab+1; --i=58
    pTAB(itab) := VDernierENDETTretourne;         itab:=itab+1; --i=59
    pTAB(itab) := VDerniercclcaf;                 itab:=itab+1; --i=60
    pTAB(itab) := VDernierMONTANTachatsretourne;  itab:=itab+1; --i=61
    pTAB(itab) := VDernierccldureeclients;        itab:=itab+1; --i=62
    pTAB(itab) := VDernierccldureefournisseurs;   itab:=itab+1; --i=63
    pTAB(itab) := VDernierccleffectif;            itab:=itab+1; --i=64

    pTAB(itab) := VAvDernierCAexportretourne;     itab:=itab+1; --i=65
    pTAB(itab) := VAvDernierRESexploitretourne;   itab:=itab+1; --i=66
    pTAB(itab) := VAvDernierRCAIretourne;         itab:=itab+1; --i=67
    pTAB(itab) := VAvDernierFPretourne;           itab:=itab+1; --i=68
    pTAB(itab) := VAvDernierENDETTretourne;       itab:=itab+1; --i=69
    pTAB(itab) := VAvDerniercclcaf;               itab:=itab+1; --i=70
    pTAB(itab) := VAvDernierMONTANTachatsretour;  itab:=itab+1; --i=71
    pTAB(itab) := VAvDernierccldureeclients;      itab:=itab+1; --i=72
    pTAB(itab) := VAvDernierccldureefournisseurs; itab:=itab+1; --i=73
    pTAB(itab) := VAvDernierccleffectif;          itab:=itab+1; --i=74

    pTAB(itab) := VAnteCAexportretourne;          itab:=itab+1; --i=75
    pTAB(itab) := VAnteRESexploitretourne;        itab:=itab+1; --i=76
    pTAB(itab) := VAnteRCAIretourne;              itab:=itab+1; --i=77
    pTAB(itab) := VAnteFPretourne;                itab:=itab+1; --i=78
    pTAB(itab) := VAnteENDETTretourne;            itab:=itab+1; --i=79
    pTAB(itab) := VAntecclcaf;                    itab:=itab+1; --i=80
    pTAB(itab) := VAnteMONTANTachatsretourne;     itab:=itab+1; --i=81
    pTAB(itab) := VAnteccldureeclients;           itab:=itab+1; --i=82
    pTAB(itab) := VAnteccldureefournisseurs;      itab:=itab+1; --i=83
    pTAB(itab) := VAnteccleffectif;               itab:=itab+1; --i=84

    pTAB(itab) := VDerniereProvenance;            itab:=itab+1; --i=85
    pTAB(itab) := VAvDerniereProvenance;          itab:=itab+1; --i=86
    pTAB(itab) := VAnteProvenance;                itab:=itab+1; --i=87
    pTAB(itab) := VDernierType;                   itab:=itab+1; --i=88
    pTAB(itab) := VAvDernierType;                 itab:=itab+1; --i=89
    pTAB(itab) := VAnteType;                      itab:=itab+1; --i=90
    pTAB(itab) := VDernierlibType;                itab:=itab+1; --i=91
    pTAB(itab) := VAvDernierlibType;              itab:=itab+1; --i=92
    pTAB(itab) := VAntelibType;                   itab:=itab+1; --i=93


    pTAB(itab) := VDerniercclcatramoncod;         itab:=itab+1; --i=94
    pTAB(itab) := VAvDerniercclcatramoncod;       itab:=itab+1; --i=95
    pTAB(itab) := VAntecclcatramoncod;            itab:=itab+1; --i=96

    --if pLIBELLE = 'O' then
    VLibDerniercclcatramoncod    := recuperelibelle('TRACA',pLANCOD,VDerniercclcatramoncod);
    VLibAvDerniercclcatramoncod  := recuperelibelle('TRACA',pLANCOD,VAvDerniercclcatramoncod);
    VLibAntecclcatramoncod       := recuperelibelle('TRACA',pLANCOD,VAntecclcatramoncod);
    --end if;

    pTAB(itab) := VLibDerniercclcatramoncod;      itab:=itab+1; --i=97
    pTAB(itab) := VLibAvDerniercclcatramoncod;    itab:=itab+1; --i=98
    pTAB(itab) := VLibAntecclcatramoncod;         itab:=itab+1; --i=99

    pNBRLIGOUT := itab-1;
    ------------------------------
    return 0;

exception
    when NO_DATA_FOUND then
        pNBRLIGOUT := 0;
        return 0;
    when others then
        pNBRLIGOUT := 0;
        pMESSAGE := sqlerrm(sqlcode);
        return sqlcode;
 
end fun_aff_3bilseqCC;

/************************************************************************************/


end pkg_funaff_chiffrescles ;
/

-- </sqlToIntegrate>
show error
