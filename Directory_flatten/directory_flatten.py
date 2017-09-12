# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import fnmatch

from EBCommons.prog_helper import log_init, log_exit, log_write
from EBCommons.paths_and_files import mkdir_path, copy_files_to_path, filter_files_with_patterns_and_extensions, \
    move_files_to_path, rename_files, rm_files
import os.path

from shutil import copy2
from typing import Union

__author__ = 'Emmanuel Barillot'

#
# Tous les fichiers d'une hiérarchie de répertoires sont attachés à la racine
# leur nom tient compte de leur position dans la hiérarchie d'origine
#

# le separateur utilisé dans le nom du fichier issu de la transformation de son chemin normalisé
# (nom du fichier compris)
PATH_SEP_IN_NAME = "#"


def get_all_rel_file_names(src_path, extensions=None, include_patterns=('*',), exclude_patterns=None, exclude_dirs=None):
    # type: (unicode, tuple, tuple, tuple, tuple) -> list
    """
    Retourne la liste à plat du chemin de tous les fichiers contenus dans le chemin fourni et dans ses sous répertoires

    :param src_path: le chemin de départ
    :param extensions: extentions de fichiers à inclure (majuscule ou minuscule)
    :param include_patterns: liste de motifs à inclure pour le nom de fichier après filtrage de l'extension
    :param exclude_patterns: liste de motifs à exclure pour le nom de fichier
    :param exclude_dirs: liste de motifs à exclure pour le nom de répertoire
    :return: liste de fichiers
    """
    if src_path is None:
        raise NameError("un chemin valide doit être défini")
    file_flatlist = []
    for dirpath, dirnames, filenames in os.walk(src_path):
        if filenames:
            rel_path = dirpath[len(src_path):]  # retire le début du chemin -> le chemin relatif à src_path
            # fabrique une liste de noms de noms de fichiers qui contiennent le chemin relatif à src_path
            file_flatlist = file_flatlist +\
                            [os.path.join(rel_path, filename)
                             for filename in filter_files_with_patterns_and_extensions(filenames
                                                                                      , extensions
                                                                                      , include_patterns
                                                                                      , exclude_patterns)]
        if exclude_dirs:
            for exclude_dir in exclude_dirs:
                for dirname in dirnames:
                    if fnmatch.fnmatch(dirname, exclude_dir):
                        dirnames.remove(dirname)
    return file_flatlist


def make_flat_name(filename_with_path, path_sep_in_name=PATH_SEP_IN_NAME):
    # type: (unicode, unicode) -> unicode
    """
    Construit un nom à plat à partir du chemin vers le fichier
    Exemple:  /dir1/dir2/doc.txt  ->  dir1<sep>dir2<sep>doc.txt

    Sous Windows, supprime le drice (C:, D: ...)

    :param filename_with_path: le nom complet du fichier
    :param path_sep_in_name: [default PATH_SEP_IN_NAME] le séparateur
    :return: un nom de fichier à plat, dont chaque élément du chemin est séparé par le séparateur fourni
    """
    filename_with_path = os.path.splitdrive(filename_with_path)[1]  # pour éliminer le drive "C:" sous windows
    return path_sep_in_name.join(os.path.normpath(filename_with_path).split(os.sep)[1:])


def flatten_files(src_path, dest_path, extensions, include_patterns=('*',), exclude_patterns=None, exclude_dirs=None):
    # type: (unicode, unicode, tuple, tuple, tuple, tuple) -> None
    """
    Recopie des fichiers disposés dans une arborescence vers un répertoire dans lequel ils seront tous recopiés
    au même niveau, avec un nouveau nom

    :param src_path: chemin à partir duquel les sous-répertoires seront parcourus et les fichiers listés
    :param dest_path: chemin en sortie dans lequel les fichiers seront tous recopiés, avec un nouveau nom
                        qui tient compte du chemin
    :param extensions: extentions de fichiers à inclure (majuscule ou minuscule)
    :param include_patterns: liste de motifs à inclure pour le nom de fichier après filtrage de l'extension
    :param exclude_patterns: liste de motifs à exclure pour le nom de fichier
    :param exclude_dirs: liste de motifs à exclure pour le nom de répertoire
    :return: None
    """
    if src_path is None:
        raise NameError("src_path doit être défini")
    if dest_path is None:
        raise NameError("dest_path doit être défini")
    if not os.path.isdir(dest_path):
        mkdir_path(dest_path)

    all_rel_file_names = get_all_rel_file_names(src_path, extensions, include_patterns, exclude_patterns, exclude_dirs)
    for one_file in all_rel_file_names:
        # log_write(one_file)
        file_flat_name = make_flat_name(one_file)
        # log_write(file_flat_name)
        src_name = os.path.normpath(src_path + os.sep + one_file)
        dest_name = os.path.join(dest_path, file_flat_name)
        log_write("copy" + ", " + src_name + " -> " + dest_name)
        try:
            copy2(src_name, dest_name)
        except Exception as e:
            log_write("error: " + unicode(e))


