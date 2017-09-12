----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------

La plupart des indications données ici fonctionnenent avec l'environnement Python / Anaconda

----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
Pour mettre à jour la distribution Anaconda sur le PC
- ouvrir une console anaconda en tant qu'administrateur
- lancer conda update --prefix "C:\Program Files\Anaconda2" anaconda

----------------------------------------------------------------------------------------------------
En cas de PROXY

Dans le terminal cmd
- set HTTP_PROXY=http://proxy.int.dns:8888
- set HTTPS_PROXY=https://proxy.int.dns:8888

Si ça plante quand même sur la vérification SSL
Créer un fichier .condarc dans le HOME du user (C:\Users\emmanuel_barillot = contenu de %USERPROFILE% ou %HOMEPATH%) et y mettre :
proxy_servers:
    http: http://proxy.int.dns:8888
    https: https://proxy.int.dns:8888

ssl_verify: False
----------------------------------------------------------------------------------------------------



----------------------------------------------------------------------------------------------------
HISTOIRE des apprentissages
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
2017-08-24
Pour trouver le source d'une classe, par exemple celui de la classe Executable du package cx_Freeze

Dans une console Python :
import inspect
import cx_Freeze

print(inspect.getsource(Executable)) et le sourec s'affiche

----------------------------------------------------------------------------------------------------
2017-08-24
Utilisation de cx_Freeze pour fabriquer un exécutable avec le projet python directory_flatten

Dans une console Anaconda se placer dans le répertoire D:\Documents\Projets\Developpements\Python\Directory_flatten
qui contient le prog à rendre executable.

1. Créer le script setup.py (voir ce projet Directory_flatten pour avoir un exemple)
2. taper la commande python setup.py build
    => crée un sous répertoire build qui contient l'exécutable et ce qu'il lui faut pour fonctionner
3. taper la commande python setup.py bdist_msi
    => crée un programme d'installation de l'exécutable et de son environnemnt, de façon à le distribuer proprement

Remarques:
- build_exe = dict(include_files = [...], packages = [...], excludes = [...])
  permet normalement de spécifier tous les pakages indispensables, les programmes à prendre en compte
  Mais pour que ça marche, il faut que tous les packages et les scripts soient sous le répertoire de base
  du projet.
  Si on veut inclure un package d'un répertoire qui n'est pas dans cette sous arbo, il ajouter son chemin
  dans l'environnement d'exécution du script setup.py. C'est ce que j'ai fait en introduisant
  sys.path.append(python_dev_root).
 
- l'option path de build_exe permet aussi d'ajouter des répertoires à la volée pour la compilation

 
Voir le site d'origine du module cx_Freeze :
http://cx-freeze.readthedocs.io/en/latest/distutils.html#distutils

Autre toto intéressant:
http://python.jpvweb.com/python/mesrecettespython/doku.php?id=cx_freeze

Pour des programmes plus complexes, il peut être utile de comprendre et d'utiliser le module distutils
décrit ici, sur lequel est basé cx_Freeze :
https://docs.python.org/2/distutils/introduction.html

----------------------------------------------------------------------------------------------------
2017-08-24
Installation du package cx_Freeze qui permet de fabriquer un executable autonome (standalone).
dans une console anaconda:

pip install cx_Freeze

Ca ne marche pas avec conda install cx_Freeze; sans doute parce que la distrib Anaconda ne
référence pas ce package.

http://apprendre-python.com/page-cx_freeze-creer-executables-python-cours-apprendre
http://cx-freeze.readthedocs.io

----------------------------------------------------------------------------------------------------
2017-08-22
Installation du package typing qui permet une controle statique des types en python.
dans une console anaconda:
conda install typing

Lien http://mypy.readthedocs.io

Ce controle des types est intégré à partir de Python 3.5.


