#coding: Utf8
from time import ctime
dico={
    12:['douze','midi'],
    0:['zéro','minuit'],
    1:'une',2:'deux',3:'trois',4:'quatre',5:'cinq',6:'six',7:'sept',8:'huit',
9:'neuf',10:'dix',11:'onze',13:'treize',14:'quatorze',
15:'quinze',16:'seize',17:'dix-sept',18:'dix-huit',19:'dix-neuf',20:'vingt',
30:'trente',40:'quarante',50:'cinquante'}

dico.update({20+k:'vingt-'+dico[k] for k in range(1,10)})
dico.update({30+k:'trente-'+dico[k] for k in range(1,10)})
dico.update({40+k:'quarante-'+dico[k] for k in range(1,10)})
dico.update({50+k:'cinquante-'+dico[k] for k in range(1,10)})
dico[21]='vingt-et-une'
dico[31]='trente-et-une'
dico[41]='quarante-et-une'
dico[51]='cinquante-et-une'  

x=ctime()
[jour,mois,date,heure,annee]=x.split()
 
#heure='12:14:14'  # pour les tests de validation 

[h,m,s]=heure.split(':')
h,m,s=int(h),int(m),int(s)
if h==0:
    print 'il est {:}'.format(dico[h][1])
elif h==12:
    print 'il est {:}'.format(dico[h][1])
elif h==1:
    print 'il est {:}'.format(dico[h]),"heure,",
else:
    print 'il est {:}'.format(dico[h]),"heures,",

if m==0:
    print '{:}'.format(dico[m][0]),'minute',
elif m==1:
    print '{:}'.format(dico[m]),'minute',
elif m==12:
    print '{:}'.format(dico[m][0]),'minutes',
else:
    print '{:}'.format(dico[m]),'minutes',
    
if s==0:
    print 'et {:}'.format(dico[s][0]),'seconde',
elif s==1:
    print 'et {:}'.format(dico[s]),'seconde',
elif s==12:
    print 'et {:}'.format(dico[s][0]),'secondes',
else:
    print 'et {:}'.format(dico[s]),'secondes',
        
 

