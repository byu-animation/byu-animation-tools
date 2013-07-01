from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os, glob
import utilities as amu
import nuke

class CheckoutDialog(QDialog):

    def __init__(self, parent=QApplication.activeWindow()):
        QDialog.__init__(self, parent)
        self.create_layout()
        self.populate_list()
        self.create_connections()
    
    def create_layout(self):
        self.selection_list = QListWidget()
        self.select_button = QPushButton('Select')
        self.info_button = QPushButton('Get Info')
        self.cancel_button = QPushButton('Cancel')
        
        button_layout = QVBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.info_button)
        button_layout.addWidget(self.cancel_button)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(2)
        main_layout.setMargin(10)
        main_layout.addWidget(self.selection_list)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def create_connections(self):
        self.connect(self.selection_list,SIGNAL('currentItemChanged(QListWidgetItem*, QListWidgetItem*)'),self.set_current_item)
        self.connect(self.select_button, SIGNAL('clicked()'), self.checkout)
        #self.connect(self.info_button, SIGNAL('clicked()'), self.show_node_info)
        self.connect(self.cancel_button, SIGNAL('clicked()'), self.close_dialog)
    
    def close_dialog(self):
        self.close()

    def get_filename(self, parentdir):
        return os.path.basename(os.path.dirname(parentdir))+'_'+os.path.basename(parentdir)

    def checkout(self):
        asset_name = str(self.current_item.text())
        toCheckout = os.path.join(os.environ['SHOTS_DIR'], asset_name,'compositing')
        try:
            destpath = amu.checkout(toCheckout, True)
        except Exception as e:
            if not amu.checkedOutByMe(toCheckout):
                nuke.message(str(e))
                return
            else:
                destpath = amu.getCheckoutDest(toCheckout)
        toOpen = os.path.join(destpath,self.get_filename(toCheckout)+'.nk')
        if os.path.exists(toOpen):
            nuke.scriptOpen(toOpen)
            nuke.message('Checkout Successful')
            self.close()
        else:
            nuke.message('No File Found'+toOpen)

    def populate_list(self):
        selection = glob.glob(os.path.join(os.environ['SHOTS_DIR'], '*'))
        for s in selection:
            item = QListWidgetItem(os.path.basename(s))
            item.setText(os.path.basename(s))
            self.selection_list.addItem(item)
        self.selection_list.sortItems(0)

    def set_current_item(self, item):
        self.current_item = item


def go():
    #nuke.message("go")
    dialog = CheckoutDialog()
    #dialog.show()
    dialog.exec_()
    #nuke.message("done")

