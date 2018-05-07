# coding=utf-8

from memory_profiler import memory_usage


# define a simple function
def f(a, n=100):
    import time
    time.sleep(2)
    b = [a] * n
    time.sleep(1)
    return b


# usage mémoire par l'interpréteur lui même (pid=-1)
mem_usage = memory_usage(-1, interval=.2, timeout=1)
print(mem_usage)


memory_usage((f, (1,), {'n' : int(1e6)}))
# This will execute the code f(1, n=int(1e6)) and return the memory consumption during this execution.

