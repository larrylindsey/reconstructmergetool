from PySide import QtGui, QtCore
import sys

class widgetWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(0,0,500,500)

        self.button = QtGui.QPushButton(self)
        self.button.setText('Button')
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        
        self.show()
class cheese(widgetWindow):
    def __init__(self, parent=None):
        widgetWindow.__init__(self,parent)
        self.setWindowTitle('Cheese')
        self.button.hide()
def main():
    app = QtGui.QApplication(sys.argv)
    a = cheese()
    sys.exit( app.exec_() )
    
main()