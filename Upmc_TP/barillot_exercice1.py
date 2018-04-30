# -*- coding: utf-8 -*-

import platform

class ExceptionApplicative(Exception):
    def __init__(self,s,f=""):
        self.s = s
        self.f = f
    def __str__(self):
        return "{}() : {}".format(self.f, self.s)


def bezout(a,b):
    """
    Calcul de 2 entiers x et y premiers entre eux tels que ax + by = 1 \
    par l'algorithme d'Euclide etendu
    """
    a0,b0 = a,b
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    pgcd = b
    if (pgcd != 1):
        raise ExceptionApplicative("{} et {} ne sont pas premiers entre eux".format(a0,b0),__name__)
    return x, y




if __name__ == "__main__" :
    pltf = platform.python_version()
    if '2.7' in pltf:
        print ("Plateforme python {} OK".format(pltf))
    else:
        print("ATTENTION : ce script a été développé et testé pour python 2.7")
        print("            Il risque de ne pas fonctionner en python {}".format(pltf))


    try:
        n = 51
        m = 18
        p,q = bezout(n,m)
        print "bezout pour {}, {} : ({}).({})+({}).({}) = 1".format(n,m,n,p,m,q)
    except ExceptionApplicative as exap:
        print exap
        
    try:
        n = 51
        m = 19
        p,q = bezout(n,m)
        print "bezout pour {}, {} : ({}).({})+({}).({}) = 1".format(n,m,n,p,m,q)
    except ExceptionApplicative as exap:
        print exap

    try:
        n = 431
        m = 227
        p,q = bezout(n,m)
        print "bezout pour {}, {} : ({}).({})+({}).({}) = 1".format(n,m,n,p,m,q)
    except ExceptionApplicative as exap:
        print exap
