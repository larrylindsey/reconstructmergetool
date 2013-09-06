from PySide import QtGui, QtCore
import reconstructmergetool as rmt
import sys
from Series import *

'''TEST.PY functions as a test page for rmtgui.py. Changes are first made to test.py until a working
product is established and ready to be copied to rmtgui.py'''
# To Do:
#     when to load series into objects?
#     Reworking GUI to use functions already in reconstructmergetool
#     Serconts, serzconts, secatts, secimgs, secconts, etc.
#     QPushButton.setAcceptDrops(True) for load series
#     Allow multiple images option

class mainFrame(QtGui.QFrame):
    '''The mainFrame() class holds all the contents of the reconstructmergetool (RMT) gui. It is the one
    RMTgui class that is open throughout the entire program.
    GUI-wise: the mainframe contains the widgets necessary for proper functioning of RMT. And a
        quit button.
    Data-wise: It contains all the important info regarding the series that are being merged.'''
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        
        # Main Data (accessed regularly by subsequent functions)
        self.ser1path = '/home/michaelm/Documents/Test Series/rmtgTest/ser1/rmtg.ser' #===
        self.ser2path = '/home/michaelm/Documents/Test Series/rmtgTest/ser2/rmtg.ser' #===
        self.serName = 'rmtg' #===
        self.ser1obj = None
        self.ser2obj = None
        
        # More Data
        self.mergedAttributes = None
        self.mergedSerContours = None
        self.mergedSerZContours = None
        self.mergedSecAttributes = None
        self.mergedSecImages = None
        self.mergedSecContours = None
        self.mergedSeries = None #=== First created (seriesAttributeWidget.next()) w/ no Contours/ZContours
        self.outputPath = 'Enter directory for output'
        
        # Load Functional Frame
        self.initUI()
        
    def initUI(self):
        # Window Dimensions and Attributes
        self.setGeometry(0,0,800,600)
        self.setWindowTitle('Reconstructmergetool v.BETA')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        # Next button
        self.nextButton = QtGui.QPushButton(self)
        self.nextButton.setText('Next')

        # Back button
        self.backButton = QtGui.QPushButton(self)
        self.backButton.setText('Back')

        # Layout: Puts buttons in bottom-right corner
        hbox = QtGui.QHBoxLayout() # Horizontal
        hbox.addStretch(1) # Push down
        hbox.addWidget(self.backButton)
        hbox.addWidget(self.nextButton)
        
        vbox = QtGui.QVBoxLayout() # Vertical
        vbox.addStretch(1) # Push right
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        
        # Show mainFrame()
        self.show()
    
    class serLoadWidget(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            self.parent.backButton.setFlat(True)
            self.parent.nextButton.clicked.connect( self.checkNextButton )
             
            # Series path text bars
            self.s1bar = QtGui.QLineEdit(self)
            self.s1bar.setText(parent.ser1path)
            self.s1browse = QtGui.QPushButton(self)
            self.s1browse.setIconSize(QtCore.QSize(25,25))
            self.s1browse.setText('Browse')
            self.s1browse.clicked.connect( self.browseSer )
            
            self.s2bar = QtGui.QLineEdit(self)
            self.s2bar.setText(parent.ser2path)
            self.s2browse = QtGui.QPushButton(self)
            self.s2browse.setIconSize(QtCore.QSize(25,25))
            self.s2browse.setText('Browse')
            self.s2browse.clicked.connect( self.browseSer )
            
            # Series name text bar
            self.sNameBar = QtGui.QLineEdit(self)
            self.sNameBar.setText(parent.serName)
            
            # Layout
            hbox1 = QtGui.QHBoxLayout()
            hbox1.addWidget(self.s1bar)
            hbox1.addWidget(self.s1browse)
            hbox1.insertSpacing(0,150)
            hbox1.insertSpacing(-1,150)
            
            hbox2 = QtGui.QHBoxLayout()
            hbox2.addWidget(self.s2bar)
            hbox2.addWidget(self.s2browse)
            hbox2.insertSpacing(0,150)
            hbox2.insertSpacing(-1,150)
            
            hbox3 = QtGui.QHBoxLayout()
            hbox3.addWidget(self.sNameBar)
            hbox3.insertSpacing(0,300)
            hbox3.insertSpacing(-1,300)
            
            vbox = QtGui.QVBoxLayout()
            vbox.insertSpacing(0,200)

            vbox.addLayout(hbox1)
            vbox.addLayout(hbox2)
            vbox.addLayout(hbox3)
            
            self.setLayout(vbox)
            self.show()
        
        def browseSer(self):
            '''Displays file browser and updates text in s1bar or s2bar.
            Parent data is not updated until next button function is executed
            successfully.'''
            path = QtGui.QFileDialog.getOpenFileName(self,
                                                     'Load Series',
                                                     '/home/',
                                                     'Series File (*.ser)')
            path = str(path[0]) # extract path and turn unicode -> regstr
            if self.sender() == self.s1browse: 
                self.s1bar.setText(path)
            elif self.sender() == self.s2browse:
                self.s2bar.setText(path)
        
        def checkNextButton(self):
            if '.ser' not in self.s1bar.text() or '.ser' not in self.s2bar.text():
                msg = QtGui.QMessageBox(self)
                msg.setText('Please enter valid paths for both series')
                msg.show()
            elif self.sNameBar.text() == 'Enter name of new series' or self.sNameBar.text() == '':
                msg = QtGui.QMessageBox(self)
                msg.setText('Please enter a valid series name')
                msg.show()
            else:
                # Update mainFrame() data
                self.parent.ser1path = self.s1bar.text()
                self.parent.ser2path = self.s2bar.text()
                self.parent.serName = self.sNameBar.text().replace('.ser','')
                
                # Merge series widget
                self.parent.seriesAttributeWidget(self.parent)
                self.parent.nextButton.clicked.disconnect( self.checkNextButton )
                self.close()

    class seriesAttributeWidget(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            self.table1 = None
            self.table2 = None
            self.conflicts = None
            
            # Update mainFrame data
            self.parent.setWindowTitle('Series Attributes') #===
            self.parent.ser1obj = rmt.getSeriesXML(self.parent.ser1path)
            self.parent.ser2obj = rmt.getSeriesXML(self.parent.ser2path)
            self.parent.backButton.setFlat(False)
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            
            # Merge series
            rmt.mergeSeriesAttributes(self.parent.ser1obj, self.parent.ser2obj, handler=self.serAttHandler)
            
            # Layout
#             vbox = QtGui.QVBoxLayout()
#             hbox = QtGui.QHBoxLayout()
#             hbox.addWidget(self.table1)
#             hbox.addWidget(self.table2)
#             vbox.addLayout(hbox)
            
            self.show()
            
        def next(self):
            if len(self.table.selectedItems()) != len(self.conflicts):
                msg = QtGui.QMessageBox(self)
                msg.setText('Please select one item per row')
                msg.show()
            else:
                # Create new dictionary of merged attributes
                newAtts = self.parent.ser1obj.output()[0]
                resolvedAtts = [ str(item.text()) for item in self.table.selectedItems() ]
                for row in range(len(self.conflicts)):
                    att = self.table.verticalHeaderItem(row).text()
                    newAtts[att] = resolvedAtts.pop(0)
                self.parent.mergedAttributes = newAtts
                self.parent.mergedSeries = Series(root=ET.Element('Series',newAtts),name=self.parent.serName)
                
                # Disconnect buttons and load next window
                self.parent.nextButton.clicked.disconnect( self.next )
                self.parent.backButton.clicked.disconnect( self.back )
                self.parent.seriesContourWidget(self.parent)
                self.close()
        
        def back(self):
            # Disconnect buttons and load prev window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.serLoadWidget( self.parent )
            self.close()
        
        def serAttHandler(self, ser1atts, ser2atts, ser3atts, conflicts):
            attLabels = [str(conflict) for conflict in conflicts]
            self.conflicts = conflicts
            # Present conflicts in a 2 column table, can select individual attributes or all for a series
            self.table = QtGui.QTableWidget(len(conflicts), 2, parent=self)
            self.table.setGeometry(0,0,800,500)
            self.table.setColumnWidth(0, 300)
            self.table.setColumnWidth(1, 300)
            self.table.setHorizontalHeaderLabels( [self.parent.ser1obj.name, self.parent.ser2obj.name] )
            self.table.setVerticalHeaderLabels( attLabels )

            # Load attributes into their slots: To keep them in order (since dictionaries are unordered)
            # ...they are pulled out of the dictionary by the key in the verticalHeaderColumn
            for row in range(len(conflicts)):
                att = self.table.verticalHeaderItem(row).text() # attribute to be extracted
                # Series 1
                tableItem = QtGui.QTableWidgetItem( ser1atts[att] )
                self.table.setItem(row, 0, tableItem)
                # Series 2
                tableItem = QtGui.QTableWidgetItem( ser2atts[att] )
                self.table.setItem(row, 1, tableItem)
            self.table.show() 
        
    class seriesContourWidget(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            self.table = None
            self.s1c = None
            self.s2c = None
            self.mergedConts = None
            
            # update mainFrame stuff
            self.parent.setWindowTitle('Series Contours') #===
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            
            rmt.mergeSeriesContours(self.parent.ser1obj.contours, self.parent.ser2obj.contours, handler=self.serContHandler)
            self.show()
            
        def serContHandler(self, ser1conts, ser2conts, ser3conts):
            self.table = QtGui.QTableWidget(len(ser1conts), 2, parent=self)
            self.table.setGeometry(0,0,800,500)
            self.table.setColumnWidth(0, 300)
            self.table.setColumnWidth(1, 300)
            self.table.setHorizontalHeaderLabels( [self.parent.ser1obj.name, self.parent.ser2obj.name] )

            for row in range( len(ser1conts) ):
                # Series 1
                tableItem = QtGui.QTableWidgetItem( ser1conts[row].name )
                self.table.setItem(row, 0, tableItem)
                # Series 2
                tableItem = QtGui.QTableWidgetItem( ser2conts[row].name )
                self.table.setItem(row, 1, tableItem)
            
            self.table.show()
            self.s1c = ser1conts
            self.s2c = ser2conts
            self.mergedConts = ser3conts
            
        def returnItems(self):
            selItems = self.table.selectedItems()
            selConts = []
            for item in selItems:
                if item.column() == 0:
                    selConts.append( self.s1c[item.row()] )
                if item.column() == 1:
                    selConts.append( self.s2c[item.row()] )
            return selConts

        def next(self):
            if ( len(self.mergedConts) + len(self.table.selectedItems()) ) != 20:
                msg = QtGui.QMessageBox(self)
                msg.setText('Please select one item per row')
                msg.show()
            else:
                # Add the selectedItems() to self.mergedAtts
                self.parent.mergedSerContours = self.mergedConts.extend( self.returnItems() )
                
                # Disconnect buttons and load next window
                self.parent.nextButton.clicked.disconnect( self.next )
                self.parent.backButton.clicked.disconnect( self.back )
                mainFrame.seriesZContourWidget( self.parent )
                self.close()
            
        def back(self):
            # Disconnect buttons and load prev window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.seriesAttributeWidget(self.parent)
            self.close()
    
    class seriesZContourWidget(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            self.table = None
            self.s1zc = None
            self.s2zc = None
            self.mergedZConts = None

            # Update mainFrame data
            self.parent.setWindowTitle('Series ZContours') #===
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            
            rmt.mergeSeriesZContours(self.parent.ser1obj.contours,
                                                    self.parent.ser2obj.contours,
                                                    handler=self.serZContHandler)
            
            self.show()
            
        def serZContHandler(self, ser1zconts, ser2zconts, ser3zconts):
            self.s1zc = ser1zconts
            self.s2zc = ser2zconts
            self.mergedZConts = ser3zconts
            
            self.prepTables(ser1zconts, ser2zconts, ser3zconts)  

        def prepTables(self, ser1zconts, ser2zconts, ser3zconts):
            table = QtGui.QTableWidget( max(len(ser1zconts),len(ser2zconts)), 2, parent=self )
            table.setGeometry(0,0,800,500)
            table.setColumnWidth(0, 300)
            table.setColumnWidth(1, 300)
            for row in range( max(len(ser1zconts),len(ser2zconts)) ):
                # Series 1
                if row < len(ser1zconts): # Prevent index out of range
                    tableItem = QtGui.QTableWidgetItem( ser1zconts[row].name )
                    table.setItem(row, 0, tableItem)
                # Series 2
                if row < len(ser2zconts):
                    tableItem = QtGui.QTableWidgetItem( ser2zconts[row].name )
                    table.setItem(row, 1, tableItem)
            self.table = table
            self.table.show()
        
        def returnItems(self):
            selItems = self.table.selectedItems()
            selzConts = []
            for item in selItems:
                if item.column() == 0:
                    selzConts.append( self.s1zc[item.row()] )
                if item.column() == 1:
                    selzConts.append( self.s2zc[item.row()] )
            return selzConts   
        
        def next(self):
            self.mergedZConts.extend( self.returnItems() )
            self.parent.mergedSerZContours = self.mergedZConts
            
            # Disconnect buttons and load next window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionAttributeWidget( self.parent )
            self.close()
            
        def back(self):
            # Disconnect buttons and load prev window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.seriesContourWidget( self.parent )
            self.close()
    
    class sectionAttributeWidget(QtGui.QWidget): #=== should be basically the same as seriesAttributeWidget()
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            
            # Update mainFrame data
            self.parent.setWindowTitle('Section Attributes') #===
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            self.parent.ser1obj.getSectionsXML( self.parent.ser1path ) #=== taking too long, need some sort of msg?
            self.parent.ser2obj.getSectionsXML( self.parent.ser2path )
            self.show()
            
        def next(self):
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionImageWidget( self.parent )
            self.close()
            
        def back(self):
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.seriesZContourWidget( self.parent )
            self.close()
                   
    class sectionImageWidget(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            self.series1 = self.parent.ser1obj
            self.series2 = self.parent.ser2obj
            self.table = None
            self.imgConflicts = [] # list of lists of images for sections. len(inner-list) >1 if there's a conflict
            
            # Update mainFrame data
            self.parent.setWindowTitle('Section Images') #===
            self.parent.nextButton.clicked.connect( self.next ) #===
            self.parent.backButton.clicked.connect( self.back )
            
            # Find conflicting images
            for i in range(len(self.series1.sections)):
                self.imgConflicts.append( rmt.mergeSectionImgs(self.series1.sections[i],
                                     self.series2.sections[i],
                                     handler=self.secImgHandler) )
            self.prepTable()
            self.show()
          
        def secImgHandler(self, s1, s2):
            return [s1.imgs[0], s2.imgs[0]]
        
        def prepTable(self):
            table = QtGui.QTableWidget( len([conf for conf in self.imgConflicts if len(conf)>1]), 2, parent=self )
            table.setGeometry(0,0,800,500)
            table.setColumnWidth(0, 300)
            table.setColumnWidth(1, 300)
            
            sectionNames = []
            count = -1
            for i in range(len(self.imgConflicts)):
                if len(self.imgConflicts[i]) > 1:
                    count += 1
                    sectionNames.append( str(self.parent.serName)+'.'+str(i))
                    tableItem = QtGui.QTableWidgetItem( str(self.imgConflicts[i][0]) )
                    table.setItem(count, 0, tableItem)
                    tableItem = QtGui.QTableWidgetItem( str(self.imgConflicts[i][1]) )
                    table.setItem(count, 1, tableItem)
            table.setVerticalHeaderLabels(sectionNames)
            table.resizeRowsToContents()
            self.table = table
            self.table.show()
        
        def returnItems(self):
            selItems = self.table.selectedItems()
            for item in selItems:
                sectionNum = int(self.table.verticalHeaderItem(item.row()).text().rsplit('.')[1])
                if item.column() == 0:
                    self.imgConflicts[sectionNum] = self.series1.sections[sectionNum].imgs
                elif item.column() == 1:
                    self.imgConflicts[sectionNum] = self.series2.sections[sectionNum].imgs
            
        def next(self):
            self.returnItems()
            self.parent.mergedSecImages = self.imgConflicts
            
            # Check for no multiple images
            for item in self.parent.mergedSecImages:
                if len(item) != 1:
                    msg = QtGui.QMessageBox(self)
                    msg.setText('Please select one image per row')
                    msg.show()
                    return
            # Disconnect buttons and open next window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionContourWidget( self.parent )
            self.close()
              
        def back(self):
            # Disconnect buttons and open previous window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionAttributeWidget( self.parent )
            self.close()
    
    class sectionContourWidget(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self,parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            self.table1 = None # Series 1 table
            self.table2 = None # Merge table
            self.table3 = None # Series 2 table
            self.table4 = None # Section selection table
            
            # Update mainFrame data
            self.parent.setWindowTitle('Section Contours') #===
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            
            # Contour handling functions
            self.prepContours()
            #===
            s1unique = ['a','b','c']
            confs = ['d','e']
            ovlps = ['f','g']
            s2unique = ['h','i','j']
            self.prepTables(s1unique, confs, ovlps, s2unique)
            
            # Layout
            vbox = QtGui.QVBoxLayout() # Holds all the boxes below
            hbox1 = QtGui.QHBoxLayout() # For the 3 tables
            hbox2 = QtGui.QHBoxLayout() # For the section selection table
            hbox1.addWidget(self.table1) # Series 1
            hbox1.addWidget(self.table2) # Conflicts/merges
            hbox1.addWidget(self.table3) # Series 2
            hbox2.addWidget(self.table4) # section selection
            vbox.addLayout(hbox1)
            vbox.addLayout(hbox2)
            self.setLayout(vbox)
            
            
            
            self.show()
            
        def prepContours(self):
            return
            allConflicts = []
            for section in range(len(self.parent.ser1obj.sections)):
                self.mergeSectionContours(self.parent.ser1obj.sections[section],
                                          self.parent.ser2obj.sections[section],
                                          handler=self.secContHandler)
#=================DOESNT WORK AS DESIGNED in rmt.py=====================               
#                 rmt.mergeSectionContours(self.parent.ser1obj,
#                                          self.parent.ser2obj,
#                                          handler=self.secContHandler)
#=======================================================================

        def mergeSectionContours(self, section1, section2, handler=None):
            # Lists of all contours in parallel sections
            conts1 = [cont for cont in section1.contours]
            conts2 = [cont for cont in section2.contours]
            # Populate shapely shapes
            for contour in conts1: contour.popshape()
            for contour in conts2: contour.popshape()
            conts3 = []
            while len(conts1) != 0 and len(conts2) != 0: # Go until lists are empty
                for elem in handler( *rmt.checkOverlappingConts(conts1,conts2) ):
                    conts3.append( elem )

        def prepTables(self, s1unique, confs, ovlps, s2unique):
            table1 = QtGui.QTableWidget(len(s1unique), 1, parent=self)
            table2 = QtGui.QTableWidget(len(confs)+len(ovlps), 1, parent=self)
            table3 = QtGui.QTableWidget(len(s1unique), 1, parent=self)
            table4 = QtGui.QTableWidget(1, len(self.parent.ser1obj.sections), parent=self)
            
            # Load labels/items into tables
            table1.setHorizontalHeaderLabels(['Unique 1'])
            for row in range(len(s1unique)):
                tableItem = QtGui.QTableWidgetItem( s1unique[row] )
                table1.setItem(row, 0, tableItem)
            table2.setHorizontalHeaderLabels(['Conflicts/Overlaps'])
            for row in range(len(confs)+len(ovlps)):
                if row < len(confs):
                    tableItem = QtGui.QTableWidgetItem( confs[row] )
                    table2.setItem(row, 0, tableItem)
                elif row >= len(confs):
                    tableItem = QtGui.QTableWidgetItem( ovlps[row-len(confs)] )
                    table2.setItem(row, 0, tableItem)
            table3.setHorizontalHeaderLabels(['Unique 2'])
            for row in range(len(s2unique)):
                tableItem = QtGui.QTableWidgetItem( s1unique[row] )
                table3.setItem(row, 0, tableItem)
            
            # Resize tables
            table1.resizeColumnsToContents()
            table1.resizeRowsToContents()
            table2.resizeColumnsToContents()
            table2.resizeRowsToContents()
            table3.resizeColumnsToContents()
            table3.resizeRowsToContents()
            table4.resizeColumnsToContents()
            table4.resizeRowsToContents()
            
            print(table1.horizontalHeaderItem(0).sizeHint())
            # Assign tables and show
            self.table1 = table1
            self.table2 = table2
            self.table3 = table3
            self.table4 = table4
            self.table1.show()
            self.table2.show()
            self.table3.show()
            self.table4.show()
            
        def secContHandler(self, ovlp1, ovlp2):
            completeOverlap = []
            if len(ovlp2) == 0:
                completeOverlap.append(ovlp1.pop())
        
            # Check for same contours and remove (prevents unnecessary user input)
            for elem in ovlp1:
                for elem2 in ovlp2:
                    if elem.overlaps(elem2) == 1: # If contours are the same -> merge and output
                        completeOverlap.append( elem )
                        ovlp1.remove( elem )
                        ovlp2.remove( elem2 )
                        
            # Check rest of contours
            conflictList = []
            for elem in ovlp1:
                for elem2 in ovlp2:
                    if elem.overlaps(elem2) != 1 and elem.overlaps(elem2) != 0: # If contours overlap, but not 100% -> user input
                        conflictList.append( [elem, elem2] )
            print('compovlp: '+str([cont.name for cont in completeOverlap]))
            print('conflist: '+str([cont.name for cont in conflictList]))
            return completeOverlap, conflictList
        
        def next(self):
            
            # Disconnect buttons and load next window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.outputWidget( self.parent )
            self.close()
            
        def back(self):
            # Disconnect buttons and load previous window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionImageWidget( self.parent )
            self.close()
            
    class outputWidget(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            
            # Update mainFrame data
            self.parent.setWindowTitle('Output Merged Series') #===
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.nextButton.setText('Finish and close') #===
            self.parent.backButton.clicked.connect( self.back )
            
            # Output path edit bar
            self.outBar = QtGui.QLineEdit(self)
            self.outBar.setText(self.parent.outputPath)
            
            # Series name bar
            self.nameBar = QtGui.QLineEdit(self)
            self.nameBar.setText( self.parent.serName )
            
            # Output path browse button
            self.outBarBrowse = QtGui.QPushButton(self)
            self.outBarBrowse.setIconSize(QtCore.QSize(25,25))
            self.outBarBrowse.setText('Browse')
            self.outBarBrowse.clicked.connect( self.browseOutPath )

            #=== Checkbox for transferring picture files?
            
            
            # Layout
            hbox = QtGui.QHBoxLayout()
            hbox.addWidget(self.outBar)
            hbox.addWidget(self.outBarBrowse)
            hbox.insertSpacing(0,150)
            hbox.insertSpacing(-1,150)
            
            hbox2 = QtGui.QHBoxLayout()
            hbox2.addWidget(self.nameBar)
            hbox2.insertSpacing(0,300)
            hbox2.insertSpacing(-1,300)
            
            vbox = QtGui.QVBoxLayout()
            vbox.insertSpacing(0,200)

            vbox.addLayout(hbox)
            vbox.addLayout(hbox2)

            self.setLayout(vbox)
            self.show()
            
        def browseOutPath(self):
            path = QtGui.QFileDialog.getExistingDirectory(self,
                                                     'Select Output Directory',
                                                     '/home/')
            path = str(path)+'/' # extract path and turn unicode -> regstr
            self.parent.outputPath = path
            self.outBar.setText(path)
                
        def next(self):
            # Output merged series, close program (restart program?)
            if '/' in self.parent.outputPath:
                if str( self.nameBar.text() ) != str( self.parent.serName ):
                    self.parent.serName = str( self.nameBar.text() )
                    self.parent.mergedSeries.name = str( self.nameBar.text() )
                    count=-1
                    for section in self.parent.mergedSeries.sections:
                        count+=1
                        section.name = str( self.nameBar.text() )+'.'+str( count )
                        print(section.name) #===
                self.parent.mergedSeries.writeseries( self.parent.outputPath )
                self.parent.mergedSeries.writesections( self.parent.outputPath )
                self.close()
            else:
                msg = QtGui.QMessageBox(self)
                msg.setText('Invalid directory, please fix')
                msg.show()
            
        def back(self):
            # Disconnect buttons and load previous window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionContourWidget( self.parent )
            self.close()
            
def main():
    app = QtGui.QApplication(sys.argv)
    rmtFrame = mainFrame()
    mainFrame.serLoadWidget(rmtFrame)   
    sys.exit( app.exec_() )
main()