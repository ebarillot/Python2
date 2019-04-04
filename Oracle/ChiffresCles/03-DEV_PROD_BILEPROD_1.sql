
SELECT entrcs,
    TO_CHAR (BILSEQ),
    TO_CHAR (BILDATCLO, 'DD/MM/YYYY'),
    TO_CHAR (BILDUREE),
    TYPBILCOD,
    ORIBILCOD,
    SSORIBILCOD,
    CRCONF
FROM BILAN
WHERE    (MOD (INSTR ('10', etacod), 2) = 1)
     AND  entrcs = '482755741'
     AND (INSTR ('89', valcod) != 0)
     AND (MOD (INSTR ('SCSS', typbilcod), 2) = 1)
     AND (MOD (INSTR ('INBL', oribilcod), 2) = 1)
ORDER BY BILDATCLO DESC, DECODE (MOD (INSTR ('INBL', ORIBILCOD), 2), 1, INSTR('INBL', ORIBILCOD), 9999);