----------------------------------------------------------------------------------------------------
2017-07-19
Installation Anaconda 4.4.0 à partir de Anaconda2-4.4.0-Windows-x86_64.exe
Installation sous 
D:\_Program_files\Conda2    => j'ai raccourci le nom, car certains Forums indiquent qu'il ne faut pas dépasser 30 caractères pour le "Prefix" Python / Anadonca


----------------------------------------------------------------------------------------------------
Lancement de spyder avec Anaconda 2.7 64 bits => Plantage
Juste installée, en 32 ou 64bits, message d'erreur au lancement:

This application failed to start because it could not find or load the Qt
platform plugin "windows in ""

Correction du plantage de Spyder, solution indiquée ici : https://github.com/ContinuumIO/anaconda-issues/issues/1270
COPY the
Continuum\Anaconda3\Library\plugins\platforms
folder to
Continuum\Anaconda3

Du coup j'ai copié tout le répertoire de <racine Anaconda>\Library\plugins\platforms  vers  <racine Anaconda>
et le lancement de spyder marche !

----------------------------------------------------------------------------------------------------
Installation de csvkit
Dans une console Anaconda:
> conda install csvkit
Fetching package metadata .....
Solving package specifications: .

Package plan for installation in environment D:\_Program_files\Conda2:

The following NEW packages will be INSTALLED:

    csvkit: 0.9.1-py27_1
    dbf:    0.96.003-py27_0

Proceed ([y]/n)? y

dbf-0.96.003-p 100% |###############################| Time: 0:00:00   5.32 MB/s
csvkit-0.9.1-p 100% |###############################| Time: 0:00:00  12.11 MB/s


----------------------------------------------------------------------------------------------------
Installation client Oracle 64 bits sous Windows:

Télécharger les packages utiles sur le site d'Oracle (selon la version voulue pour le client):
ATTENTION à bien télécharger les packages 64 bits ! Par défaut, Oracle propose les 32 bits.
instantclient-basic-windows.x64-11.2.0.4.0.zip      ==> driver de base indispensable pour se connecter à une bdd en mode OCI
instantclient-sdk-windows.x64-11.2.0.4.0.zip        ==> SDK, pour développer des progs, notamment en Python, donc indispensable pour se connecter à Oracle à partir de Python
instantclient-sqlplus-windows.x64-11.2.0.4.0.zip    ==> pour tester le client sur une connection avec sqlplus, avant d'utiliser Python

Décompresser les packages précédents les uns après les autres dans le répertoire:
D:\_Program_files\OracleClient_64bit
Un sous répertoire instantclient_11_2 se créée dans lequel tous les fichiers vont venir s'installer.


Positionnement de la variable d'environnement ORACLE_HOME pour utiliser le don driver:
Dans les propriétés de l'ordinateur / Paramètres système avancés / Variables d'environnement / Variables utilisateur pour emmanuel_barillot
Faire "Nouvelle" et taper:
ORACLE_HOME=D:\_Program_files\OracleClient_64bit\instantclient_11_2


Vérification dans une console anaconda:
> set ORACLE_HOME
==> ORACLE_HOME=D:\_Program_files\OracleClient_64bit\instantclient_11_2

Ensuite pour vérifier une connection avec le client Oracle taper dans une console anaconda:
sqlplus fra2prod/fra2prod@devdbirisfr.int.dns:1521/svcproddev2.world
Normalement, une connexion s'établit avec fra2prod de l'instance Oracle PRODDEV2.

----------------------------------------------------------------------------------------------------
Installation cx_Oracle avec pip dans une console anaconda:

- l'installation par le réseau ne se pase pas bien
- installation par le package whl:
  > pip install --use-wheel --no-index --find-links=. cx_Oracle-5.3+oci12c-cp27-cp27m-win_amd64.whl

L'exécution du script python suivant dans une console anaconda donne une erreur: "ImportError: DLL load failed: The specified module could not be found."

import cx_Oracle

connstr='etudes_consult/IF5489rG@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=dbirisclone.int.dns)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=svcprodclo1.world)))'
conn = cx_Oracle.connect(connstr)
curs = conn.cursor()
curs.execute('select count(*) from fra2prod.idcellixium_param')
for row in curs:
    print row
