# coding=utf-8
# from __future__ import print_function, unicode_literals

import multiprocessing
import string
from map_reduce_simple import SimpleMapReduce


def file_to_words(filename):
    """Read a file and return a sequence of (word, occurances) values.
    """
    STOP_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if', 'in',
        'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the', 'to', 'with',
        }
    TR = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

    print(multiprocessing.current_process().name, 'reading', filename)
    output = []

    with open(filename, 'rt') as f:
        for line in f:
            if line.lstrip().startswith('..'):  # Skip rst comment lines
                continue
            line = line.translate(TR)  # Strip punctuation
            for word in line.split():
                word = word.lower()
                if word.isalpha() and word not in STOP_WORDS:
                    output.append((word, 1))
    return output


def count_words(item):
    """Convert the partitioned data for a word to a
    tuple containing the word and the number of occurances.
    """
    word, occurances = item
    return word, sum(occurances)


def do_calculation(data):
    return data * 2


def do_append(data):
    return data+'_'


if __name__ == '__main__':
    import operator
    import glob

    input_files = glob.glob('README.txt')
    # input_files = ['README.txt']

    mapper = SimpleMapReduce(file_to_words, count_words, num_workers=4)
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

'''