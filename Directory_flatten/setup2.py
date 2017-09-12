# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable

# version du setup.py qui tente d'utiliser includes au lieu de modifier sys.path
# pour trouver le module EBCommons\prog_helper.py à inclure dans l'exécutable
# Mais même en spécifiant le module à inclure dans le paramètre include_files, ça ne suffit pas.
# le problème de chemin n'est pas résolu.


# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(include_files = [r"D:\Documents\Projets\Developpements\Python\EBCommons\prog_helper.py"], excludes = [])

base = 'Console'

executables = [
    Executable('directory_flatten.py', base=base)
]

setup(name='toto',
      version = '1.0',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
