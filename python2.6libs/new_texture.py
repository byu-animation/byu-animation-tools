from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pyqt_houdini
import os, glob

class NewTextureDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('New Texture')
        self.create_layout()
        #self.create_connections()
        #self.refresh()

    def create_layout(self):
        self.asset_list = QComboBox()
        
        #Create file select button
        self.file_select_button = QPushButton('Select File')

        #Create selction layout
        selection_layout = QHBoxLayout()
        selection_layout.setSpacing(2)
        selection_layout.addWidget(self.asset_list)
        selection_layout.addWidget(self.file_select_button)
        
        #Create Ok and Cancel Buttons
        self.ok_button = QPushButton('OK')
        self.cancel_button = QPushButton('Cancel')
        
        #Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        #Create main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(2)
        main_layout.setMargin(2)
        main_layout.addLayout(selection_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

def go():
    app = QApplication.instance()
    if app is None:
        app = QApplication(['houdini'])
    dialog = NewTextureDialog()
    dialog.show()
    pyqt_houdini.exec_(app, dialog)
    
if __name__ == '__main__':
    go()