def unflatten_files(src_path, dest_path, path_sep_in_name=PATH_SEP_IN_NAME):
    # type: (unicode, unicode, unicode) -> None
    """
    Recopie des fichiers placés dans un répertoire (tous au même niveau) vers une arborescence déduite du nom
    de chaque fichier.
    Le nom du fichier doit donc avoir un format adapté: des noms séparés par le séparateur.
    Si un répertoire n'existe pas, il est créé.

    :param src_path: chemin à partir duquel les fichiers seront listés
    :param dest_path: chemin en sortie dans lequel les fichiers seront tous recopiés et les répertoires créés
    :param path_sep_in_name:
    :return: None
    """
    if src_path is None:
        raise NameError("src_path doit être défini")
    if dest_path is None:
        raise NameError("dest_path doit être défini")
    all_rel_file_names = os.listdir(src_path)
    for one_file in all_rel_file_names:
        # log_write(one_file)
        dest_file_path = os.sep.join(one_file.split(path_sep_in_name))
        # log_write(unicode(rel_path))
        src_name = os.path.normpath(src_path + os.sep + one_file)
        dest_name = os.path.normpath(dest_path + os.sep + dest_file_path)
        log_write("copy" + ", " + src_name + " -> " + dest_name)
        # creation des repertoires jusqu'au répertoire du fichier final, s'il n'existent pas
        # os.path.dirname() permet d'enlever le nom du fichier et de ne conserver que le nom du répertoire
        mkdir_path(os.path.dirname(dest_name))
        # copie du fichier
        copy2(src_name, dest_name)


def trt_LaReunion():
    path_work = r"2004-10-08-La_Reunion"
    path_src_root = r"I:\Photos"
    path_dest_root = r"T:\Photos"
    path_orig = os.path.join(path_src_root, path_work)
    path_flatten = os.path.join(path_dest_root, path_work)
    path_DxO = os.path.join(path_flatten, "DxO_red")

    phase = 2

    if phase == 1:
        mkdir_path(path_flatten)
        copy_files_to_path(path_orig
                           , path_flatten
                           , extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP')
                           , include_patterns=('*',)
                           , exclude_patterns=None)
    if phase == 2:
        # move_files_to_path( path_orig=path_flatten
        #                     , path_dest=path_DxO
        #                     , extensions=None
        #                     , include_patterns=("*DxO*",)
        #                     , exclude_patterns=("*DxO_red*",)
        #                     )
        # rename_files(path_orig=path_DxO
        #              , old_str='DxO_1'
        #              , new_str='DxO'
        #              , extensions=None
        #              , include_patterns=("*DxO_1*",)
        #              , exclude_patterns=None
        #              )
        rm_files(path_orig=path_DxO
                     , extensions=None
                     , include_patterns=("*DxO_2*",)
                     , exclude_patterns=None
                     )


def trt_KadoreFleurs():
    path_work = r"2010-07-17-KadoreFleurs"
    path_src_root = r"I:\Photos"
    path_dest_root = r"T:\Photos"
    path_orig = os.path.join(path_src_root, path_work)
    path_flatten = os.path.join(path_dest_root, path_work)
    path_DxO = os.path.join(path_flatten, "DxO_red")

    phase = 2

    if phase == 1:
        mkdir_path(path_flatten)
        copy_files_to_path(path_orig
                           , path_flatten
                           , extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP')
                           , include_patterns=('*',)
                           , exclude_patterns=None)
    if phase == 2:
        move_files_to_path( path_orig=path_flatten
                            , path_dest=path_DxO
                            , extensions=None
                            , include_patterns=("*DxO*",)
                            , exclude_patterns=("*DxO_red*",)
                            )
        # rename_files(path_orig=path_DxO
        #              , old_str='DxO_1'
        #              , new_str='DxO'
        #              , extensions=None
        #              , include_patterns=("*DxO_1*",)
        #              , exclude_patterns=None
        #              )
        # rm_files(path_orig=path_DxO
        #              , extensions=None
        #              , include_patterns=("*DxO_2*",)
        #              , exclude_patterns=None
        #              )


def trt_USA():
    path_work                       = "2009-05-07-USA\Originaux"
    path_src_root                   = r"I:\Photos"
    path_dest_root                  = r"T:\Photos"
    path_dest_work_root             = os.path.join(path_dest_root, path_work)
    path_orig                       = os.path.join(path_src_root, path_work)
    path_dest_for_flatten           = os.path.join(path_dest_work_root, "flat")
    path_dest_for_rebuild_file_tree = os.path.join(path_dest_work_root, "tree")
    path_dest_for_DxO               = os.path.join(path_dest_work_root, "DxO")

    mkdir_path(path_dest_for_flatten)
    mkdir_path(path_dest_for_rebuild_file_tree)
    mkdir_path(path_dest_for_DxO)
    flatten_files(  path_orig
                  , path_dest_for_flatten
                  , extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP')
                  , include_patterns=('*',)
                  , exclude_patterns=('*DxO*',)
                  )
    # unflatten_files(path_dest_for_flatten, path_dest_for_rebuild_file_tree)


