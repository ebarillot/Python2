import math as m
from decimal import Decimal

def develop_dyad(x, n=10):
    """ Calcul du développement dyadique propre à l'ordre n
    """
    dd = []
    x0 = 0.
    x1 = int(2.0*x)
    print (x0,x1)
    dd.append(x1)
    for i in range(1,n):
        x0 = x0 + x1 / (2.0**(i))   # attention, ne pas mettre i+1
        ##print ("[{}] x0={}".format(i,x0))
        x1 = int(2.0**(i+1)*(x-x0))
        ##print ("[{}] x1={}".format(i,x1))
        dd.append(x1)
    ##print (i,x0,x1)
    return dd



def compose_dyad(dd):
    """ Compose un nombre x à partir de son développement dyadique propre à l'ordre n
    """
    x = 0.
    for i in range(len(dd)):
        x = x + dd[i] / (2.0**(i+1))   # attention, ne pas mettre i+1
        ##print ("[{}] x={}".format(i,x))
    return x


# x doit être dans [0,1[
x = Decimal(m.pi / 4.)
##x = 1./3.
n = 50

print ("x = %f" % x)
dd = develop_dyad(x, n)
print (dd)
print (compose_dyad(dd))
