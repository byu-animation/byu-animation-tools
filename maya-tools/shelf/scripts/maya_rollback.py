from PyQt4.QtCore import *
from PyQt4.QtGui import *

import maya.cmds as cmd
import maya.OpenMayaUI as omu
import sip
import os, glob
import utilities as amu

CHECKOUT_WINDOW_WIDTH = 330
CHECKOUT_WINDOW_HEIGHT = 400
ORIGINAL_FILE_NAME = cmd.file(query=True, sceneName=True)

def maya_main_window():
    ptr = omu.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QObject)

class RollbackDialog(QDialog):
    def __init__(self, parent=maya_main_window()):
    #def setup(self, parent):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Rollback')
        self.setFixedSize(CHECKOUT_WINDOW_WIDTH, CHECKOUT_WINDOW_HEIGHT)
        self.create_layout()
        self.create_connections()
        self.refresh()

    def create_layout(self):
        #Create the selected item list
        self.selection_list = QListWidget()
        self.selection_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding) 

        #Create Select and Cancel buttons
        self.open_button = QPushButton('Open Version')
        self.select_button = QPushButton('Rollback')
        self.cancel_button = QPushButton('Cancel')

        #Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.cancel_button)

        #Create main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(2)
        main_layout.setMargin(2)
        main_layout.addWidget(self.selection_list)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def create_connections(self):
        #Connect the selected item list widget
        self.connect(self.selection_list,
                    SIGNAL('currentItemChanged(QListWidgetItem*, QListWidgetItem*)'),
                    self.set_current_item)
            
        #Connect the buttons
        self.connect(self.open_button, SIGNAL('clicked()'), self.open_version)
        self.connect(self.select_button, SIGNAL('clicked()'), self.rollback)
        self.connect(self.cancel_button, SIGNAL('clicked()'), self.close_dialog)

    def update_selection(self, selection):
        #Remove all items from the list before repopulating
        self.selection_list.clear()

        #Add the list to select from
        for s in selection:
            item = QListWidgetItem(os.path.basename(s)) 
            item.setText(os.path.basename(s))
            self.selection_list.addItem(item)
        self.selection_list.sortItems(0)

    def refresh(self):
        filePath = os.path.split(ORIGINAL_FILE_NAME)[0]
        checkInDest = amu.getCheckinDest(filePath)
        versionFolders = os.path.join(checkInDest, "src")
        selections = glob.glob(os.path.join(versionFolders, '*'))
        self.update_selection(selections)

    def get_checkout_mode(self):
        return ''

    def get_filename(self, parentdir):
        return os.path.basename(os.path.dirname(parentdir))+'_'+os.path.basename(parentdir)

    ########################################################################
    # SLOTS
    ########################################################################
    def rollback(self):
        dialogResult = self.showWarningDialog()
        if dialogResult == 'Yes':
            version = str(self.current_item.text())[1:]
            dirPath = os.path.split(ORIGINAL_FILE_NAME)[0]
            print dirPath
            cmd.file(force=True, new=True)
            amu.setVersion(dirPath, int(version))
            self.close()
                
    def close_dialog(self):
        print ORIGINAL_FILE_NAME
        cmd.file(ORIGINAL_FILE_NAME, force=True, open=True)
        self.close()

    def set_current_item(self, item):
        self.current_item = item

    def showWarningDialog(self):
        return cmd.confirmDialog(  title           = 'WARNING!'
                                   , message       = 'YOU ARE ABOUT TO DELETE ALL VERSIONS OF THIS ASSET NEWER THAN THE VERSION YOU SELECTED. Are you absolutely sure that this is what you want to do?'
                                   , button        = ['Yes', 'No']
                                   , defaultButton = 'No'
                                   , cancelButton  = 'No'
                                   , dismissString = 'No')

    def show_no_file_dialog(self):
        return cmd.confirmDialog(  title           = 'No Such Version'
                                   , message       = 'For some reason this version folder does not contain a file. Please try another version.'
                                   , button        = ['Ok']
                                   , defaultButton = 'Ok'
                                   , cancelButton  = 'Ok'
                                   , dismissString = 'Ok')

    def open_version(self):
        filePath = os.path.split(ORIGINAL_FILE_NAME)[0]
        checkInDest = amu.getCheckinDest(filePath)
        v = str(self.current_item.text())
        checkinPath = os.path.join(checkInDest, "src", v)
        checkinName = os.path.join(checkinPath, os.path.basename(ORIGINAL_FILE_NAME))
        print checkinName
        if os.path.exists(checkinName):
            cmd.file(checkinName, force=True, open=True)
        else:
            self.show_no_file_dialog()

def go():
    dialog = RollbackDialog()
    dialog.show()
    
if __name__ == '__main__':
    if ORIGINAL_FILE_NAME != '':
        cmd.file(save=True, force=True)
        go()