def trt_LaVanoise():
    path_work              = "2010-07-26-Vanoise"
    path_src_root          = r"I:\Photos"
    path_dest_root         = r"T:\Photos"
    path_dest_work_root    = os.path.join(path_dest_root, path_work)
    path_orig              = os.path.join(path_src_root, path_work)
    path_flatten           = os.path.join(path_dest_work_root, "flat")
    path_DxO               = os.path.join(path_dest_work_root, "DxO")

    phase = 2

    if phase == 1:
        flatten_files(  path_orig
                      , path_flatten
                      , extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP')
                      , include_patterns=('*',)
                      , exclude_patterns=('*DxO*',)
                      )
    if phase == 2:
        move_files_to_path( path_orig=path_flatten
                            , path_dest=path_DxO
                            , extensions=None
                            , include_patterns=("*DxO*",)
                            , exclude_patterns=("*DxO_red*",)
                            )
        # rename_files(path_orig=path_DxO
        #              , old_str='DxO_1'
        #              , new_str='DxO'
        #              , extensions=None
        #              , include_patterns=("*DxO_1*",)
        #              , exclude_patterns=None
        #              )
        # rm_files(path_orig=path_DxO
        #              , extensions=None
        #              , include_patterns=("*DxO_2*",)
        #              , exclude_patterns=None
        #              )


def trt_Vacances_Vannes_Emmanuel():
    path_work = r"2016-08-01-Vacances_Vannes_Emmanuel"
    path_src_root = r"I:\Photos"
    path_dest_root = r"T:\Photos"
    path_orig = os.path.join(path_src_root, path_work)
    path_flatten = os.path.join(path_dest_root, path_work)
    path_DxO = os.path.join(path_flatten, "DxO_red")

    phase = 2

    if phase == 1:
        mkdir_path(path_flatten)
        copy_files_to_path(path_orig
                           , path_flatten
                           , extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP')
                           , include_patterns=('*',)
                           , exclude_patterns=None)
    if phase == 2:
        move_files_to_path( path_orig=path_flatten
                            , path_dest=path_DxO
                            , extensions=None
                            , include_patterns=("*DxO*",)
                            , exclude_patterns=("*DxO_red*",)
                            )


def trt_Vacances_Vannes_Maryline():
    path_work = r"2016-08-01-Vacances_Vannes_Maryline"
    path_src_root = r"I:\Photos"
    path_dest_root = r"T:\Photos"
    path_orig = os.path.join(path_src_root, path_work)
    path_flatten = os.path.join(path_dest_root, path_work)
    path_DxO = os.path.join(path_flatten, "DxO_red")

    phase = 2

    if phase == 1:
        mkdir_path(path_flatten)
        copy_files_to_path(path_orig
                           , path_flatten
                           , extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP')
                           , include_patterns=('*',)
                           , exclude_patterns=None)
    if phase == 2:
        move_files_to_path( path_orig=path_flatten
                            , path_dest=path_DxO
                            , extensions=None
                            , include_patterns=("*DxO*",)
                            , exclude_patterns=("*DxO_red*",)
                            )


def trt_local():
    path_work                       = r"test_files"
    path_src_root                   = r"D:\Documents\Projets\Developpements\Python\Directory_flatten"
    path_orig                       = os.path.join(path_src_root, path_work, r"1-in")
    path_dest_root                  = r"D:\Documents\Projets\Developpements\Python\Directory_flatten"
    path_dest_work_root             = os.path.join(path_dest_root, path_work)
    path_dest_for_flatten           = os.path.join(path_dest_work_root, r"2-flat")
    path_dest_for_rebuild_file_tree = os.path.join(path_dest_work_root, r"3-tree")

    mkdir_path(path_dest_for_flatten)
    mkdir_path(path_dest_for_rebuild_file_tree)
    flatten_files(  path_orig
                  , path_dest_for_flatten
                  , extensions=('.txt',)
                  , include_patterns=('*',)
                  , exclude_patterns=('*DxO*',)
                  )
    unflatten_files(path_dest_for_flatten, path_dest_for_rebuild_file_tree)


