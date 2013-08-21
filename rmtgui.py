from PySide import QtGui, QtCore
import reconstructmergetool as rmt
import sys
from Series import *

# To Do:
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
        
        # Data
        self.ser1path = None # Populated in serLoadWidget.loadSeries()
        self.ser2path = None # "
        self.ser1obj = None # "
        self.ser2obj = None # "
        self.serName = None # "
        self.mergedAtts = None # Populated in serAttributeWidget.nextStep()
        self.mergedSeries = None # Populated in self.mkMergeSer()
        self.mergedConts = None # Populated in serContourWidget.nextStep()
        self.mergedZConts = None # Populated in serZContourWidget.nextStep()
        
        self.initUI()
        
    def initUI(self):
        # Quit Button
        quitButton = QtGui.QPushButton(self)
        quitButton.setText('Quit')
        quitButton.clicked.connect( QtCore.QCoreApplication.instance().quit )
        
        # Window Dimensions and Attributes
        self.setGeometry(0,0,800,600)
        self.setWindowTitle('Reconstructmergetool v.1')
        self.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        # Name indicator: shown in bot-left corner after Series() object is created
        self.nameIndicator = QtGui.QPushButton(self)
        self.nameIndicator.hide()
        
        # Layout
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(quitButton)
        hbox.insertWidget(0, self.nameIndicator)
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        
        self.show()
    
    def mkMergeSer(self):
        '''Creates a Series object with attributes and name.
        Does not contain contours or sections'''
        self.mergedSeries = Series( root=ET.Element('Series', self.mergedAtts), name=self.serName ) #=== where to pick name?
        self.nameIndicator.setText('Output Series: '+self.serName)
        self.nameIndicator.show()
        
class serLoadWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()
        # Data
        self.parent = parent
        
    def initUI(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setGeometry(0,0,800,500)
        
        # Load Series Buttons
        self.ser1Button = QtGui.QPushButton('Load Series 1\n(may take a few seconds)', parent=self)
        self.ser1Button.setGeometry(400-150,100,300,100)
        self.ser1Button.clicked.connect( self.loadSeries )
        
        self.ser2Button = QtGui.QPushButton('Load Series 2\n(may take a few seconds)', parent=self)
        self.ser2Button.setGeometry(400-150,250,300,100)
        self.ser2Button.clicked.connect( self.loadSeries )
        
        # Series Name lineEdit
        self.lineEd = QtGui.QLineEdit(self)
        self.lineEd.setText('<Enter name for new series>')
        self.lineEd.setGeometry(400-100,362,200,25)
        self.lineEd.setAlignment(QtCore.Qt.AlignCenter)
        
        # Continue button
        self.continueButton = QtGui.QPushButton(self)
        self.continueButton.setText('Load both series\nto continue')
        self.continueButton.setGeometry(400-75,400,150,75)
        self.continueButton.setFlat(True)
        
        self.show()
        
    def loadSeries(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                                                     "Load Series",
                                                     "/home/",
                                                     "Series File (*.ser)")
        # Change appropriate path
        if self.sender() == self.ser1Button:
            self.parent.ser1path = str(fileName[0])
            self.parent.ser1obj = rmt.getSeries(self.parent.ser1path)
            self.ser1Button.setText(self.parent.ser1path) # new text = ser name
            self.ser1Button.setFlat(True)
        elif self.sender() == self.ser2Button:
            self.parent.ser2path = str(fileName[0])
            self.parent.ser2obj = rmt.getSeries(self.parent.ser2path)
            self.ser2Button.setText(self.parent.ser2path)
            self.ser2Button.setFlat(True)
            
        self.checkContinueButton()
        
    def checkContinueButton(self):
        # Check to see if both series are loaded
        if self.parent.ser1path != None and self.parent.ser2path != None:
            self.continueButton.show()
            self.continueButton.setText('Continue')
            self.continueButton.setFlat(False)
            self.continueButton.clicked.connect( self.nextStep )
            
    def nextStep(self):
        '''Updates data in the mainFrame() class'''
        print('New series name: '+str(self.lineEd.text()))
        if self.lineEd.text() == None or self.lineEd.text() == '<Enter name for new series>' or self.lineEd.text() == '':
            err = QtGui.QMessageBox(self)
            err.setText('Please enter a name for the new series')
            err.show()
        else:
            name = self.lineEd.text()
            if '.ser' in name:
                name = name.replace('.ser','') # series names dont have .ser in them
            self.parent.serName = name
            serAttributeWidget(self.parent)
            self.close()     
              
class serAttributeWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        # Data
        self.parent = parent
        self.ser1obj = parent.ser1obj
        self.ser2obj = parent.ser2obj
        self.initUI()
        
        self.setGeometry(0,0,800,500)
        
    def initUI(self):
        self.table = serAttributeTable(parent = self)
        
        # Continue button
        self.continueButton = QtGui.QPushButton(self.parent) # Parent = mainFrame()
        self.continueButton.setText('Continue')
        self.continueButton.setGeometry(400-75,500,150,75)
        self.continueButton.clicked.connect( self.nextStep )
    
        self.continueButton.show()
        self.show()
        
    def nextStep(self):
        selectedAtts = self.table.selectedItems() # dictionary of selected attributes
        if len(selectedAtts) != 86:
            err = QtGui.QMessageBox(self)
            err.setText('Please select one item per row to continue\n(86 items total must be selected)\nClick on the series name to choose all attributes for that series')
            err.show()
        else:
            self.parent.mergedAtts = self.table.returnItems() # turns selectedItems() to a dictionary
            self.continueButton.close()
            self.parent.mkMergeSer()
            serContourWidget(self.parent)
            self.close()
    def serAttHandler(self): # rmt.serAttHandler(ser1atts, ser2atts, ser3atts, conflicts)
        
        
        
        return
    
class serAttributeTable(QtGui.QTableWidget):
    '''Receives a parent frame, series1 attributes and series2 attributes. Provides a table display
    GUI for selecting and outputting the attributes to be included in the merged series'''
    def __init__(self, parent=None):
        QtGui.QTableWidget.__init__(self, len(parent.ser1obj.output()[0]), 2, parent=parent)
        self.parent = parent
        self.ser1obj = self.parent.ser1obj
        self.ser2obj = self.parent.ser2obj
        # Create table
        self.setGeometry(0,0,800,500)
        self.setColumnWidth(0, 318)
        self.setColumnWidth(1, 318)
        
        # Make attribute labels for rows, series names for columns
        self.setHorizontalHeaderLabels( [self.ser1obj.name, self.ser2obj.name] )
        self.setVerticalHeaderLabels( [attribute for attribute in self.ser1obj._attribs] )
        
        # Some rows need to be taller to show all output
        self.setWordWrap(True)
        self.resizeRowsToContents()
        self.setRowHeight(55, 100) # borderColors
        self.setRowHeight(56, 100) # fillcolors
        self.setRowHeight(83, 75) # mvmtIncrement
        self.setRowHeight(84, 75) # ctrlIncrement
        self.setRowHeight(85, 75) # shiftIncrement
        
        # Load table with attributes
        for row in range(len(self.ser1obj.output()[0])):
            header = self.verticalHeaderItem(row).text()
            # Series 1
            tableItem = QtGui.QTableWidgetItem( self.ser1obj.output()[0][header] )
            self.setItem(row,0,tableItem)
            # Series 2
            tableItem = QtGui.QTableWidgetItem( self.ser2obj.output()[0][header] )
            self.setItem(row,1,tableItem)
        
        self.show()
        
    def returnItems(self):
        '''Returns dictionary of selected attributes'''
        selAtts = [ str(item.text()) for item in self.selectedItems() ]
        attDict = {}
        for att in self.ser1obj._attribs:
            attDict[att] = selAtts.pop(0)
        return attDict

class serContourWidget(QtGui.QWidget): #===
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()
        
    def initUI(self):
        self.setGeometry(0,0,800,500)
        
        # Instructional message
        msg = QtGui.QMessageBox(self)
        msg.setText('Please select a set of series contours to be output to the merged series')
        msg.show()
        
        
        self.show()
        
def main():
    app = QtGui.QApplication(sys.argv)
    rmtFrame = mainFrame()
    serLoadWidget( rmtFrame )
    sys.exit( app.exec_() )
main()