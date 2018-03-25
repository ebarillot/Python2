# coding: Utf8 

def polynomeD(L):   #derivee
    n=len(L)-1
    return [k*L[k] for k in range(1,n+1)]



def polynomeP(L):   #primitive
    n=len(L)-1
    L=[L[k]/float(k+1) for k in range(0,n+1)]
    L.insert(0,0)
    return L
    


S=[1,-1,0,5,17,13]
print S
DS=polynomeD(S)
print DS

S=[1,-1,0,5,10]
print S
PS=polynomeP(S)
print PS

