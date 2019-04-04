set serveroutput on

declare
    res         number := 0;
    pMESSAGE    VARCHAR2(500);
    pNBBILOUT   NUMBER;
    pNBRLIGOUT  NUMBER;
    pTAB        pkg_funaff_bilan2.TableauCHAINE;
begin
    res := pkg_funaff_bilan2.fun_aff_listebilan(
                       pMESSAGE,            --        pMESSAGE              OUT VARCHAR2,
                       0,                   --        pENTNUMTYP         IN     NUMBER,
                       '482755741',         --        pENTNUM            IN     VARCHAR2,
                       '',                  --        pCLIPRE            IN     VARCHAR2 DEFAULT '',
                       '',                  --        pCLIREF            IN     VARCHAR2 DEFAULT '',
                       '',                  --        pREDACTCOD         IN     VARCHAR2 DEFAULT '',
                       '',                  --        pSERVICECOD        IN     VARCHAR2 DEFAULT '',
                       'SCSS',              --        pTYPBILCOD         IN     VARCHAR2 DEFAULT 'SCSS',
                       'INBL',              --        pORIBILCOD         IN     VARCHAR2 DEFAULT 'INBL',
                       '10',                --        pETACOD            IN     VARCHAR2 DEFAULT '10',
                       '89',                --        pVALCOD            IN     VARCHAR2 DEFAULT '89',
                       -1,                  --         pNBRANNEE          IN     NUMBER DEFAULT -1,
                       '0',                 --        pLISTEANNEEBILAN   IN     VARCHAR2 DEFAULT '0',
                       'O',                 --        pTROU              IN     VARCHAR2 DEFAULT 'O',
                       1,                   --        pNBRBILAN          IN     NUMBER DEFAULT 1,
                       pNBBILOUT,           --        pNBBILOUT             OUT NUMBER,
                       pNBRLIGOUT,          --        pNBRLIGOUT            OUT NUMBER,
                       pTAB,                --        pTAB                  OUT TableauCHAINE,
                       0,                   --        pORDRE_BILAN       IN     NUMBER DEFAULT 0,
                       'N'                  --        pACCES_CONF        IN     VARCHAR2 DEFAULT 'N')
                   );
    for i in pTAB.first .. pTAB.last loop
        dbms_output.put_line(pTAB(i));
    end loop;
end;
/
show errors