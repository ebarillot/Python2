
Le code a été développé et exécuté avec PyCharm en version 2018.1.
Il est basé sur Python 2.7.13, fourni par la distribution Anaconda 4.4.7.

J'exécute mon code pas à pas dans la console Python de PyCharm.
Je sélectionne le code à exécuter et je le lance avec le raccourci clavier PyCharm: Ctrl-Shift-E.
C'est très commode pour mettre au point, notamment quand il y a beaucoup de figures générées.

J'utilise Git et GitHub pour versionner mon code.
Cela m'oblige à structurer un tant soit peu mes projets et mes répertoires de code Python.
C'est pourquoi en début de script, il y a un certain nombre de variables qui permettent de configurer:
- path_root: le chemin vers le répertoire du script lui-même
- path_data: le chemin vers le fichier des données.
Dans mon environnement, ils sont différents. Ils peuvent être semblables sur un autre environnement.

J'ai aussi l'habitude de travailler avec un code source en UTF-8 et j'utilise des chaines de caractères par défaut en unicode grâce à la directive :
from __future__ import unicode_literals

