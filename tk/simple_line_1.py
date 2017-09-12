#!/usr/bin/python
# -*- coding: utf-8 -*-

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from Tkinter import *

root = Tk()
root.title('Very simple Tkinter line')
canvas_1 = Canvas(root, width=300, height=200,
                  background="#ffffff")
canvas_1.grid(row=0, column=0)
canvas_1.create_line(10, 20, 50, 70)
root.mainloop()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