def trt_Amsterdam():
    path_work                       = "2007-04-10-Amsterdam-Bruxelles"
    path_src_root                   = r"I:\Photos"
    path_dest_root                  = r"T:\Photos"
    path_dest_work_root             = os.path.join(path_dest_root, path_work)
    path_orig                       = os.path.join(path_src_root, path_work)
    path_dest_for_flatten           = os.path.join(path_dest_work_root, "flat")
    path_dest_for_rebuild_file_tree = os.path.join(path_dest_work_root, "tree")
    path_dest_for_DxO               = os.path.join(path_dest_work_root, "DxO")

    mkdir_path(path_dest_for_DxO)
    flatten_files(  path_orig
                  , path_dest_for_flatten
                  , extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP')
                  , include_patterns=('*',)
                  , exclude_patterns=('*DxO*','*red*','resize*')
                  , exclude_dirs=('mary-resize-mail',))
    # unflatten_files(path_dest_for_flatten, path_dest_for_rebuild_file_tree)


def trt_2005_04_24_Bretagne_56():
    path_work                       = "2005-04-24-Bretagne 56"
    path_src_root                   = r"I:\Photos"
    path_dest_root                  = r"T:\Photos"
    path_dest_work_root             = os.path.join(path_dest_root, path_work)
    path_orig                       = os.path.join(path_src_root, path_work)
    path_dest_for_flatten           = os.path.join(path_dest_work_root, "flat")
    path_dest_for_rebuild_file_tree = os.path.join(path_dest_work_root, "tree")
    path_dest_for_DxO               = os.path.join(path_dest_work_root, "DxO")

    mkdir_path(path_dest_for_DxO)
    flatten_files(  path_orig
                  , path_dest_for_flatten
                  , extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP')
                  , include_patterns=('*',)
                  , exclude_patterns=('*DxO*','*red*','resize*')
                  , exclude_dirs=('mary-resize-mail',))
    # unflatten_files(path_dest_for_flatten, path_dest_for_rebuild_file_tree)


def trt_folder(folder_name):
    path_work                       = folder_name
    path_src_root                   = r"I:\Photos"
    path_dest_root                  = r"T:\Photos"
    path_dest_work_root             = os.path.join(path_dest_root, path_work)
    path_orig                       = os.path.join(path_src_root, path_work)
    path_dest_for_flatten           = os.path.join(path_dest_work_root, "flat")
    path_dest_for_rebuild_file_tree = os.path.join(path_dest_work_root, "tree")
    path_dest_for_DxO               = os.path.join(path_dest_work_root, "DxO")

    mkdir_path(path_dest_for_DxO)
    flatten_files(  path_orig
                  , path_dest_for_flatten
                  , extensions=('.JPG', '.JPEG', '.PEF', '.NEF', '.RW2', '.DOP')
                  , include_patterns=('*',)
                  , exclude_patterns=('*DxO*','*red*','resize*')
                  , exclude_dirs=('mary-resize-mail',))
    # unflatten_files(path_dest_for_flatten, path_dest_for_rebuild_file_tree)


def move_DxO_files(folder_name):
    move_files_to_path(r"T:\Photos" + os.path.sep + folder_name + os.path.sep + r"flat"
                    , r"T:\Photos" + os.path.sep + folder_name + os.path.sep + r"DxO"
                    , extensions=None
                    , include_patterns=("*DxO*",)
                    , exclude_patterns=None
                    )


#####################
# programme principal
#####################
if __name__ == "__main__":
    """
    Programme qui fournit des exemples d'appel de la fonction flatten_files()
    """
    log_init()

    # path_root = r"I:\Photos\2010-07-26-Vanoise"
    # path_orig = os.path.join(path_root, "1-in")
    # path_dest_for_flatten = os.path.join(path_root, "2-flat")
    # path_dest_for_rebuild_file_tree = os.path.join(path_root, "3-rebuild_tree")
    # path_dest_for_move = os.path.join(path_root, "DxO")

    # path_root = r"I:\Photos\2010-07-17-KadoreFleurs"
    # path_orig = path_root
    # path_dest_for_flatten = r"T:\Photos\2010-07-17-KadoreFleurs"
    # path_dest_for_rebuild_file_tree = os.path.join(path_dest_for_flatten, "3-rebuild_tree")
    # path_dest_for_move = os.path.join(path_root, "DxO")


    # trt_local()
    # trt_USA()
    # trt_LaReunion()
    # trt_KadoreFleurs()
    # trt_LaVanoise()
    # trt_Vacances_Vannes_Emmanuel()
    # trt_Vacances_Vannes_Maryline()
    # trt_Amsterdam()
    # trt_2005_04_24_Bretagne_56()
    # trt_folder("2005-07-13-VacancesHautesAlpesQueyras")
    # move_DxO_files(r"2007-04-10-Amsterdam-Bruxelles")
    # move_DxO_files(r"2005-04-24-Bretagne 56")
    move_DxO_files("2005-07-13-VacancesHautesAlpesQueyras")
    log_exit()
