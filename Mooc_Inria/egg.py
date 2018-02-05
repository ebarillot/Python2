# fichier egg.py
import spam
from spam import beans
def g(L):
    L.append(spam.beans)
    L.append(beans)
    spam.beans = 2
    L.append(spam.beans)
    L.append(beans)
    L.append(spam.f())
    return L
print g([])
