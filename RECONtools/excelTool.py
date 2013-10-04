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

def getTraceTypes(dendrite_rObj):
    '''Returns a list of all the trace types in a dendrite rObject (alphabetical order)'''
    trace_types = []
    for protrusion in dendrite_rObj.children:
        for trace in protrusion.children:
            trace_types.append(trace.type)
    return sorted(list(set(trace_types)))

def getProtrusionSpacing( dendrite_rObject ):
    '''Returns a dictionary of protrusion keys and values representing how much extra spacing is needed in the sheet'''
    prot_spacing = {}
    for protrusion in dendrite_rObject.children:
        spacing = 0
        for child in protrusion:
            # If child has subchildren, adjust spacing
            if child.name[-1].isalpha() and ord(child.name[-1]) - 97 > spacing:
                spacing = ord(child.name[-1])-97
        prot_spacing[protrusion.name] = spacing
    return prot_spacing

class excelWorkbook(openpyxl.Workbook):
    def __init__(self):
        openpyxl.Workbook.__init__(self)
        
        self.dendriteFilter = []
        self.traceTypeFilter = ['d[0-9][0-9]c[0-9][0-9]']
        self.dendriteDict = None
        
    def getDendriteDict(self, series):
        self.dendriteDict = series.getObjectHierarchy(*series.getObjectLists())


    def writeProtrusions(self, dendrite_rObj, sheet):
        '''Writes data and headers for protrusions with correct with spacing'''
        prot_spacing = getProtrusionSpacing(self.dendriteDict[dendrite_rObj.name])
        prot_by_start = sorted([prot for prot in self.dendriteDict[dendrite_rObj.name].children], key=lambda rObject: rObject.start)
        
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
    
    def writeWorkbook(self):
        '''Writes data from a loaded dendrite dictionary to a worksheet'''
        # for each dendrite in the dictionary, create a sheet and fill with data
        for dendrite in self.dendriteDict:
            # Create sheet
            sheet_name = self.dendriteDict[dendrite].series.name+' '+self.dendriteDict[dendrite].name
            self.create_sheet(title=sheet_name)
            sheet = self.get_sheet_by_name(sheet_name)
            
            # Protrusion spacing
            prot_spacing = getProtrusionSpacing(self.dendriteDict[dendrite])
            
            # Write protrusion data and column headers
            self.writeProtrusions( self.dendriteDict[dendrite], sheet )
            types = getTraceTypes( self.dendriteDict[dendrite] )
            
            sorted_prots = sorted([prot for prot in self.dendriteDict[dendrite]], key=lambda rObject: rObject.start)
            
            # Write traces
            column = 8
            # Each trace type
            types = [tType for tType in types if tType not in self.traceTypeFilter]
            for tType in types:
                # Column headers
                sheet.cell(row=0, column=column).value = 'Object Name'
                sheet.cell(row=0, column=column+1).value = 'Start'
                sheet.cell(row=0, column=column+2).value = 'End'
                sheet.cell(row=0, column=column+3).value = 'Count'
                sheet.cell(row=0, column=column+4).value = 'Surface Area'
                sheet.cell(row=0, column=column+5).value = 'Flat Area'
                sheet.cell(row=0, column=column+6).value = 'Volume'
                if 'cfa' in tType:
                    sheet.cell(row=0,column=column+7).value = 'Total Volume'
                    
                row = 1 # reset row for each trace type
                for protrusion in sorted_prots:
                    protrusionChildren = [child for child in protrusion if re.compile(tType).match(child.name)]
                    for child in sorted(protrusionChildren, key=lambda rObject: rObject.name):
                        sheet.cell(row=row,column=column).value = child.name
                        sheet.cell(row=row,column=column+1).value = child.start
                        sheet.cell(row=row,column=column+2).value = child.end
                        sheet.cell(row=row,column=column+3).value = child.count
                        sheet.cell(row=row,column=column+4).value = child.surfacearea
                        sheet.cell(row=row,column=column+5).value = child.flatarea
                        sheet.cell(row=row,column=column+6).value = child.volume
                        if 'cfa' in tType:
                            sheet.cell(row=row,column=column+7).value = child.totalvolume
                        row+=1
                    if len(protrusionChildren) != prot_spacing[protrusion.name]+1:
                        row+=prot_spacing[protrusion.name]+1-len(protrusionChildren)
                column+=8
                if 'cfa' in tType: # one more column shift for the totalvolume attribute
                    column+=1

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