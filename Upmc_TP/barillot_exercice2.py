# -*- coding: utf-8 -*-

import platform

def polydiv(A,B):
    """
        Calcul de la division de deux polynomes A / B
        Retourne [Q,R] le quotient et le reste de telle façon que
        A = B*Q+R
    """
    Q = [0] # quotient
    R = A   # reste
    while (polydegre(R) >= polydegre(B)):
        #print ("degre R = {}".format(polydegre(R)))
        #print ("degre B = {}".format(polydegre(B)))
        P = monome(R[polydegre(R)],polydegre(R)-polydegre(B))
        #print ("P = {}".format(P))
        R = polysomme(R,polyproduit(polymul(-1,P),B))
        #print ("R = {}".format(R))
        Q = polysomme(Q,P)
        #print ("Q = {}".format(Q))
        #raw_input()
    return Q,R


def polysomme(A,B):
    """
    Somme de deux polynomes de degrés différents ou égaux
    """
    degA = polydegre(A)
    degB = polydegre(B)
    plus_grand_degre = degA
    if (degA < degB):
        plus_grand_degre = degB
    C = [0]*(plus_grand_degre+1)
    for i in range(0,degA+1):
        C[i] = A[i]
    for i in range(0,degB+1):
        C[i] = C[i] + B[i]
    return C

def polymul(c,P):
    """
    Multiplication d'un polynome par un scalaire
    """
    return [c*x for x in P]

def monome(c,d):
    """
    Construit un monome d'un degre donne et de coefficient donne
    """
    P = [0]*(d+1)
    P[d] = c
    return P

def polydegre(A):
    """
    Degre d'un polynome
    """
    deg = len(A)-1
    while (A[deg] == 0 and deg >= 0):
        deg = deg -1
    return deg

def polyproduit(A,B):
    """
    Produit de 2 polynomes
    """
    C = []
    for k in range(polydegre(A)+polydegre(B)+1):
        s = 0
        for i in range(k+1):
            if (i <= polydegre(A)) and (k-i <= polydegre(B)):
                s = s + A[i]*B[k-i]
        C.append(s)
    return C


if __name__ == "__main__" :
    pltf = platform.python_version()
    if '2.7' in pltf:
        print ("Plateforme python {} OK".format(pltf))
    else:
        print("ATTENTION : ce script a été développé et testé pour python 2.7")
        print("            Il risque de ne pas fonctionner en python {}".format(pltf))

    PA = [1,1,1,1,1]
    PB = [1,1,1,1]
    print "A = {}".format(PA)
    print "B = {}".format(PB)
    Q,R = polydiv(PA,PB)
    print "{} = {} x {} + {}".format(PA,PB,Q,R)
    Q,R = polydiv(PB,PA)
    print "{} = {} x {} + {}".format(PB,PA,Q,R)

    PA = [5,-4,3,2,-1]
    PB = [1,0,-1,1]
    Q,R = polydiv(PA,PB)
    print "{} = {} x {} + {}".format(PA,PB,Q,R)


