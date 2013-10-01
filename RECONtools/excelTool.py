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
                sheet.cell(row=row, column=column+4).value = 'Surface Area'
                sheet.cell(row=row, column=column+5).value = 'Flat Area'
                sheet.cell(row=row, column=column+6).value = 'Volume'
                
                row+=1
                for prot in sorted_prots:
                    sheet.cell(row=row, column=column).value = prot.name
                    sheet.cell(row=row, column=column+1).value = prot.start
                    sheet.cell(row=row, column=column+2).value = prot.end
                    sheet.cell(row=row, column=column+3).value = prot.count
                    sheet.cell(row=row, column=column+4).value = prot.surfacearea
                    sheet.cell(row=row, column=column+5).value = prot.flatarea
                    sheet.cell(row=row, column=column+6).value = prot.volume
                    
                    if prot_spacing[prot.name] > 0:
                        row+=prot_spacing[prot.name]
                    row+=1
                #=== Insert thick line down column? subchildren appear 8 columns right than supposed to
                #=== protrusion children not consistent down the columns
                
#                 # PROTRUSION CHILDREN
#                 column = 8
#                 list_of_types = []
#                 for row in range(len(sheet.rows)):
#                     check = sheet.cell(row=row,column=0).value # check protrusion column cell value
#                     if check != None and re.compile('d[0-9]{2}p[0-9]{2}').match(str(check)): # if no subchildren
#                         pNo = check
#                         #print('=============='+str(pNo)+'=============')
#                         # for each protrusion child
#                         for child in self.dendriteDict[dendrite][str(pNo)].children:
#                             
#                             # Get a reg exp for this protrusion child
#                             childExp = ''
#                             for character in child.name:
#                                 if character.isdigit():
#                                     character = '[0-9]'
#                                 childExp+=character
#                             list_of_types.append(childExp)
#                             
#                             # write trace data for this trace on all protrusions
#                             row += 1
#                             check2 = sheet.cell(row=row,column=0).value
#                             if check2 != None and re.compile('d[0-9]{2}p[0-9]{2}').match(str(check2)):
#                                 for child2 in self.dendriteDict[dendrite][str(check2)]:
#                                     if re.compile(childExp).match(child2.name) != None:
#                                         pass
#                                         #print(child2.name)
#                 
#                 list_of_types = list(set(list_of_types)) #=== still need to distinguish multiple subchildren
#                 print(list_of_types)
                            
                            
                
                            #sheet.cell(row=0,column=column).value = 'Name'
                            #sheet.cell(row=0,column=column+1).value = 'Start'
                            #sheet.cell(row=0,column=column+2).value = 'End'
                            #sheet.cell(row=0,column=column+3).value = 'Count'
                            #sheet.cell(row=0,column=column+4).value = 'Surface Area'
                            #sheet.cell(row=0,column=column+5).value = 'Flat Area'
                            #sheet.cell(row=0,column=column+6).value = 'Volume'
                            #sheet.cell(row=row,column=column).value = child.name
                            #sheet.cell(row=row,column=column+1).value = child.start
                            #sheet.cell(row=row,column=column+2).value = child.end
                            #sheet.cell(row=row,column=column+3).value = child.count
                            #sheet.cell(row=row,column=column+4).value = child.surfacearea
                            #sheet.cell(row=row,column=column+5).value = child.flatarea
                            #sheet.cell(row=row,column=column+6).value = child.volume
                        #column+=8
                    #else: # contains subchildren
                        #pass
                        
                
                
                
                
                
                
                # PROTRUSION CHILDREN
#                 column = 8 # start at 8th column
#                 row = 1
#                 child_columns = ['sp', 'sph', 'cfa']
#                 for row in range(len(sheet.rows)):
#                     if re.compile('d[0-9]{2}p[0-9]{2}').match(str(sheet.cell(row=row, column=0)).value):
#                         protrusionNum = sheet.cell(row=row,column=0).value[-2:]
#                         print(protrusionNum)
#                     
#                 
                
#                 # PROTRUSION CHILDREN ====
#                 for row in range(len(sheet.rows)+1):
#                     column=8
#                     cell = sheet.cell(row=row, column=0)
#                     if cell.value != None and re.compile('d[0-9]{2}p[0-9]{2}').match(cell.value) != None:
#                         for child in self.dendriteDict[dendrite][str(cell.value)].children:
#                             sheet.cell(row=0,column=column).value = 'Name'
#                             sheet.cell(row=0,column=column+1).value = 'Start'
#                             sheet.cell(row=0,column=column+2).value = 'End'
#                             sheet.cell(row=0,column=column+3).value = 'Count'
#                             sheet.cell(row=0,column=column+4).value = 'Surface Area'
#                             sheet.cell(row=0,column=column+5).value = 'Flat Area'
#                             sheet.cell(row=0,column=column+6).value = 'Volume'
#                             if prot_spacing[prot.name] < 1:
#                                 sheet.cell(row=row,column=column).value = child.name
#                                 sheet.cell(row=row,column=column+1).value = child.start
#                                 sheet.cell(row=row,column=column+2).value = child.end
#                                 sheet.cell(row=row,column=column+3).value = child.count
#                                 sheet.cell(row=row,column=column+4).value = child.surfacearea
#                                 sheet.cell(row=row,column=column+5).value = child.flatarea
#                                 sheet.cell(row=row,column=column+6).value = child.volume
#                                 column+=8
#                             else:
#                                 sRow = row + ord(prot.name[-1])-97 #increment row by subchild order number
#                                 sheet.cell(row=sRow,column=column).value = child.name
#                                 sheet.cell(row=sRow,column=column+1).value = child.start
#                                 sheet.cell(row=sRow,column=column+2).value = child.end
#                                 sheet.cell(row=sRow,column=column+3).value = child.count
#                                 sheet.cell(row=sRow,column=column+4).value = child.surfacearea
#                                 sheet.cell(row=sRow,column=column+5).value = child.flatarea
#                                 sheet.cell(row=sRow,column=column+6).value = child.volume
# #                                 column+=8 # spacing for next child               

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