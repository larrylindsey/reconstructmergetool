from PySide import QtGui, QtCore
import sys

class mainFrame(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(0,0,500,500)

        # QUIT
        self.quitButton = QtGui.QPushButton(self)
        self.quitButton.setGeometry(QtCore.QRect(400, 475, 96, 27))
        self.quitButton.setObjectName("quitButton")
        self.quitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.quitButton.setText(QtGui.QApplication.translate("Form", "Quit :(",
                                                             None, QtGui.QApplication.UnicodeUTF8))
        self.show()
        
class serLoadWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
  
        # FRAME
        self.frame = QtGui.QFrame(parent)
        self.frame.setGeometry(QtCore.QRect(0, 0, 475, 475))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        # LAYOUT
        self.horizontalLayoutWidget = QtGui.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(59, 90, 441, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")       
         
        # LOAD SERIES 1
        self.ser1Button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.ser1Button.setObjectName("ser1Button")
        self.horizontalLayout.addWidget(self.ser1Button)
        self.ser1Button.setText(QtGui.QApplication.translate("Form", "Load Series 1", None, QtGui.QApplication.UnicodeUTF8))
        self.ser1path = self.ser1Button.clicked.connect(self.loadSeries)
        self.ser1Button.show()
        
        # LOAD SERIES 2
        self.ser2Button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.ser2Button.setObjectName("ser2Button")
        self.horizontalLayout.addWidget(self.ser2Button)
        self.ser2Button.setText(QtGui.QApplication.translate("Form", "Load Series 2", None, QtGui.QApplication.UnicodeUTF8))
        self.ser2path = self.ser2Button.clicked.connect(self.loadSeries)      
    
        self.frame.show()
        
    def loadSeries(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.setNameFilter('Series files (*.ser)')
        dialog.setViewMode(QtGui.QFileDialog.Detail)
        if dialog.exec_():
            seriesPath = dialog.selectedFiles()
            return seriesPath
        else:
            return None
def main():
    app = QtGui.QApplication(sys.argv)
    win = mainFrame()
    serLoadWindow(win)
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()