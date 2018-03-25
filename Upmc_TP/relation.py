# coding: Utf8 
# x R y  signifie "x divise y"

relation={}
n=120
elements = range(1,n+1)
for k in elements:
    print elements[k-1], k
    relation[k]=[m for m in elements if m % k ==0]
print 'relation : \n', relation
    
# relation inverse (à partir du dictionnaire)
relationM1={}
for m in elements:
	relationM1[m] = [k for k in elements if m in relation[k]]

print 'relation^{-1}: \n', relationM1



