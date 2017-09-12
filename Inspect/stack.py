#!/usr/bin/python
# -*- coding: utf-8 -*-
import inspect

print __file__
c = inspect.currentframe()
print c.f_lineno

def hello_1():
    print inspect.stack
    # ?? what file called me in what line?

# hello_1()


def hello_2():
    (frame, filename, line_number,
     function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
    print(frame, filename, line_number, function_name, lines, index)

# hello_2()

def hello_3():
    frame,filename,line_number,function_name,lines,index = inspect.stack()[1]
    print(frame,filename,line_number,function_name,lines,index)

hello_3()
