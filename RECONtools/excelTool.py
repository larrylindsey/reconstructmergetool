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
        
        self.dendriteFilter = []
        self.dendriteChildFilter = []
        self.dendriteDict = None
        
    def getDendriteDict(self, series):
        self.dendriteDict = series.getObjectHierarchy(*series.getObjectLists())
            
    def writeWorkbook(self, series_name):
        for dendrite in self.dendriteDict:
            # Create sheet if not in filter and has protrusions
            if dendrite not in self.dendriteFilter and len(self.dendriteDict[dendrite].children) > 0:
                self.create_sheet(title=series_name+' '+dendrite)
                sheet = self.get_sheet_by_name(series_name+' '+dendrite)
                
                row = 0
                column = 0
            
                # PROTRUSIONS
                # ---1) make list of protrusions names (sorted by start index)
                sorted_prots = sorted([prot for prot in self.dendriteDict[dendrite]], key=lambda rObject: rObject.start)
                prot_spacing = self.getProtrusionSpacesCount()
                # ---2) write protrusions and data to cells
                sheet.cell(row=row, column=column).value = 'Protrusion Name'
                sheet.cell(row=row, column=column+1).value = 'Start'
                sheet.cell(row=row, column=column+2).value = 'End'
                sheet.cell(row=row, column=column+3).value = 'Count'
                
                row+=1
                for prot in sorted_prots:
                    sheet.cell(row=row, column=column).value = prot.name
                    sheet.cell(row=row, column=column+1).value = prot.start
                    sheet.cell(row=row, column=column+2).value = prot.end
                    sheet.cell(row=row, column=column+3).value= prot.count
                    if prot_spacing[prot.name] > 0:
                        row+=prot_spacing[prot.name]
                    row+=1

    def buildFilterBank(self, list_of_expressions):
        '''Turns a list of expressions into a list of regular expressions for filtering'''
        bank = []
        for exp in list_of_expressions:
            exp = processExp( exp )
            bank.append( exp )
        self.dendriteFilter = bank
            
    def getProtrusionSpacesCount(self):
        '''Protrusions with more than 1 subtrace require extra spacing in the excel sheet. This function
        determines how much spacing is required for that protrusion'''
        indicator = re.compile('[0-9]{2}[a-z]{1}') # Indicates that there are multiple subchildren
        protrusionSpacing = {}
        denDict = self.dendriteDict
        for dendrite in denDict:
            for protrusion in denDict[dendrite]:
                extraSpaces = 0
                for child in protrusion:
                    if indicator.match(child.name[-3:]) and ord(child.name[-1])-97 > extraSpaces:
                        extraSpaces = ord(child.name[-1])-97
                protrusionSpacing[protrusion.name] = extraSpaces
        return protrusionSpacing