# coding: Utf8 
 
def Trinome(a,b,c):
    if a==0:
        print 'Equation du premier degré'
        if b!=0:
            print "dont l'unique solution est ",'{:4f}'.format(float(c)/b)
        elif c!=0:
            print "qui n'a pas de solution"
        else:
            print 'dont tout nombre réel est solution'
    else:
        print 'Equation du second degré'
        D=b**2-4*a*c
        if D>0:
            print 'ayant deux racines réelles'
        elif D==0:
            print 'ayant une racine réelle double'
        else:
            print "n'ayant aucune racine réelle",  

def TrinomeC(a,b,c):
    from math import sqrt 
    from cmath import sqrt as sqrtC
    if a==0:
        print 'Equation du premier degré'
        if b!=0:
            print "dont l'unique solution est ",'{:4f}'.format(float(c)/b)
        elif c!=0:
            print "qui n'a pas de solution"
        else:
            print 'dont tout nombre est solution'
    else:
        print 'Equation du second degré'
        D=b**2-4*a*c
        if D>0:
            x1,x2=(-b-sqrt(D))/(2*a),(-b+sqrt(D))/(2*a)
            print 'ayant deux racines réelles : \n', x1, ' et ',x2
        elif D==0:
            print 'ayant une racine réelle double : ','{:4f}'.format(-float(b)/(2*a))
        else:
            x1,x2=(-b-sqrtC(D))/(2*a),(-b+sqrtC(D))/(2*a)
            print 'ayant deux racines complexes conjugués \n', x1, ' et ',x2

execfile('racine.py')
def TrinomeNewton(a,b,c):
    if a==0:
        print 'Equation du premier degré'
        if b!=0:
            print "dont l'unique solution est ",'{:4f}'.format(float(c)/b)
        elif c!=0:
            print "qui n'a pas de solution"
        else:
            print 'dont tout nombre est solution'
    else:
        print 'Equation du second degré'
        D=b**2-4*a*c
        if D>0:
            racD=racine(D,D/2)
            x1,x2=(-b-racD)/(2*a),(-b+racD)/(2*a)
            print 'ayant deux racines réelles : \n', x1, ' et ',x2
        elif D==0:
            print 'ayant une racine réelle double : ','{:4f}'.format(-float(b)/(2*a))
        else:
            racD=(1j)*racine(-D,-D/2)
            x1,x2=(-b-racD)/(2*a),(-b+racD)/(2*a)
            print 'ayant deux racines complexes conjugués \n', x1, ' et ',x2