conn.close()

----------------------------------------------------------------------------------------------------
Pour désinstaller cx_Oracle avec pip
Dans une console anaconda:
> pip uninstall cx_Oracle

----------------------------------------------------------------------------------------------------
Installation cx_Oracle avec conda dans une console anaconda:
documentation conda: https://conda.io/docs/


> conda info
==> donne une liste de channel URLs vide
Pour ajouter une URL:
> conda config --add channels https://repo.continuum.io/pkgs/free/win-64/
ou encore:
conda config --add channels http://conda.anaconda.org/conda-forge
conda config --add channels http://conda.anaconda.org/conda-forge-test

Ensuite, installation de cx_Oracle avec conda:

>conda install cx_Oracle
Fetching package metadata .....
Solving package specifications: .

Package plan for installation in environment D:\_Program_files\Conda2:

The following NEW packages will be INSTALLED:

    cx_oracle: 6.0b2-py27_0

The following packages will be UPDATED:

    conda:     4.3.21-py27_0 --> 4.3.22-py27_0

Proceed ([y]/n)? y

cx_oracle-6.0b 100% |###############################| Time: 0:00:00   6.54 MB/s
conda-4.3.22-p 100% |###############################| Time: 0:00:00  11.34 MB/s


----------------------------------------------------------------------------------------------------
Tests connection Oracle dans une console Python / Anaconda ou dans Spyder
Le script suivant fonctionne parfaitement:

import cx_Oracle

connstr='etudes_consult/IF5489rG@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=dbirisclone.int.dns)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=svcprodclo1.world)))'
conn = cx_Oracle.connect(connstr)
curs = conn.cursor()
curs.execute('select count(*) from fra2prod.idcellixium_param')
for row in curs:
    print row
conn.close()



----------------------------------------------------------------------------------------------------
Installation de l'IDE PyCharm:
sous
D:\_Program_files\PyCharm_2017.1.5
en version 64 bits

Une fois l'IDE lancé, configurer le chemin vers l'interpréteur Python dans les Settings du projet.

----------------------------------------------------------------------------------------------------
Installation à partir de fichiers whl:

On peut récupérer les fichiers whl (navigateur chrome, car firefox semble poser pb avec les certificats du site pypi)
ici https://pypi.python.org/pypi (moteur de recherche et dépendances)
ou ici https://docs.continuum.io/anaconda/pkg-docs
ou ici http://www.lfd.uci.edu/~gohlke/pythonlibs/

Chercher le package et la version pour python 2.7 - amd64 (la version installéé avec anaconda) sur le site :
https://pypi.python.org

Exemple, pour installer paramiko, télécharger:
cffi
cryptography
ecdsa
paramiko

Dans une console MinGW ou cmd (administrateur)
Se mettre dans le repertoire où il y a les packages *.whl (D:\Documents\Downloads\install-python-pylab)

pip install --use-wheel --no-index --find-links=. cffi-1.8.3-cp27-cp27m-win_amd64.whl
pip install --use-wheel --no-index --find-links=. cryptography-1.5.2-cp27-cp27m-win_amd64.whl
pip install --use-wheel --no-index --find-links=. ecdsa-0.13-py2.py3-none-any.whl
pip install --use-wheel --no-index --find-links=. paramiko-1.17.2-py2.py3-none-any.whl

et puis Fabric qui nécessite paramiko < 2.0.0
pip install --use-wheel --no-index --find-links=. Fabric-1.12.0-py2-none-any.whl


Pour voir si un package est installé: pip list | grep <package>

----------------------------------------------------------------------------------------------------

Installation (windows) à partir de fichiers .tar.gz sans utiliser pip:

