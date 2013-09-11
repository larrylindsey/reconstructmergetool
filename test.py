from PySide import QtGui, QtCore
import reconstructmergetool as rmt
import sys
from Series import *
import time

'''TEST.PY functions as a test page for rmtgui.py. Changes are first made to test.py until a working
product is established and ready to be copied to rmtgui.py'''
# To Do:
#     list of sectionContourWidgets in mainFrame, put sec slider in mainFrame
#     QPushButton.setAcceptDrops(True) for load series

class mainFrame(QtGui.QFrame):
    '''The mainFrame() class holds all the contents of the reconstructmergetool (RMT) gui. It is the one
    RMTgui class that is open throughout the entire program.
    GUI-wise: the mainframe contains the widgets necessary for proper functioning of RMT. And a
        quit button.
    Data-wise: It contains all the important info regarding the series that are being merged.'''
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        # Window Dimensions and Attributes
        self.setGeometry(0,0,800,600)
        self.setWindowTitle('Reconstructmergetool v.BETA') #===
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        # Widgets
        self.nextButton = QtGui.QPushButton(self)
        self.backButton = QtGui.QPushButton(self)
        self.slider = QtGui.QSlider(self)
        self.label = QtGui.QLabel(self)
        
        # Main Data
#         self.ser1path = '/home/wtrdrnkr/Downloads/BBCHZ/BBCHZ.ser'
#         self.ser2path = '/home/wtrdrnkr/Downloads/SRQHN/SRQHN.ser'
        self.ser1path = '/home/michaelm/Documents/Test Series/rmtgTest/ser1/BBCHZ.ser' #===
        self.ser2path = '/home/michaelm/Documents/Test Series/rmtgTest/ser2/BBCHZ.ser' #===
