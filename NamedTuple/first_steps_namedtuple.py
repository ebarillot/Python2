# coding=utf-8

from collections import OrderedDict

from typing import Dict, Any, Callable, NamedTuple

# creation d'une classe avec des champs simples (ressemble aux case class scala)
CompteurOne = NamedTuple(b'CompteurOne',[(b'num', int), (b'name', unicode), (b'value', int)])

cpts = list()
cpts.append(CompteurOne(num=1, name='cpt1', value=11))
cpts.append(CompteurOne(num=1, name='cpt2', value=12))
cpts.append(CompteurOne(num=1, name='cpt3', value=13))

# creation d'une classe avec un champ de type dictionnaire
# le contenu du dict est mutable
CptFi = NamedTuple(b'CptFi',
                   [(b'fichier', unicode),
                    (b'remettant', unicode),
                    (b'date_run', unicode),
                    (b'compteurs', Dict)])

cptfi = CptFi(fichier='fic', remettant='INTRUM', date_run='2017/08/01 10:00:00', compteurs=dict())

for cpt in cpts:
    cptfi.compteurs[cpt.name] = cpt.value

print(cptfi)
print(cptfi.compteurs['cpt1'])
print(cptfi.compteurs.keys())

# classe qui est un CptFi mais avec des compteurs triés
class CptFiOrdered(CptFi):
    def sorted(self, funcmp):
        # type: (Callable[Any, Any]) -> CptFiOrdered
        cpts_sorted = sorted(self.compteurs.items(), key=lambda t: t[1], cmp=funcmp)
        return self._replace(compteurs=OrderedDict(cpts_sorted))


cptfiplus = CptFiOrdered(fichier='fic', remettant='INTRUM', date_run='2017/08/01 10:00:00', compteurs=dict())
for cpt in cpts:
    cptfiplus.compteurs[cpt.name] = cpt.value


def cmpkeys(x, y):
    if x > y:
        return 1
    elif x < y:
        return -1
    else:
        return 0


print('CptFiPlus: '+ str(cptfiplus.sorted(cmpkeys)))
