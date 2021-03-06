# coding=utf-8
"""

Exemple adapté de cette page:
https://pymotw.com/2/multiprocessing/mapreduce.html

"""

from __future__ import print_function, unicode_literals

import codecs
import multiprocessing
import string
from map_reduce_simple import SimpleMapReduce


# astuce pour que la fonctions tramsnmise à Pool.map() puisse recevoir plusieurs arguments:
# elle reçoit un tuple qui contient plusieurs champs
def file_to_words((filename, enc)):
    """Read a file and return a sequence of (word, occurances) values.
    """
    STOP_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if', 'in',
        'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the', 'to', 'with',
        }
    # TR = string.maketrans(string.punctuation, ' ' * len(string.punctuation))  # pour str
    unicode_punctuation_map = dict((ord(char), None) for char in string.punctuation)    # pour unicode

    print(multiprocessing.current_process().name, 'reading', filename)
    output = []

    # with open(filename, 'r') as f:  # t pour text mode (default), par opposition à b pour binary mode
    #     for line in f:
    #         line = _line.decode('utf8')
    with codecs.open(filename, 'r', encoding=enc) as f:  # pas besoin de spécifier t ou b dans le mode d'ouverture
        for line in f:
            if line.lstrip().startswith('..'):  # Skip rst comment lines
                continue
            elif line.lstrip().startswith('#'):  # Skip # comment lines
                continue
            # line = line.translate(TR)  # Strip punctuation pour string
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

    # on fabrique une liste de tuples, chaque tuple
    # contient plusieurs champs qui correspondent aux
    # arguments passés à la fonction mappée par multiprocessing.Pool.map()
    # Ici, on fabrique une liste de tuple (nom de fichier, encodage du fichier)
    # au moment où on veut exécuter la fonction
    inputs = zip(input_files, ['utf8']*len(input_files))

    mapper = SimpleMapReduce(file_to_words, count_words, num_workers=4)
    word_counts = mapper(inputs=inputs)
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
Plante :

Traceback (most recent call last):
  File "C:\Program Files\JetBrains\PyCharm Community Edition 2017.2.3\helpers\pydev\pydevd.py", line 1664, in <module>
    main()
  File "C:\Program Files\JetBrains\PyCharm Community Edition 2017.2.3\helpers\pydev\pydevd.py", line 1658, in main
    globals = debugger.run(setup['file'], None, None, is_module)
  File "C:\Program Files\JetBrains\PyCharm Community Edition 2017.2.3\helpers\pydev\pydevd.py", line 1068, in run
    pydev_imports.execfile(file, globals, locals)  # execute the script
  File "C:/Users/emmanuel_barillot/Documents/Developpements/Python2/Multiprocessing/map_reduce_counting_words.py", line 48, in <module>
    word_counts = mapper(inputs=input_files)
  File "C:\Users\emmanuel_barillot\Documents\Developpements\Python2\Multiprocessing\map_reduce_simple.py", line 54, in __call__
    map_responses = self.pool.map(self.map_func, inputs, chunksize=chunksize)
  File "C:\ProgramData\Anaconda2\lib\multiprocessing\pool.py", line 251, in map
    return self.map_async(func, iterable, chunksize).get()
  File "C:\ProgramData\Anaconda2\lib\multiprocessing\pool.py", line 567, in get
    raise self._value
TypeError: unhashable type: 'list'

==> ATTENTION, peut se produire avec la directive suivante:
from __future__ import unicode_literals


ATTENTION aussi avec unicode et la fonction unicode.translate():
elle ne fonctionne pas comme string.translate(), il n'y a pas de fonction unicode.maketrans()


'''