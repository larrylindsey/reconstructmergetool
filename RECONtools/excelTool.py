#!/usr/bin/env python
import xlrd, xlwt, sys, os, re
from xlutils import copy, save

def buildFilterBank(list_of_expressions):
    '''Turns a list of expression into a list of regular expressions for filtering'''
    bank = []
    for exp in list_of_expressions:
        exp = processExp( exp )
        bank.append( exp )
    return bank

def processExp( exp ): #===
    # Need to cap at end? $
    '''Converts filter from RECONSTRUCT format to python regexp format'''
    exp = exp.replace('*', '.')
    exp = exp.replace('?', '[a-z]') #=== "? matches any single character" (numbers included?)
    exp = exp.replace('#', '[0-9]')
    return re.compile( str(exp),re.I ) # re.I (Ignore Case)

def buildProtList(series, filterBank):
    '''Returns a list of contour names from series, specified by filterBank'''
    protList = []
    for section in series.sections:
        for contour in [cont.name for cont in section.contours]:
            for exp in filterBank:
                if exp.match(contour) != None:
                    protList.append(contour)
    return list(set(protList))

def buildProtDict(protList):
    '''Creates a dictionary of protrusion names, each associated with a list of objects representing data'''
    protDict = {}
    for prot in protList:
        protDict[prot] = []
    return protDict

