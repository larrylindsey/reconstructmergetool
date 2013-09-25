#!/usr/bin/env python
import sys, re, openpyxl
import reconstructmergetool as rmt
# === implement some classes?
# Gathering excel info

list_of_dendrite_children = ['p##', 'cfa##', 'c##']

def loadTemplate(path_to_workbook):
    '''Returns a openpyxl.sheet for the sheet named "Template" in the workbook.'''
    wkbk = openpyxl.load_workbook(path_to_workbook)
    template = wkbk.get_active_sheet()
    return template

def importColumns(xl_template):
    '''Builds/returns a list of columns found in template'''
    columns = []
    for col in range( len(xl_template.columns) ):
        columns.append( xl_template.cell(row=0,column=col) )
    return columns

def processExp(exp): #===
    # Need to cap at end? $
    '''Converts a filter string from RECONSTRUCT format to python regexp format'''
    exp = exp.replace('*', '.')
    exp = exp.replace('?', '[a-z]') #=== "? matches any single character" (numbers included?)
    exp = exp.replace('#', '[0-9]')
    return re.compile( str(exp),re.I ) # re.I (Ignore Case)

def buildFilterBank(list_of_expressions):
    '''Turns a list of expressions into a list of regular expressions for filtering'''
    bank = []
    for exp in list_of_expressions:
        exp = processExp( exp )
        bank.append( exp )
    return bank

# Gather info from series
def buildDendriteList(series, filterBank):
    '''Returns a list of contour names from series, specified by filterBank'''
    dendrites = []
    for section in series.sections:
        for contour in [cont.name for cont in section.contours]:
            for exp in filterBank:
                if exp.match(contour) != None:
                    dendrites.append(contour)
    return sorted(list(set(dendrites)))
      
# Creating excel docs
def writeColumns(worksheet, list_of_columns):
    '''Writes columns to specified worksheet.'''
    for col in range( len(list_of_columns)):
        style = list_of_columns[col].style
        worksheet.cell(row=0, column=col).value = list_of_columns[col].value
        worksheet.cell(row=0, column=col).style.alignment = style.alignment
        worksheet.cell(row=0, column=col).style.borders = style.borders
        worksheet.cell(row=0, column=col).style.fill = style.fill
        worksheet.cell(row=0, column=col).style.font = style.font
        worksheet.cell(row=0, column=col).style.protection = style.protection
        worksheet.cell(row=0, column=col).style.number_format = style.number_format

def addProtrusions(workbook, protDict):
    sheetNames = workbook.get_sheet_names()
    for dendrite in protDict:
        sheet = workbook.get_sheet_by_name(str([sheetName for sheetName in sheetNames if dendrite in sheetName][0]))
        row = 1
        for protrusion in protDict[dendrite]:
            sheet.cell(row=row, column=0).value = protrusion
            row+=1
            
def addDendriteSheet(workbook, series_name, xl_template, dendrite):
    '''Adds a worksheet to workbook for the specific dendrite. Formatted to template.'''
    worksheet = workbook.create_sheet( title=series_name+' '+dendrite )
    writeColumns(worksheet, importColumns(xl_template))
    
def addDendriteSheets(workbook, series_name, xl_template, dendrite_list):
    '''Adds a sheet to workbook for each dendrite of dendrite_list.'''
    for dendrite in dendrite_list:
        addDendriteSheet(workbook, series_name, xl_template, dendrite)

def main():
    list_of_dendrites = ['d06','d07','d14']
    series = rmt.getSeries('/home/michaelm/Documents/Test Series/BBCHZ/BBCHZ.ser')
