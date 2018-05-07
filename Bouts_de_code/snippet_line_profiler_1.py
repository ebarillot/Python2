# coding=utf-8

# A lancer dans une console Anaconda avec:
# kernprof -v -l script_to_profile.py
# ou
# kernprof -v -l script_to_profile.py
#  puis
# python -m line_profiler snippet_line_profiler_1.py.lprof
@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a


if __name__ == '__main__':
    my_func()
