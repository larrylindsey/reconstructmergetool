from PySide import QtGui, QtCore
import reconstructmergetool as rmt
import sys
from Series import *
from threading import Thread, Lock

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
        self.ser1path = '/home/michaelm/Documents/Test Series/BBCHZ/BBCHZ.ser' #===
        self.ser2path = '/home/michaelm/Documents/Test Series/BBCHZ2/BBCHZ.ser' #===
        self.serName = 'Apple' #===
        self.ser1obj = None
        self.ser2obj = None
        
        # More Data
        self.mergedAttributes = None
        self.mergedSerContours = None
        self.mergedSerZContours = None
        
        # Load Functional Frame
        self.initUI()
        
    def initUI(self):
        # Window Dimensions and Attributes
        self.setGeometry(0,0,800,600)
        self.setWindowTitle('Reconstructmergetool v.1')
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
            self.table = None
            self.conflicts = None
            
            # Update mainFrame data
            self.parent.setWindowTitle('Series Attributes') #===
            self.parent.ser1obj = rmt.getSeriesXML(self.parent.ser1path)
            self.parent.ser2obj = rmt.getSeriesXML(self.parent.ser2path)
            self.parent.backButton.setFlat(False)
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            
            # merge series
            rmt.mergeSeriesAttributes(self.parent.ser1obj, self.parent.ser2obj, handler=self.serAttHandler)
            
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
            self.parent.ser1obj.getSectionsXML( self.parent.ser1path )
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
            
            # Update mainFrame data
            self.parent.setWindowTitle('Section Images') #===
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            
            self.checkMultipleImage()
            print('TESTING')
            self.show()
            
        def checkMultipleImage(self): #===
            '''Checks series objects for more than one image'''
            flag = False
            ser1conflictList = []
            for section in self.series1.sections:
                ser1conflict = []
                if len(section.imgs) > 1:
                    ser1conflict = [img for img in section.imgs]
                    flag = True
                ser1conflictList.append(ser1conflict)
            
            ser2conflictList = []
            for section in self.series2.sections:
                ser2conflict = []
                if len(section.imgs) > 1:
                    ser2conflict = [img for img in section.imgs]
                    flag = True
                ser2conflictList.append(ser2conflict)
            
            # find the max number of images in a sections: use to set up # of columns in table
            maxImg = 1
            for conf in ser1conflictList:
                if len(conf) > maxImg:
                    maxImg = len(conf)
            for conf in ser2conflictList:
                if len(conf) > maxImg:
                    maxImg = len(conf)
            
            if flag == True: # Does a section contain more than one image? if so, make table
                msg = QtGui.QMessageBox(self)
                msg.setText('One or more sections contain more than one image, please make any necessary changes')
                msg.show()
                
                #=== should not be len+len (too many)
                self.table = QtGui.QTableWidget( (len(ser1conflictList)+len(ser2conflictList)), maxImg, parent=self)
                self.table.setGeometry(0,0,800,500)
    
                # Add multiple image conflicts to table
                confNames = []
                count = -1 # cur loc in ser#confList
                count2 = -1 # row in table
                for conf in ser1conflictList:
                    count += 1
                    if len(conf) > 1:
                        confNames.append( self.series1.sections[count].name )
                        count2 += 1
                        count3 = -1
                        for img in conf:
                            count3 += 1
                            tableItem = QtGui.QTableWidgetItem(str(img)) #===
                            self.table.setItem(count2, count3, tableItem)
                count = -1 # cur loc in ser#confList
                count2 = -1 # row in table
                for conf in ser2conflictList:
                    count += 1
                    if len(conf) > 1:
                        confNames.append( self.series2.sections[count].name )
                        count2 += 1
                        count3 = -1
                        for img in conf:
                            count3 += 1
                            tableItem = QtGui.QTableWidgetItem(str(img)) #===
                            self.table.setItem(count2, count3, tableItem)
                
                self.table.setVerticalHeaderLabels(confNames)
                self.table.resizeRowsToContents()
                self.table.resizeColumnsToContents()
                self.table.show()
            
        def secImgHandler(self): #===
            return
         
        def next(self):
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionContourWidget( self.parent )
            self.close()
            
        def back(self):
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionAttributeWidget( self.parent )
            self.close()
    
    class sectionContourWidget(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self,parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            
            # Update mainFrame data
            self.parent.setWindowTitle('Section Contours') #===
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            
            self.show()
            
        def next(self):
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionContourWidget( self.parent )
            self.close()
            
        def back(self):
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
            self.parent.backButton.clicked.connect( self.back )
            
        def next(self):
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            self.close()
            
        def back(self):
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