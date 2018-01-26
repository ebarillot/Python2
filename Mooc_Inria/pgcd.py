import os
os.chdir(r'D:\Emmanuel\2015-10_MOOC_Python')

def pgcd(a,b):
    if b > a:
        tmp = a
        a = b
        b = tmp
    ##print a,b
    while b > 0:
        tmp = b
        b = a%b
        a = tmp
        ##print a,b
    return a
    


print pgcd(125,105)
