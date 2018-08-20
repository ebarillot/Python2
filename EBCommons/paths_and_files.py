# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import fnmatch
import os
import re
from shutil import copy2, move
from string import lower

__author__ = 'Emmanuel Barillot'


def mkdir_path(path_to_create):
    # type: (unicode) -> None
    """
    Crée un répertoire et tous les répertoire intermédiaires qui manquent.
    Fonctionne sous Windows et sous Linux.
    :param path_to_create: le chemin à créer
    :return: None
    """
    def mkp(p):
        # type: (unicode) -> None
        """
        Fonction appelée récursivement pour créer les répertoire intermédiaires qui manquent
        :param p: chemin dont on contrôle l'existence avant de le créer
        :return: None
        """
        if p is not None and not os.path.isdir(p):
            mkp(os.path.split(p)[0])
            os.mkdir(p)
    mkp(path_to_create)


def copy_files_to_path(path_orig, path_dest, extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP'),
                       include_patterns=('*',), exclude_patterns=None):
    # type: (unicode, unicode, tuple or None, tuple or None, tuple or None) -> None
    if not os.path.isdir(path_dest):
        mkdir_path(path_dest)
    for filename in filter_files_with_patterns_and_extensions(
            os.listdir(path_orig), extensions, include_patterns, exclude_patterns):
        copy2(os.path.join(path_orig, filename), os.path.join(path_dest, filename))


def move_files_to_path(path_orig, path_dest, extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP'),
                       include_patterns=('*',), exclude_patterns=None):
    # type: (unicode, unicode, tuple or None, tuple or None, tuple or None) -> None
    if not os.path.isdir(path_dest):
        mkdir_path(path_dest)
    for filename in filter_files_with_patterns_and_extensions(
            os.listdir(path_orig), extensions, include_patterns, exclude_patterns):
        move(os.path.join(path_orig, filename), os.path.join(path_dest, filename))


def rm_files(path_orig, extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP'), include_patterns=('*',),
             exclude_patterns=None):
    # type: (unicode, tuple or None, tuple or None, tuple or None) -> None
    for filename in filter_files_with_patterns_and_extensions(os.listdir(path_orig), extensions, include_patterns,
                                                              exclude_patterns):
        os.remove(os.path.join(path_orig, filename))


def rename_files(path_orig, old_str, new_str, extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP'),
                 include_patterns=('*',), exclude_patterns=None):
    # type: (unicode, unicode, unicode, tuple or None, tuple or None, tuple or None) -> None
    for filename in filter_files_with_patterns_and_extensions(os.listdir(path_orig), extensions, include_patterns,
                                                              exclude_patterns):
        newname = filename.replace(old_str, new_str)
        os.rename(os.path.join(path_orig, filename), os.path.join(path_orig, newname))


def count_files(path_orig, extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP'), include_patterns=('*',),
                exclude_patterns=None):
    # type: (unicode, tuple or None, tuple or None, tuple or None) -> int
    return len(filter_files_with_patterns_and_extensions(os.listdir(path_orig), extensions, include_patterns,
                                                         exclude_patterns))


def count_files_by_extensions(path_orig, extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP'),
                              include_patterns=('*',), exclude_patterns=None):
    # type: (unicode, tuple or None, tuple or None, tuple or None) -> dict

    extension_cnt = dict()
    for filename in filter_files_with_patterns_and_extensions(os.listdir(path_orig), extensions, include_patterns,
                                                              exclude_patterns):
        extension = os.path.splitext(filename)[1]
        if extensions:
            if extension in extensions:
                extension_cnt[extension] = extension_cnt.get(extension, 0) + 1
        else:
            extension_cnt[extension] = extension_cnt.get(extension, 0) + 1

    return extension_cnt


def filter_files_with_regex(filenames, file_re=".*"):
    # type: (unicode, unicode) -> []
    """
    Retourne la liste des fichiers réguliers présents dans le répertoire
    Le nom des fichiers peut être filtré par une expression régulière

    :param filenames: les noms de fichiers à filtrer
    :param file_re: filtre sur le nom des fichiers
    :return: liste des noms de fichiers trouvés
    """
    file_re_comp = re.compile(file_re)
    filtered_file_names = filter(lambda x: file_re_comp.match(x) is not None, filenames)
    return filtered_file_names


def filter_files_with_patterns_and_extensions(filenames, extensions=None, include_patterns=('*',),
                                              exclude_patterns=None):
    # type: (list, tuple or None, tuple or None, tuple or None) -> list
    filtered = filenames
    if extensions:
        filtered = filter(lambda x: x.endswith(tuple(map(lower, extensions))), map(lower, filtered))
    if include_patterns and include_patterns[0] != '*' and filtered:
        filtered = [f for patt in include_patterns for f in filtered if fnmatch.fnmatch(f, patt)]
    if exclude_patterns and filtered:
        filtered = [f for patt in exclude_patterns for f in filtered if not fnmatch.fnmatch(f, patt)]
    return filtered


if __name__ == "__main__":
    # mkdir_path(r'T:\Photos\toto\titi\tutu')

    # print(filter_files_with_patterns_and_extensions(os.listdir(r'T:\Photos\2009-05-07-USA\Originaux\DxO')
    #                                                 , extensions=None
    #                                                 , include_patterns=("*DxO*",)
    #                                                 , exclude_patterns=("*DxO_2*")
    #                                                 )[:20]
    #       )

    # print(count_files(r'T:\Photos\2009-05-07-USA\Originaux\DxO'
    #                             , extensions=None
    #                             , include_patterns=("*DxO*",)
    #                             , exclude_patterns=("*DxO_2*",)
    #                             ))

    print(count_files(r'T:\Photos\2010-07-17-KadoreFleurs', extensions=None, include_patterns=("*DxO*",),
                      exclude_patterns=None))
    print(count_files(r'T:\Photos\2010-07-17-KadoreFleurs', extensions=None, include_patterns=('*',),
                      exclude_patterns=("*DxO*",)))

    print(count_files_by_extensions(r'T:\Photos\2010-07-17-KadoreFleurs', extensions=None, include_patterns=('*',),
                                    exclude_patterns=None))

    # move_files_to_path(r'T:\Photos\2009-05-07-USA\Originaux\DxO'
    #                 , r'T:\Photos\2009-05-07-USA\Originaux\DxO_2'
    #                 , extensions=None
    #                 , include_patterns=("*DxO_2*",)
    #                 , exclude_patterns=None
    #                 )
    # rename_files(r'T:\Photos\2009-05-07-USA\Originaux\DxO'
    #              , 'DxO_1'
    #              , 'DxO'
    #              , extensions=None
    #              , include_patterns=("*DxO_2*",)
    #              , exclude_patterns=None
    #              )
