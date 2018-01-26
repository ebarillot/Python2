from Tkinter import *

import time

def demo():
   modif(matrice,matrice_of_len,birth,death)
   for i in range(0,540,30):
      for j in range(0,540,30):
         if(matrice[j/30][i/30]== '0' ):
            can.create_oval(i,j,i+30,j+30,fill='red')
         else:
            can.create_oval(i,j,i+30,j+30,fill='blue')
   fen.after(1000,demo)

def aux(matrice):
    tmp =[]
    for i in range(len(matrice)):
        tmp1 =[]
        for j in range(len(matrice[0])):
            tmp1.append(oqp(matrice, i, j))
        tmp.append(tmp1)
    return tmp

def birth_or_death(matrice, matrice_of_len,b_or_d,test):
   c ='0'
   if(test):
      c = '1'
   for i in range(len(matrice)):
      for j in range(len(matrice[0])):
         if(matrice[i][j] !=c):
            matrice[i][j] = b_or_d[matrice_of_len[i][j]]
      
def init_mat(fic):
   matrice = []
   file = open(fic,'r')
   line = file.readlines()
   for i in range(len(line)):
      matrice.append(line[i].split())
   file.close();
   return  matrice

def oqp(matrice,lig, col):
   compt = 0
   ligne =len(matrice)
   colonne = len(matrice[0]) -1
   if(lig < ligne -1):
      if(col != 0):
         if(int(matrice[lig + 1][col -1]) == 1):
            compt = compt + 1
      if(int(matrice[lig + 1][col]) == 1):
         compt = compt + 1
      if(col  != colonne):
         if(int(matrice[lig + 1][col +1]) == 1):
            compt = compt + 1
   if(col  != colonne ):
      if(int(matrice[lig ][col +1]) == 1):
         compt = compt + 1
   if(col != 0):
      if(int(matrice[lig ][col - 1]) == 1):
         compt = compt + 1
   if(lig != 0):
      if(col != 0):
         if(int(matrice[lig-1][col-1]) == 1):
            compt = compt + 1
      if(col  != colonne):
         if(int(matrice[lig - 1][col+1]) == 1):
            compt = compt + 1
      if(int(matrice[lig - 1][col]) == 1):
         compt = compt + 1
   return compt

def modif(matrice,matrice_of_len,birth,death):
   matrice_of_len = aux(matrice)
   birth_or_death(matrice,matrice_of_len,birth,True)
   birth_or_death(matrice,matrice_of_len,death,False)
   

# programme principal
file = "life.txt" #fichier de matrice 
birth= '010101010101010' # regle de naissance
death= '110001100110001' #regle de deces
matrice = init_mat(file)
matrice_of_len = []
fen =Tk()
can = Canvas(fen,bg='black', height=550,width=550)
can.grid(row=0,column=0)
demo()
fen.mainloop()