#         self.ser1path = '/home/michaelm/Documents/Test Series/BBCHZ/BBCHZ.ser' #===
#         self.ser2path = '/home/michaelm/Documents/Test Series/BBCHZ2/BBCHZ.ser' #===
        self.serName = 'rmtg' #===
        self.ser1obj = rmt.getSeries(self.ser1path) #===
        self.ser2obj = rmt.getSeries(self.ser2path) #===

        # Reconstruct Object Data
        self.mergedAttributes = None
        self.mergedSerContours = None
        self.mergedSerZContours = None
        
        self.mergedSecAttributes = None
        self.mergedSecImages = None
        self.mergedSecContours = None
        self.contourWidgets = [] #===
        self.currentWidget = None
        
        self.mergedSeries = None #=== First created (seriesAttributeWidget.next()) w/ no Contours/ZContours
        self.outputPath = 'Enter directory for output'
        
        # Load Functional Frame
        self.initUI()
        
    def initUI(self):
        self.prepNandBbuttons()
        self.prepSlider()
        self.prepLayout()
        
        # shown when needed
        self.slider.hide()
        self.label.hide()

        self.show()
    
    def prepLayout(self):
        # Layout: Puts buttons in bottom-right corner
        hbox = QtGui.QHBoxLayout() # Horizontal
        hbox.addStretch(1) # Push down
        hbox.addWidget(self.backButton)
        hbox.addWidget(self.nextButton)
        vbox2 = QtGui.QVBoxLayout() #===
        vbox2.addWidget(self.slider) #===
        vbox2.addWidget(self.label) #===
        
        vbox = QtGui.QVBoxLayout() # Vertical
        vbox.addStretch(1) # Push right
        vbox.addLayout(vbox2) #===
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        
    def prepNandBbuttons(self):
        # Next button
        self.nextButton.setText('Next')

        # Back button
        self.backButton.setText('Back')
          
    def prepSlider(self): #===
        # doesnt properly respond to clicking on ticks
        # Slider
        if type(self.ser1obj) != None and type(self.ser2obj) != None:
            minTick = int(self.ser1obj.sections[0].name[-1]) # section # of first section in section list
            if minTick == 0:
                maxTick = len(self.ser1obj.sections)-1 # number of sections in section list
            else:
                maxTick = len(self.ser1obj.sections)
            self.slider.setRange(minTick, maxTick)
        
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.slider.setTickInterval(1)
         
        # Label
        self.label.setText('Section '+str(self.slider.value()))
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        
        self.slider.sliderReleased.connect( self.changeSection )
        self.slider.sliderMoved.connect( self.changeSectionLabel )
        
    def changeSection(self): #===
        '''Loads appropriate section when the slider is released on a new position'''
        print('Switched to section: '+str(self.slider.value()))
        self.currentWidget.hide()
        print('section '+str(self.currentWidget.section)+' hidden')
        for sec in self.contourWidgets:
            if sec.section == self.slider.value():      
                self.currentWidget = sec
                print('section '+str(self.currentWidget.section)+' showing')
                self.currentWidget.show()
                return
        sec = mainFrame.sectionContourWidget( self, self.slider.value() )
        self.contourWidgets.append(sec)
        self.currentWidget = sec
        self.currentWidget.show()
   
    def changeSectionLabel(self): #===
        '''Updates the section label while the slider is being moved'''
        print('Hovering: '+str(self.slider.sliderPosition())) # currently hovering
        print('Previously Hovered: '+str(self.slider.value())) # currently selected
        newPos = self.slider.sliderPosition()
        self.label.setText('Section '+str(newPos))
           
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
            self.table = None
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
            self.table.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.MultiSelection)
            # Load attributes into their slots: To keep them in order (since dictionaries are unordered)
            # ...they are pulled out of the dictionary by the key in the verticalHeaderColumn
            for row in range(len(conflicts)):
                att = self.table.verticalHeaderItem(row).text() # attribute to be extracted
                # Series 1
                tableItem = QtGui.QTableWidgetItem( ser1atts[att] )
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                self.table.setItem(row, 0, tableItem)
                # Series 2
                tableItem = QtGui.QTableWidgetItem( ser2atts[att] )
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                self.table.setItem(row, 1, tableItem)
            self.table.show() 
        
    class seriesContourWidget(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            self.table1 = None
            self.table2 = None
            self.s1c = None
            self.s2c = None
            self.mergedConts = None
            
            # update mainFrame stuff
            self.parent.setWindowTitle('Series Contours') #===
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            
            rmt.mergeSeriesContours(self.parent.ser1obj.contours, self.parent.ser2obj.contours, handler=self.serContHandler)
            
            self.prepLayout()
            self.show()
        
        def prepLayout(self):
            # Layout
            vbox = QtGui.QVBoxLayout() # Holds all the boxes below
            hbox1 = QtGui.QHBoxLayout() # For the 2 tables
            hbox1.addWidget(self.table1) # Series 1
            hbox1.addWidget(self.table3) # Merged series contours
            hbox1.addWidget(self.table2) # Series 2
            vbox.addLayout(hbox1)
            self.setLayout(vbox)
            
        def serContHandler(self, ser1conts, ser2conts, ser3conts):
            table1 = QtGui.QTableWidget(len(ser1conts), 1, parent=self)
            table2 = QtGui.QTableWidget(len(ser2conts), 1, parent=self)
            table3 = QtGui.QTableWidget(len(ser3conts), 1, parent = self)
            
            for table in [table1, table2, table3]:
                table.setColumnWidth(0, 240)
                table.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.MultiSelection)
            table1.setHorizontalHeaderLabels( [self.parent.ser1obj.name] )
            table2.setHorizontalHeaderLabels( [self.parent.ser2obj.name] )
            table3.setHorizontalHeaderLabels( ['Merged Series Contours'])
            
            for row in range( len(ser1conts) ):
                tableItem = QtGui.QTableWidgetItem( ser1conts[row].name )
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table1.setItem(row, 0, tableItem)
            for row in range( len(ser2conts) ):
                tableItem = QtGui.QTableWidgetItem( ser2conts[row].name )
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table2.setItem(row, 0, tableItem)
            for row in range( len(ser3conts) ):
                tableItem = QtGui.QTableWidgetItem( ser3conts[row].name )
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightGreen')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table3.setItem(row, 0, tableItem)
                
            self.table1 = table1
            self.table2 = table2
            self.table3 = table3
