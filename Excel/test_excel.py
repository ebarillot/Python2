#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
# Python 2.7
 
import win32com.client

file_xls = r"essai1.xlsx"
sheet = 1

e = win32com.client.Dispatch('Excel.Application')
e.Visible = 1
wb = e.Workbooks.Open(file_xls)
nbrows = wb.Sheets(sheet).UsedRange.Rows.Count
nbcols = wb.Sheets(sheet).UsedRange.Columns.Count

print ("rows: %d " % nbrows)
print ("cols: %d " % nbcols)

row1, col1 = 1, 1
row2, col2 = nbrows-row1+1, nbcols-col1+1
print ("row1, col1: {} {}, row2, col2: {} {}".format(row1, col1, row2, col2))
cell1 = wb.Worksheets(sheet).Cells(row1, col1)
cell2 = wb.Worksheets(sheet).Cells(row2, col2)

print (wb.Worksheets(sheet).Range(cell1, cell2).Value)

##wb.Worksheets(sheet).Cells(row2+1,1).Value = "Hello" 


##wb.Close(SaveChanges=0)
##del wb
##del e
