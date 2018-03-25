# coding: Utf8 

def eratosthene(n):
    print "Crible d'Eratosthène : "
    L=range(2,n+1)
    LP=[]
    while len(L):
        LP.append(L[0])
        L=[nombre for nombre in L if nombre % LP[-1] !=0]
    print 'Nombres premiers plus petits que ', n
    print LP


n=input('Entrez un entier ')
eratosthene(n)



def eratostheneC(n):
    pasPremiers=[k for j in range(2, int(racine(n))+1) for k in range(j*2, n, j)]
    return [k for k in range(2, n) if k not in pasPremiers]

from math import sqrt as racine
print 'Les nombres premiers plus petits que ', n, 'sont \n', eratostheneC(n)

 