#             self.table1.show()
#             self.table2.show()
            self.s1c = ser1conts
            self.s2c = ser2conts
            self.mergedConts = ser3conts
            
        def returnItems(self): #=== multiple tables added
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
            table.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.MultiSelection)
            for row in range( max(len(ser1zconts),len(ser2zconts)) ):
                # Series 1
                if row < len(ser1zconts): # Prevent index out of range
                    tableItem = QtGui.QTableWidgetItem( ser1zconts[row].name )
                    tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                    table.setItem(row, 0, tableItem)
                # Series 2
                if row < len(ser2zconts):
                    tableItem = QtGui.QTableWidgetItem( ser2zconts[row].name )
                    tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
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
                    tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                    table.setItem(count, 0, tableItem)
                    tableItem = QtGui.QTableWidgetItem( str(self.imgConflicts[i][1]) )
                    tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                    table.setItem(count, 1, tableItem)
            table.setVerticalHeaderLabels(sectionNames)
            table.resizeRowsToContents()
            table.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.MultiSelection)
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
            
#             for sec in self.parent.ser1obj.sections: #===
            self.parent.contourWidgets.append( mainFrame.sectionContourWidget(self.parent, 0 )) #===
            self.parent.currentWidget = self.parent.contourWidgets[0]
            self.parent.currentWidget.show()
                
            self.close()
              
        def back(self):
            # Disconnect buttons and open previous window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionAttributeWidget( self.parent )
            self.close()
    
    class sectionContourWidget(QtGui.QWidget):
        def __init__(self, parent=None, section=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            self.table1 = None # Series 1 table
            self.table2 = None # Merge table
            self.table3 = None # Series 2 table
            self.section = section
            
            # Original contours returned from rmt.mergeSectionContours()
            #=== Do not change these as this is what will be accessed if 'defaults' button pressed 
            self.uniqueA = None
            self.compOvlp = None
            self.confOvlp = None
            self.uniqueB = None
            
            # Update mainFrame data
            self.parent.setWindowTitle('Section Contours') #===
            
            # Load widget for each section into self.parent.tempContours
            self.prepTables(*rmt.mergeSectionContours(self.parent.ser1obj.sections[self.section],
                                                     self.parent.ser2obj.sections[self.section],
                                                     handler=self.secContHandler))
            self.prepButtonFunctionality()
            self.prepLayout()
        
        def secContHandler(self, uniqueA, compOvlp, confOvlp, uniqueB):
            '''rmtgui version of section contour handler'''
            self.uniqueA = uniqueA
            self.compOvlp = compOvlp
            self.confOvlp = confOvlp
            self.uniqueB = uniqueB
            return uniqueA, compOvlp, confOvlp, uniqueB

        def prepButtonFunctionality(self):
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            self.table2.itemDoubleClicked.connect( self.resolveConflict ) #=== Double click item to resolve conflict
        
        def prepLayout(self):
            self.parent.slider.show()
            self.parent.label.show()
            
            # Layout
            vbox = QtGui.QVBoxLayout() # Holds all the boxes below
            hbox1 = QtGui.QHBoxLayout() # For the 3 tables
            hbox1.addWidget(self.table1) # Series 1
            hbox1.addWidget(self.table2) # Conflicts/merges
            hbox1.addWidget(self.table3) # Series 2
            vbox.addLayout(hbox1)
            self.setLayout(vbox)
            
        def prepTables(self, s1unique, ovlps, confs, s2unique): #===
            table1 = QtGui.QTableWidget(len(s1unique), 1, parent=self)
            table2 = QtGui.QTableWidget(len(confs)+len(ovlps), 1, parent=self)
            table3 = QtGui.QTableWidget(len(s2unique), 1, parent=self)
            
            # Load labels/items into tables
            table1.setHorizontalHeaderLabels(['Unique 1'])
            for row in range(len(s1unique)):
                tableItem = QtGui.QTableWidgetItem( s1unique[row].name )
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table1.setItem(row, 0, tableItem)
                
            table2.setHorizontalHeaderLabels(['Conflicts/Overlaps'])
            row = 0
            for elem in confs:
                tableItem = QtGui.QTableWidgetItem( elem[0].name )
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('pink')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table2.setItem(row, 0, tableItem)
                row+=1
            for elem in ovlps:
                tableItem = QtGui.QTableWidgetItem( elem[0].name)
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightGreen')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table2.setItem(row, 0, tableItem)
                row+=1
                    
            table3.setHorizontalHeaderLabels(['Unique 2'])
            for row in range(len(s2unique)):
                tableItem = QtGui.QTableWidgetItem( s2unique[row].name )
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table3.setItem(row, 0, tableItem)
            
            # Apply changes to tables
            for table in [table1,table2,table3]:
                table.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.MultiSelection)
                table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
                table.setColumnWidth(0,240)
            
            # Assign tables to self
            self.table1 = table1
            self.table2 = table2
            self.table3 = table3
            return self
            
        def resolveConflict(self, item): #===
            row = item.row()
            pink = '#ffc0cb'
            yellow = '#ffff66'
            if item.background().color().name() in [pink, yellow]: # If background color = pink (i.e. is a conflict)
                self.showDetails( *self.returnConfConts(row) )
            self.itemToYellow(item)
            
        def returnConfConts(self, row):
            '''Returns a Contour object that is represented in row of the table'''
            return self.confOvlp[row][0], self.confOvlp[row][1]
        
        def showDetails(self, confA, confB): #===
            '''Gives more detail of the contours in conflict'''
            res = QtGui.QWidget(self)
            res.setGeometry(0,0,800,500)
            res.setAutoFillBackground(True)

            # Conflict Label (Name of conflicting contours)
            labelBox = QtGui.QHBoxLayout()
            label = QtGui.QLabel(self) # Label
            label.setText('Conflict: '+str(confA.name))
            labelBox.addWidget(label)
            labelBox.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            labelBox.setSizeConstraint(QtGui.QLayout.SetFixedSize)
            
            # Sections box
            sectionBox = QtGui.QHBoxLayout()
            #--- Section A
            secAbox = QtGui.QVBoxLayout() # For sectionA detail & button
            tBoxA = QtGui.QLabel(self) # Text box
            tBoxA.setText(str(confA))
            tBoxA.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            confAbut = QtGui.QPushButton(self) # Contour A button
            confAbut.setText('Keep A') #=== change size
            secAbox.addWidget(tBoxA)
            secAbox.addWidget(confAbut)
            sectionBox.addLayout(secAbox)
            #--- Section B
            secBbox = QtGui.QVBoxLayout() # For sectionB detail & button
            tBoxB = QtGui.QLabel(self) # Text box
            tBoxB.setText(str(confB))
            tBoxB.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            confBbut = QtGui.QPushButton(self) # Contour B button
            confBbut.setText('Keep B') #=== change size
            secBbox.addWidget(tBoxB)
            secBbox.addWidget(confBbut)
            sectionBox.addLayout(secBbox)
            
            # 'Cancel' & 'Keep Both buttons'
            archButtonBox = QtGui.QVBoxLayout()
            bothBut = QtGui.QPushButton(self)
            bothBut.setText('Keep Both Contours')
            cancelBut = QtGui.QPushButton(self)
            cancelBut.setText('Cancel')
            archButtonBox.addWidget(bothBut)
            archButtonBox.addWidget(cancelBut)
            archButtonBox.insertSpacing(-1,100) #===
            
            # Add to outside most layoutBox
            vbox = QtGui.QVBoxLayout() # For entire detail window
            vbox.addLayout(labelBox)
            vbox.addLayout(sectionBox)
            vbox.addLayout(archButtonBox)
            
            res.setLayout(vbox)
            res.show()
            
        def itemToYellow(self, item):
            item.setBackground(QtGui.QBrush(QtGui.QColor('#ffff66')))

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
#     mainFrame.serLoadWidget(rmtFrame) #===
    mainFrame.sectionImageWidget(rmtFrame)
    sys.exit( app.exec_() )
main()