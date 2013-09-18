#!/usr/bin/env python
from xlrd import open_workbook
from xlwt import Workbook, Worksheet
import sys, re

class myWorksheet:
    def __init__(self, sheet):
        self.sheet = sheet
        self.filterBank = []
        
    def buildFilterBank(self, list_of_expressions):
        '''Turns a list of expression into a list of regular expressions for filtering'''
        bank = []
        for exp in list_of_expressions:
            exp = self.processExp( exp )
            bank.append( exp )
        return bank

    def processExp(self, exp ): #===
        # Need to cap at end? $
        '''Converts filter from RECONSTRUCT format to python regexp format'''
        exp = exp.replace('*', '.')
        exp = exp.replace('?', '[a-z]') #=== "? matches any single character" (numbers included?)
        exp = exp.replace('#', '[0-9]')
        return re.compile( str(exp),re.I ) # re.I (Ignore Case)

    def buildProtList(self, series, filterBank):
        '''Returns a list of contour names from series, specified by filterBank'''
        protList = []
        for section in series.sections:
            for contour in [cont.name for cont in section.contours]:
                for exp in filterBank:
                    if exp.match(contour) != None:
                        protList.append(contour)
        return list(set(protList))

    def buildProtDict(self, protList):
        '''Creates a dictionary of protrusion names, each associated with a list of objects representing data'''
        protDict = {}
        for prot in protList:
            protDict[prot] = []
        return protDict

    def importColumns(self, template):
        columns = []
        for col in range( template.ncols ):
            columns.append( str(template.cell(0,col).value) )
        return columns

    def writeColumns(self, columns):
        for col in range( len(columns) ):
            self.sheet.write(0,col,columns[col])
