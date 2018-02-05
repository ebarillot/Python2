Jeu de la vie avec tkinter--------------------------
Url     : http://codes-sources.commentcamarche.net/source/49177-jeu-de-la-vie-avec-tkinterAuteur  : dia100dalyDate    : 24/08/2013
Licence :
=========

Ce document intitulé « Jeu de la vie avec tkinter » issu de CommentCaMarche
(codes-sources.commentcamarche.net) est mis à disposition sous les termes de
la licence Creative Commons. Vous pouvez copier, modifier des copies de cette
source, dans les conditions fixées par la licence, tant que cette note
apparaît clairement.

Description :
=============

Comme promis dans mon premier code source voici . le jeu de la vie en mode graph
ique . Pour plus de details voir le jeu de la vie il ya des explication du princ
ipe.
<br /><a name='source-exemple'></a><h2> Source / Exemple : </h2>
<br /><
pre class='code' data-mode='basic'>
from Tkinter import *

import time

def
 demo():
   modif(matrice,matrice_of_len,birth,death)
   for i in range(0,540,
30):
      for j in range(0,540,30):
         if(matrice[j/30][i/30]== '0' ):

            can.create_oval(i,j,i+30,j+30,fill='red')
         else:
        
    can.create_oval(i,j,i+30,j+30,fill='blue')
   fen.after(1,demo)

def aux(
matrice):
    tmp =[]
    for i in range(len(matrice)):
        tmp1 =[]
   
     for j in range(len(matrice[0])):
            tmp1.append(oqp(matrice, i, j
))
        tmp.append(tmp1)
    return tmp

def birth_or_death(matrice, matr
ice_of_len,b_or_d,test):
   c ='0'
   if(test):
      c = '1'
   for i in ra
nge(len(matrice)):
      for j in range(len(matrice[0])):
         if(matrice[
i][j] !=c):
            matrice[i][j] = b_or_d[matrice_of_len[i][j]]
      
d
ef init_mat(fic):
   matrice = []
   file = open(fic,'r')
   line = file.read
lines()
   for i in range(len(line)):
      matrice.append(line[i].split())
 
  file.close();
   return  matrice

def oqp(matrice,lig, col):
   compt = 0

   ligne =len(matrice)
   colonne = len(matrice[0]) -1
   if(lig &lt; ligne -
1):
      if(col != 0):
         if(int(matrice[lig + 1][col -1]) == 1):
    
        compt = compt + 1
      if(int(matrice[lig + 1][col]) == 1):
         
compt = compt + 1
      if(col  != colonne):
         if(int(matrice[lig + 1][
col +1]) == 1):
            compt = compt + 1
   if(col  != colonne ):
      
if(int(matrice[lig ][col +1]) == 1):
         compt = compt + 1
   if(col != 0
):
      if(int(matrice[lig ][col - 1]) == 1):
         compt = compt + 1
   
if(lig != 0):
      if(col != 0):
         if(int(matrice[lig-1][col-1]) == 1)
:
            compt = compt + 1
      if(col  != colonne):
         if(int(ma
trice[lig - 1][col+1]) == 1):
            compt = compt + 1
      if(int(matri
ce[lig - 1][col]) == 1):
         compt = compt + 1
   return compt

def mod
if(matrice,matrice_of_len,birth,death):
   matrice_of_len = aux(matrice)
   bi
rth_or_death(matrice,matrice_of_len,birth,True)
   birth_or_death(matrice,matri
ce_of_len,death,False)
   

# programme principal
file = &quot;life.txt&quot
; #fichier de matrice 
birth= '010101010101010' # regle de naissance
death= '1
10001100110001' #regle de deces
matrice = init_mat(file)
matrice_of_len = []

fen =Tk()
can = Canvas(fen,bg='black', height=550,width=550)
can.grid(row=0,co
lumn=0)
demo()
fen.mainloop()
</pre>
<br /><a name='conclusion'></a><h2> Con
clusion : </h2>
<br />Merci de laisser des commentaire 
<br />Bientot une aid
e aide pour le sudoku
