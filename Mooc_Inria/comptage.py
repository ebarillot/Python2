import os
os.chdir(r'D:\Emmanuel\2015-10_MOOC_Python')

def comptage(in_filename, out_filename):
    n_lines = n_words = n_char = 0
    with open(in_filename, "r") as entree:
        with open(out_filename, "w") as sortie:
            for i, line in enumerate(entree):
                sortie.write("{}:{}:{}:{}".format(i+1,len(line.split()),len(line),line))
                n_lines += 1
                n_words += len(line.split())
                n_char += len(line)
            sortie.write("{}:{}:{}\n".format(n_lines,n_words,n_char))


comptage('romeo_and_juliet.txt','romeo_and_juliet_2.txt')
