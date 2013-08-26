from PySide import QtGui, QtCore
import reconstructmergetool as rmt
import sys
from Series import *
from threading import Thread, Lock

'''TEST.PY functions as a test page for rmtgui.py. Changes are first made to test.py until a working
product is established and ready to be copied to rmtgui.py'''
# To Do:
#     return seratts as dict
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
        self.ser1path = 'Drag and drop, or enter path to, series 1 file'
        self.ser2path = 'Drag and drop, or enter path to, series 2 file'
        self.serName = 'Enter name of new series'
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
            msg = QtGui.QMessageBox(self)
            if '.ser' not in self.s1bar.text() or '.ser' not in self.s2bar.text():
                msg.setText('Please enter valid paths for both series')
                msg.show()
            elif self.sNameBar.text() == 'Enter name of new series' or self.sNameBar.text() == '':
                msg.setText('Please enter a valid series name')
                msg.show()
            else:
                msg.setText('Creating new series: %s'%(self.sNameBar.text()))
                msg.show()
                # Update mainFrame() data
                self.parent.ser1path = self.s1bar.text()
                self.parent.ser2path = self.s2bar.text()
                self.parent.serName = self.sNameBar.text().replace('.ser','')
                
                # Merge series widget
                self.parent.mergeSeries(self.parent)
                self.close()
            
                
    class mergeSeries(QtGui.QWidget): #=== table is returning items before even shown/selected: QWaitCondition
        def __init__(self, parent=None): # .... mutex.wait(ULONG_MAX)
            QtGui.QWidget.__init__(self, parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            self.parent.backButton.setFlat(False)
            self.parent.backButton.clicked.connect( self.back )
            
            # Data
            self.table = None
            self.parent.ser1obj = rmt.getSeriesXML(self.parent.ser1path) # .ser only, no sections
            self.parent.ser2obj = rmt.getSeriesXML(self.parent.ser2path) # "
            
            self.newSer = rmt.mergeSeries(self.parent.ser1obj,
                                          self.parent.ser2obj,
                                          name = self.parent.serName,
                                          mergeSerAttfxn = self.serAttHandler,
                                          mergeSerContfxn = self.serContHandler,
                                          mergeSerZContfxn = self.serZContHandler)
            self.mainThread.start() #===
            self.show()
            
        def back(self):
            self.parent.serLoadWidget(self.parent)
            self.close()
        def next(self):
            msg = QtGui.QMessageBox(self) #===
            msg.setText('Next Pressed') #===
            
        def serAttHandler(self, ser1atts, ser2atts, ser3atts, conflicts):
            def next():
                print( len(self.table.selectedItems()) )
                if len( self.table.selectedItems() ) != len(conflicts): #===
                    msg = QtGui.QMessageBox(self) #===
                    msg.setText('Please selected one attribute per row') #===
                else:
                    msg = QtGui.QMessageBox(self)
                    msg.setText('Items selected')

            self.parent.nextButton.clicked.connect( next )

            attLabels = [str(conflict) for conflict in conflicts]
            confAtts1 = [ser1atts[conflict] for conflict in conflicts]
            confAtts2 = [ser2atts[conflict] for conflict in conflicts]
            
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
                tableItem = QtGui.QTableWidgetItem( self.parent.ser1obj.output()[0][att] )
                self.table.setItem(row, 0, tableItem)
                # Series 2
                tableItem = QtGui.QTableWidgetItem( self.parent.ser2obj.output()[0][att] )
                self.table.setItem(row, 1, tableItem)
            self.table.show()

        def serContHandler(self, ser1conts, ser2conts, ser3conts):
            return []

        def serZContHandler(self, ser1zconts, ser2zconts, ser3zconts):
            return []
         
def main():
    app = QtGui.QApplication(sys.argv)
    rmtFrame = mainFrame()
    a = mainFrame.serLoadWidget(rmtFrame)   
    sys.exit( app.exec_() )
main()