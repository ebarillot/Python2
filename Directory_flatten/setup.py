# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable
from os import path
import sys

# racine des développements python
python_dev_root = path.normpath(r"D:\Documents\Projets\Developpements\Python")

# ajout du chemin vers les autres packageq nécessaires
# Il faut le package EBCommons notamment car importé dans le prog à freezer
# sys.path.append(python_dev_root)

# le chemin vers le programme à freezer
# prog_src_path = path.normpath(python_dev_root + path.sep + r"\Directory_flatten\directory_flatten.py")
prog_src_script = r"directory_flatten.py"
prog_exe_name = "dirflat.exe"

print(python_dev_root)
print(prog_src_script)

buildOptions = dict(
      packages = [r"EBCommons"]
    , excludes = []
    , path = sys.path.append(python_dev_root)
)

executables = [
    Executable(script=prog_src_script
               , base='Console'
               , targetName=prog_exe_name)      # pour changer le nom de l'exe
]

# On appelle la fonction setup
setup(
    name = "directory_flatten",
    version = "0.1",
    author = "E.Barillot",
    description = "Mise a plat des fichiers d une arborescence",
    options=dict(build_exe=buildOptions),
    executables = executables
)
