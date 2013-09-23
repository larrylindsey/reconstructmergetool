#!/usr/bin/env python
import sys, re, openpyxl
import reconstructmergetool as rmt

# Gathering excel info
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
        for contour in [cont.name.lower() for cont in section.contours]:
            for exp in filterBank:
                if exp.match(contour) != None:
                    dendrites.append(contour)
    return sorted(list(set(dendrites)))

def buildProtrusionDictionary(series, dendrite_list): #=== check if adding for all dendrites
    '''Returns a dictionary of a list of protrusions for each dendrite in dendrite list'''
    protDict = {}
    dendrite_list = list(set([dendrite.lower() for dendrite in dendrite_list])) # lowercase all dendrites
    for dendrite in dendrite_list:
        if dendrite not in protDict:
            protDict[dendrite] = []
            for section in series.sections:
                for contour in section.contours:
                    if processExp(dendrite+'p##').match(contour.name): # find all the d##p## contours
                        if contour.name not in protDict[dendrite]:
                            protDict[dendrite].append(contour.name)
            protDict[dendrite].sort()
    return protDict
            
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
#     list_of_expressions = list(input('Enter list of expressions for filter: '))
    list_of_expressions = ['d04$', 'd05$', 'd06$']
#     path_to_series = str(input('Enter path to series: '))
    path_to_series = '/home/michaelm/Documents/Test Series/BBCHZ/BBCHZ.ser'
#     path_to_workbook = str(input('Enter path to template workbook: '))
    path_to_workbook = '/home/michaelm/Documents/Test Series/template.xlsx'
    workbook = openpyxl.Workbook()
    # 1) Build filter bank
    filterBank = buildFilterBank(list_of_expressions)
    # 2) Load series
    series = rmt.getSeries(path_to_series)
    # 3) Build dendrite list
    dendriteList = buildDendriteList(series, filterBank)
    protDict = buildProtrusionDictionary(series, dendriteList)
    # 4) Import template columns
    template = loadTemplate(path_to_workbook)
    # 5) Build sheet for each dendrite
    addDendriteSheets(workbook, series.name, template, dendriteList)
    addProtrusions(workbook, protDict)
    # 6) Add protrusions to dendrite sheets
    # 7) Save
    save_path = input('Enter path to save xl file: ')
    workbook.save(save_path)

# main()



