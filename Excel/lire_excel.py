#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
# Python 2.7
 
import win32com.client
 
#############################################################################
class Excelfacile(object):
 
    def __init__(self, fichier=""):
 
        self.excel = win32com.client.Dispatch('Excel.Application')
        self.fichier = fichier
        if fichier=="":
            self.wb = self.excel.Workbooks.Add()
        else:
            self.wb = self.excel.Workbooks.Open(fichier)
 
    def nbrows(self, sheet=1):
        """retourne le nombre total de ligne utilisées"""
        return self.wb.Sheets(sheet).UsedRange.Rows.Count
 
    def nbcols(self, sheet=1):
        """retourne le nombre total de colonnes utilisées"""
        return self.wb.Sheets(sheet).UsedRange.Columns.Count
 
    def listeval(self, sheet=1, row1=1, col1=1, row2=None, col2=None):
        """retourne la liste des valeurs du rectangle [[row1,col1][row2,col2]]
           de la feuille 'sheet' 
           si row2 et/ou col2 = None, on prend la dernière ligne et/ou colonne   
        """        
        cell1 = self.wb.Worksheets(sheet).Cells(row1, col1)
        if row2==None:
            row2 = self.nbrows(sheet) - row1 + 1
        if col2==None:
            col2 = self.nbcols(sheet) - col1 + 1
        cell2 = self.wb.Worksheets(sheet).Cells(row2, col2)
        return self.wb.Worksheets(sheet).Range(cell1, cell2).Value
 
    def save(self, nouvfichier="", ):
        if nouvfichier=="":
            self.wb.Save()
        else:
            self.fichier = nouvfichier
            self.wb.SaveAs(nouvfichier)
 
    def close(self):
        self.wb.Close(SaveChanges=0)
        del self.excel
 
#############################################################################
if __name__ == "__main__":
 
    # chargement    
    excel = Excelfacile(r"essai1.slk")
 
    # affichage des valeurs
    for ligne in excel.listeval():
        print ligne
 
    # enregistrement sous le format xls
    excel.save(r"essai1.xls")
 
    # fermeture
    excel.close()
