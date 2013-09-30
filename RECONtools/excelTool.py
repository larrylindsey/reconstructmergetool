#!/usr/bin/env python
import sys, re, openpyxl
import reconstructmergetool as rmt
# === implement some classes?
# Gathering excel info

def processExp(exp): #===
        # Need to cap at end? $
        '''Converts a filter string from RECONSTRUCT format to python regexp format'''
        exp = exp.replace('*', '.')
        exp = exp.replace('?', '[a-z]') #=== "? matches any single character" (numbers included?)
        exp = exp.replace('#', '[0-9]')
        return re.compile( str(exp),re.I ) # re.I (Ignore Case)

class excelWorkbook(openpyxl.Workbook):
    def __init__(self):
        openpyxl.Workbook.__init__(self)
        
        self.columns = ['p', 'sp', 'sph', 'cfa']
        self.objectDetails = ['object name','start', 'end', 'count', 'surface area', 'flat area', 'volume']
        
        self.dendriteFilter = None #===
        self.dendriteChildFilter = None #===
        self.dendriteDict = None
        self.protrusionChildCount = None # determines spacing for excel output
    
        self.protrusionExp = re.compile('p[0-9]{2}$')
        self.childExp = re.compile('[a-z]{1,5}[0-9]{2}[a-z]{0,5}$')
        
    def getDendriteDict(self, series):
        self.dendriteDict = series.getDendriteHierarchy()
    
    def writeColumns(self, sheet): #===
        columnNo = 0
        for detail in self.objectDetails:
            sheet.cell(row=0, column=columnNo).value = str(detail)
            columnNo+=1
            
    def writeProtrusions(self, series_name):
        # check dendriteDict for all protrusions
        for dendrite in self.dendriteDict:
            
            # Add protrusions to a list
            protrusionDict = {} # build list of protrusions
            for child in self.dendriteDict[dendrite]: #===
                if self.protrusionExp.match(child) != None: # if is a protrusion
                    protrusionDict[child] = self.dendriteDict[dendrite][child]['count']
            
            # Create sheets for each dendrite that contains a protrusion
            if len(protrusionDict) > 0:
                self.create_sheet(title=str(series_name+' '+dendrite))
                sheet = self.get_sheet_by_name(series_name+' '+dendrite)
                
            # Sort protrusions and determine number of spaces to add after
            row = 1 # row in current excel sheet

            for protrusion in sorted(protrusionDict.items(), key=lambda x: (x[1],x[0])):  # sort by value then key   
                spaces = 0
                if protrusion in self.protrusionChildCount[dendrite]:
                    spaces = int(self.protrusionChildCount[dendrite][protrusion])-1
                # add protrusion to sheet
                sheet.cell(row=row, column=0).value = str(dendrite+protrusion[0])
                
                row+=1
                # add spaces if needed
                while spaces != 0:
                    sheet.cell(row=row, column=0).value = ''
                    spaces-=1
                    row+=1
    
#     def importTemplateFromWorkbook(self, path_to_workbook):
#         '''Returns the active sheet from workbook to serve as a template for the columns'''
#         workbook = openpyxl.load_workbook(path_to_workbook)
#         self.template = workbook.get_active_sheet()
           
#     def importColumns(self, worksheet):
#         '''Writes columns to sheet as per template'''
#         for col in range( len(self.template.columns) ):
#             style = self.template.columns[col].style
#             worksheet.cell(row=0, column=col).value = self.template.columns[col].value
#             worksheet.cell(row=0, column=col).style.alignment = style.alignment
#             worksheet.cell(row=0, column=col).style.borders = style.borders
#             worksheet.cell(row=0, column=col).style.fill = style.fill
#             worksheet.cell(row=0, column=col).style.font = style.font
#             worksheet.cell(row=0, column=col).style.protection = style.protection
#             worksheet.cell(row=0, column=col).style.number_format = style.number_format
#             worksheet.cell(row=0, column=col).value = self.columns[col]

    def buildFilterBank(self, list_of_expressions):
        '''Turns a list of expressions into a list of regular expressions for filtering'''
        bank = []
        for exp in list_of_expressions:
            exp = processExp( exp )
            bank.append( exp )
        self.dendriteFilter = bank
            
    def getProtrusionChildCount(self):
        denDict = self.dendriteDict
        outDict = {}
        for dendrite in denDict:
            outDict[dendrite[0:3]] = {}
            highestSubChild = '' # determines how many excel rows this protrusion requires
            for child in denDict[dendrite]:
                if self.childExp.match( child ) != None: # if child has a sub child (i.e. d07c16a, d07c16b)
                    protrusionNo = child[-3:len(child)-1]
                    if child[-1] > highestSubChild:
                        highestSubChild = child[-1]
            if highestSubChild != '':
                outDict[dendrite[0:3]]['p'+protrusionNo] = ord(highestSubChild)-96 # position in alphabet = number of row required
        self.protrusionChildCount = outDict