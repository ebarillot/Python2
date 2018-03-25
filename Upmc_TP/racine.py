# coding: Utf8 

def racine(a,x0):    # prendre x0=a/2 ou x0=int(math.sqrt(a))
    NbrMaxIter=100
    a=float(a)
    rac=x0        # rac=float(x0)
    for k in range(0,NbrMaxIter):
        rac=0.5*(rac+a/rac)
    return rac


##x=1725.245
##sol=racine(x)
##print sol,sol*sol-x
