# coding=utf-8

"""
Variante de Multiprocessing/map_reduce_counting_words.py
qui utilise le module functools.partial pour passer plusieurs arguments
à la fonction mappée:
  -> partial permet de passer une fonction partiellement évaluée au lieu
  de construire une liste de tuples comme arguments à la fonction mappée
  quand on veut l'exécuter
  -> fonctionne quand on peut rendre constants tous les arguments sauf 1
     pendant le travail qui est effectué par la fonction mappée

Exemple tiré de:
http://python.omics.wiki/multiprocessing_map/multiprocessing_partial_function_multiple_arguments
"""

from __future__ import print_function, unicode_literals

import codecs
import multiprocessing
import string
from map_reduce_simple import SimpleMapReduce
from functools import partial


# la focntion mappée reçoit plusieurs arguments
def file_to_words(filename, enc):
    """Read a file and return a sequence of (word, occurances) values.
    """
    STOP_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if', 'in',
        'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the', 'to', 'with',
        }
    unicode_punctuation_map = dict((ord(char), None) for char in string.punctuation)    # pour unicode

    print(multiprocessing.current_process().name, 'reading', filename)
    output = []

    with codecs.open(filename, 'r', encoding=enc) as f:  # pas besoin de spécifier t ou b dans le mode d'ouverture
        for line in f:
            if line.lstrip().startswith('..'):  # Skip rst comment lines
                continue
            elif line.lstrip().startswith('#'):  # Skip # comment lines
                continue
            line = line.translate(unicode_punctuation_map)  # Strip punctuation pour unicode
            for word in line.split():
                word = word.lower()
                if word.isalpha() and word not in STOP_WORDS:
                    output.append((word, 1))
    return output


def count_words(item):
    """Convert the partitioned data for a word to a
    tuple containing the word and the number of occurances.
    """
    word, occurences = item
    return word, sum(occurences)


def do_calculation(data):
    return data * 2


def do_append(data):
    return data+'_'


if __name__ == '__main__':
    import operator
    import glob

    input_files = glob.glob('*.py') # marche
    # input_files = ['README.txt'] # marche aussi

    file_to_words_partial = partial(file_to_words, enc='utf8')  # file_to_words_partial n'a plus qu'un argument

    mapper = SimpleMapReduce(file_to_words_partial, count_words, num_workers=4)
    word_counts = mapper(inputs=input_files)
    word_counts.sort(key=operator.itemgetter(1))
    word_counts.reverse()

    print('\nTOP 20 WORDS BY FREQUENCY\n')
    top20 = word_counts[:20]
    longest = max(len(word) for word, count in top20)
    for word, count in top20:
        print('%-*s: %5s' % (longest + 1, word, count))

    # inputs = list(range(10))
    # print('Input   :', inputs)
    # mapper = SimpleMapReduce(do_calculation, count_words, num_workers=4)
    # result = mapper(inputs=inputs)
    # print('result   :', result)

    # inputs = ['a','b','c']
    # print('Input   :', inputs)
    # mapper = SimpleMapReduce(do_append, count_words, num_workers=4)
    # result = mapper(inputs=inputs)
    # print('result   :', result)


# le b devant la chaine multi ligne sert à neutraliser les \ qui apparaissent dans les chemins
b'''

==> ATTENTION TypeError: unhashable type: 'list' peut se produire avec la directive suivante:
from __future__ import unicode_literals


ATTENTION aussi avec unicode et la fonction unicode.translate():
elle ne fonctionne pas comme string.translate(), il n'y a pas de fonction unicode.maketrans()


'''