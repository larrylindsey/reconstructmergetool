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
    
    # return a dictionary of protrusions and their require spacing for given dendrite rObject
    def getProtrusionSpacing( dendrite_rObject ):
        prot_spacing = {}
        for protrusion in dendrite_rObject.children:
            spacing = 0
            for child in protrusion:
                # If child has subchildren, adjust spacing
                if child.name[-1].isalpha() and ord(child.name[-1]) - 97 > spacing:
                    spacing = ord(child.name[-1])-97
            prot_spacing[protrusion.name] = spacing
        return prot_spacing
    
    # write protrusions and their data to a sheet
    def writeProtrusions(dendrite_rObj, sheet):
        prot_spacing = getProtrusionSpacing(wkbk.dendriteDict[dendrite_rObj.name])
        prot_by_start = sorted([prot for prot in wkbk.dendriteDict[dendrite_rObj.name].children], key=lambda rObject: rObject.start)
        
        row=0
        column=0
        # Write protrusion column headers
        sheet.cell(row=row, column=column).value = 'Protrusion Name'
        sheet.cell(row=row, column=column+1).value = 'Start'
        sheet.cell(row=row, column=column+2).value = 'End'
        sheet.cell(row=row, column=column+3).value = 'Count'
        sheet.cell(row=row, column=column+4).value = 'Surface Area'
        sheet.cell(row=row, column=column+5).value = 'Flat Area'
        sheet.cell(row=row, column=column+6).value = 'Volume'
        
        # Write protrusions and data
        for prot in prot_by_start:
            row += 1
            sheet.cell(row=row, column=column).value = prot.name
            sheet.cell(row=row, column=column+1).value = prot.start
            sheet.cell(row=row, column=column+2).value = prot.end
            sheet.cell(row=row, column=column+3).value = prot.count
            sheet.cell(row=row, column=column+4).value = prot.surfacearea
            sheet.cell(row=row, column=column+5).value = prot.flatarea
            sheet.cell(row=row, column=column+6).value = prot.volume
            row += prot_spacing[prot.name]
        
    # get all trace types in a dendrite hierarchy
    def getTraceTypes(dendrite_rObj):
        trace_types = []
        for protrusion in dendrite_rObj.children:
            for trace in protrusion.children:
                # convert trace name to regular expression
                trace_expression = ''
                for character in trace.name:
                    if character.isdigit():
                        character = '[0-9]'
                    trace_expression+=character
                if trace_expression[-1].isalpha():
                    trace_expression = trace_expression[:-1]
                # append to trace_types list
                trace_types.append(trace_expression)
        # return a set of all trace_types in a dendrite
        return sorted(list(set(trace_types)))
    
    def writeWorkbook():
        # for each dendrite in the dictionary, create a sheet and fill with data
        for dendrite in wkbk.dendriteDict:
            # Create sheet
            sheet_name = 'BBCHZ '+wkbk.dendriteDict[dendrite].name
            wkbk.create_sheet(title=sheet_name)
            sheet = wkbk.get_sheet_by_name(sheet_name)
            
            # Protrusion spacing
            prot_spacing = getProtrusionSpacing(wkbk.dendriteDict[dendrite])
            
            # Write protrusion data and column headers
            writeProtrusions( wkbk.dendriteDict[dendrite], sheet )
            types = getTraceTypes( wkbk.dendriteDict[dendrite] )
            
            sorted_prots = sorted([prot for prot in wkbk.dendriteDict[dendrite]], key=lambda rObject: rObject.start)
            
            # Write traces
            column = 8
            # Each trace type
            for tType in types:
                # Column headers
                sheet.cell(row=0, column=column).value = 'Object Name'
                sheet.cell(row=0, column=column+1).value = 'Start'
                sheet.cell(row=0, column=column+2).value = 'End'
                sheet.cell(row=0, column=column+3).value = 'Count'
                sheet.cell(row=0, column=column+4).value = 'Surface Area'
                sheet.cell(row=0, column=column+5).value = 'Flat Area'
                sheet.cell(row=0, column=column+6).value = 'Volume'
                row = 1 # reset row for each trace type
                for protrusion in sorted_prots:
                    protrusionChildren = sorted([child for child in protrusion if re.compile(tType).match(child.name)])
                    if len(protrusionChildren) == 0: # protrusion has no children, increment to next prot
                        row+=1
                        row+=prot_spacing[protrusion.name]
                    for child in protrusionChildren:
                        sheet.cell(row=row,column=column).value = child.name
                        sheet.cell(row=row,column=column+1).value = child.start
                        sheet.cell(row=row,column=column+2).value = child.end
                        sheet.cell(row=row,column=column+3).value = child.count
                        sheet.cell(row=row,column=column+4).value = child.surfacearea
                        sheet.cell(row=row,column=column+5).value = child.flatarea
                        sheet.cell(row=row,column=column+6).value = child.volume
                        row+=1
                column+=8


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