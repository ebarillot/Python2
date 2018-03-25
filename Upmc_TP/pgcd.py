# coding: Utf8 

def PGCD(x,y):     # pas optimal, mais très clair!
    if x>y:
        x,y=y,x
    r=y%x
    while r:
        x,y=r,x
        r=y%x
    return x


def pgcd(a,b):    # solution élégante!
    while b:
        a,b = b, a%b
    return abs(a)

 
