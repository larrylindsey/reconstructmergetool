import excelTool
import sys, os
from PySide import QtGui, QtCore

class excelToolWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setGeometry(0,0,800,500)
        self.seriesPathLine = None
        self.seriesPathBrowse = None
        self.seriesPath = 'Enter or browse path to series'
        self.savePathLine = None
        self.savePathBrowse = None
        self.savePath = 'Enter or browse path to save excel workbook'
        self.goButton = None
        
        self.functionalItems()
        self.layout()
        self.show()
        
        
    def functionalItems(self):
        self.seriesPathLine = QtGui.QLineEdit(self)
        self.seriesPathLine.setText( self.seriesPath )
        
        self.seriesPathBrowse = QtGui.QPushButton(self)
        self.seriesPathBrowse.setIconSize(QtCore.QSize(25,25))
        self.seriesPathBrowse.setText('Browse')
        
        self.savePathLine = QtGui.QLineEdit(self)
        self.savePathLine.setText( self.savePath )
        
        self.savePathBrowse = QtGui.QPushButton(self)
        self.savePathBrowse.setIconSize(QtCore.QSize(25,25))
        self.savePathBrowse.setText('Browse')
        
        self.goButton = QtGui.QPushButton(self)
        self.goButton.setText('Go')
        

    def layout(self):
        vbox = QtGui.QVBoxLayout()
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget( self.seriesPathLine )
        hbox1.addWidget( self.seriesPathBrowse )
        hbox1.insertSpacing(0,150)
        hbox1.insertSpacing(-1,150)
        
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget( self.savePathLine )
        hbox2.addWidget( self.savePathBrowse )
        hbox2.insertSpacing(0,150)
        hbox2.insertSpacing(-1,150)
        
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget( self.goButton )
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        self.setLayout(vbox)

    def browseSer(self):
            '''Displays file browser and updates text in s1bar or s2bar.
            Parent data is not updated until next button function is executed
            successfully.'''
            if self.sender() == self.seriesPathBrowse:
                path = QtGui.QFileDialog.getOpenFileName(self,
                                                     'Load Series',
                                                     '/home/',
                                                     'Series File (*.ser)')
                path = str(path[0])
                self.seriesPathLine.setText(path)
            elif self.sender() == self.savePathBrowse:
                self.savePathLine.setText(path)
def main():
    app = QtGui.QApplication(sys.argv)
    t = excelToolWindow()
    sys.exit( app.exec_() )
main()
    