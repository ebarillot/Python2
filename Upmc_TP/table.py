# coding: Utf8 

def table():
    for i in range(1,10):
        s='{:4d}'.format(i)
        for j in range(2,10):
             s=s+'{:4d}'.format(i*j)
        print s
             
table()