(méthode inspirée de : http://biyoenformatik.blogspot.fr/2014/12/how-to-install-openpyxl-on-windows.html)

On peut récupérer les fichiers <package>.tar.gz (navigateur chrome, car firefox semble poser pb avec les certificats du site pypi)
ici https://pypi.python.org/pypi (moteur de recherche et dépendances)
ou ici https://docs.continuum.io/anaconda/pkg-docs
ou ici http://www.lfd.uci.edu/~gohlke/pythonlibs/

- Dans une fenetre cmd windows, se placer dans le répertoire du téléchargement:
  D:\Documents\Downloads\install-python-pylab
Exemple avec le package openpyxl-2.4.0:
- Dans un explorateur, décompresser (avec 7zip par exemple) dans le répertoire openpyxl-2.4.0.tar (à créer)
  -> Un répertoire dist est créé qui contient openpyxl-2.4.0.tar
- Dans l'explorateur aller dans dist et détarer avec 7zip: un répertoire openpyxl-2.4.0 est créé.
  -> Arbo complete: <téléch>\openpyxl-2.4.0\dist\openpyxl-2.4.0\
- Dans la console cmd aller dans ce répertoire et faire: python setup.py install
- Le package s'installe dans le répertoire site-packages qui correspond à l'installation de la commande python qui a été exécutée hjuste avant.
- Par exemple, pour une installation Anaconda x64 dont le répertoire racine est D:\_Program_files\Anaconda2_x64,
  le nouveau package est installé dans le sous répertoire suivant de l'installation:
  D:\_Program_files\Anaconda2_x64\Lib\site-packages\openpyxl-2.4.0-py2.7.egg

- Dans une console cmd, la commande pip list affiche bien une ligne openpyxl (2.4.0)




----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
Méthode d'installation qui ne marche pas toujours :

. ouvrir un windows powershell
. aller sous  C:\Python27\Scripts>
. faire dans l'ordre:
    pip.exe install numpy-1.9.3+mkl-cp27-none-win_amd64.whl
    pip.exe install six-1.10.0-py2.py3-none-any.whl
    pip.exe install python_dateutil-2.4.2-py2.py3-none-any.whl
    pip.exe install pyparsing-2.0.6-py2.py3-none-any.whl
    pip.exe install pytz-2015.7-py2.py3-none-any.whl
    pip.exe install cycler-0.9.0-py2.py3-none-any.whl
    pip.exe install setuptools-19.1.1-py2.py3-none-any.whl
    pip.exe install matplotlib-1.5.0-cp27-none-win_amd64.whl

    
Attention à regarder les dépendances non satisfaites et à installer les packages nécessaires.
Les packages whl sont dispo ici : http://www.lfd.uci.edu/~gohlke/pythonlibs/

En allant chercher les packages sur Internet (en passant par le proxy) :
C:\Python27\Scripts>pip.exe --proxy proxy1.int.dns:8888 install rpy2  --upgrade
Requirement already up-to-date: rpy2 in c:\python27\lib\site-packages
Requirement already up-to-date: six in c:\python27\lib\site-packages (from rpy2)
Requirement already up-to-date: singledispatch in c:\python27\lib\site-packages (from rpy2)


Sous Linux:
pip --proxy http://proxy.int.dns:8888 install rpy2


----------------------------------------------------------------------------------------------------
Doc sur pip install:

https://pip.pypa.io/en/latest/reference/pip_install
https://pip.pypa.io/en/latest/user_guide/#installing-from-wheels

----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
Mise à jour de pip :

python -m pip install --upgrade pip

----------------------------------------------------------------------------------------------------
Autres packages dispo chez anaconda
https://docs.continuum.io/anaconda/pkg-docs

Installation:
conda install csvkit

----------------------------------------------------------------------------------------------------
Comment installer des packages avec pip sous anaconda ?

Car il ne semble pas possible d'installer des packages pip avec conda.

Question toujours ouverte: comment utiliser pip au travers d'un proxy en gérant correctement le certificat ?

----------------------------------------------------------------------------------------------------
Installation à partir de fichiers whl:

On peut récupérer les fichiers whl (navigateur chrome, car firefox semble poser pb avec les certificats du site pypi)
ici https://pypi.python.org/pypi (moteur de recherche et dépendances)
ou ici https://docs.continuum.io/anaconda/pkg-docs
ou ici http://www.lfd.uci.edu/~gohlke/pythonlibs/

Chercher le package et la version pour python 2.7 - amd64 (la version installéé avec anaconda) sur le site :
https://pypi.python.org

Exemple, pour installer paramiko, télécharger:
cffi
cryptography
ecdsa
paramiko

Dans une console MinGW ou cmd (administrateur)
Se mettre dans le repertoire où il y a les packages *.whl (D:\Documents\Downloads\install-python-pylab)

pip install --use-wheel --no-index --find-links=. cffi-1.8.3-cp27-cp27m-win_amd64.whl
pip install --use-wheel --no-index --find-links=. cryptography-1.5.2-cp27-cp27m-win_amd64.whl
pip install --use-wheel --no-index --find-links=. ecdsa-0.13-py2.py3-none-any.whl
pip install --use-wheel --no-index --find-links=. paramiko-1.17.2-py2.py3-none-any.whl

et puis Fabric qui nécessite paramiko < 2.0.0
pip install --use-wheel --no-index --find-links=. Fabric-1.12.0-py2-none-any.whl


Pour voir si un package est installé: pip list | grep <package>

----------------------------------------------------------------------------------------------------


----------------------------------------------------------------------------------------------------
Installer R:
conda install -c r r-essentials
conda install -c r r

anaconda search -t conda rpy2

----------------------------------------------------------------------------------------------------
Installation rpy2 à partir du package whl :
pip install "D:\Telechargements\rpy2-2.7.8-cp27-none-win_amd64.whl"

pip install "D:\Documents\Downloads\install-python-pylab\rpy2-2.7.8-cp27-none-win_amd64.whl"

[Program] C:\Windows\system32>pip install "D:\Telechargements\rpy2-2.7.8-cp27-none-win_amd64.whl"
Processing d:\telechargements\rpy2-2.7.8-cp27-none-win_amd64.whl
Requirement already satisfied (use --upgrade to upgrade): six in c:\program files\anaconda2\lib\site-packages (from rpy2==2.7.8)
Requirement already satisfied (use --upgrade to upgrade): singledispatch in c:\program files\anaconda2\lib\site-packages (from rpy2==2.7.8)
Installing collected packages: rpy2
Successfully installed rpy2-2.7.8
You are using pip version 8.0.2, however version 8.1.0 is available.
You should consider upgrading via the 'python -m pip install --upgrade pip' command.

----------------------------------------------------------------------------------------------------
pour faire marcher rpy2 dans une console python:

- ouvrir console anaconda python
- faire : set R_HOME=C:\Program Files\R\R-3.2.3      sans mettre de " "
- faire : set R_USER=emmanuel ou contenu de %USERNAME%
- faire : set PATH:%PATH%;C:\Program Files\R\R-3.2.3\bin\x64

Puis taper python et 
from rpy2.robjects import r
r('x <- rnorm(100)')  # generate x at R
r('y <- x + rnorm(100,sd=0.5)')  # generate y at R
r('plot(x,y)')  # have R plot them


----------------------------------------------------------------------------------------------------
Sites internet qui peuvent aider :
http://www.swegler.com/becky/blog/2014/08/03/ipython-ipython-notebook-anaconda-and-r-rpy2/
https://cran.r-project.org/bin/windows/base/
https://www.continuum.io/conda-for-r
https://www.continuum.io/blog/developer/jupyter-and-conda-r
http://heather.cs.ucdavis.edu/~matloff/rpy2.html#use


----------------------------------------------------------------------------------------------------
pour faire marcher rpy2 dans spyder:

- définir les variables R_HOME, R_USER et PATH comme ci-dessus dans l'environnement Windows général
- ou créer un .bat qui définit les variables R_HOME, R_USER et PATH comme ci-dessus avant de lancer python ou spyder


