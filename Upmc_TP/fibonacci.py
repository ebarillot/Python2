# coding: Utf8 

def fibo1(n):
    if type(n)!=int or n<0:      #+ test n >= 2
        return 'probleme  !'
    u0,u1=0,1                      
    for k in range(2,n+1):
        u=u0+u1
        u0=u1
        u1=u
    return u

def fibo2(n):
     if n < 2: return n
     u,v=0,1
     for i in range(1,n): u,v=v,u+v
     return v

def fiboReel(n):
    a=math.sqrt(5)
    return (((1+a)/2)**n - ((1-a)/2)**n)/a

def fibo3(n):   # test n>2
    if n<=1:
         return n
    else:
         return fibo3(n-1)+fibo3(n-2)


def fibo4(n):
     def aux (n):
             if n == 0: return 1,0
             u,v=aux(n/2)
             u,v=u*u+v*v,v*(2*u+v)                 
             return (v,u+v) if (n%2==1) else (u,v) 
     return aux(n)[1]

  





