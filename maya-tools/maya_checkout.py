from PyQt4 import QtCore
from PyQt4 import QtGui

#import maya.cmds as mc
#import maya.OpenMayaUI as omu
import sip
import glob
import utilities as amu

def maya_main_window():
	#ptr = omu.MQtUil.mainWindow()
	#return sip.wrapinstance(long(ptr), QtCore.QObject)
	return QtGui.QMainWindow()

class CheckoutDialog(QtGui.QDialog):
		def __init__(self, parent=maya_main_window()):
				QtGui.QDialog.__init__(self, parent)
				self.setWindowTitle('Checkout')
				self.setFixedSize(330, 475)
				self.create_layout()
				self.create_connections()
				self.refresh()
		
		def create_layout(self):
				#Create the selected item list
				self.selection_list = QtGui.GListWidget()
				
				#Create Models, Rig, Animation
				self.radio_button_group = QTGui.QVButtonGroup('Select type')
				self.model_radio = QTGui.QRadioButton('Model', self.radio_button_group)
				self.rig_radio = QTGui.QRadioButton('Rig', self.radio_button_group)
				self.animation_radio = QTGui.QRadioButton('Animation', self.radio_button_group)
				self.model_radio.isChecked(1)
				
				#Create Select and Cancel buttons
				self.select_button = QTGui.QPushButton('Select')
				self.cancel_button = QTGui.QPushButton('Cancel')
				
				#Create button layout
				button_layout = QTGui.QHBoxLayout()
				button_layout.setSpacing(2)
				button_layout.addStretch()
				#button_layout.addWidget(self.models_button)
				#button_layout.addWidget(self.rigs_button)
				#button_layout.addWidget(self.animation_button)
				button_layout.addWidget(self.select_button)
				button_layout.addWidget(self.cancel_button)
				
				#Create main layout
				main_layout = QtGui.QVBoxLayout()
				main_layout.setSpacing(2)
				main_layout.setMargin(2)
				main_layout.addWidget(self.selection_list)
				main_layout.addWidget(self.radio_button_group)
				main_layout.addLayout(button_layout)
				
				self.setLayout(main_layout)
		
		def create_connections(self):
				#Connect the selected item list widget
				self.connect(self.selection_list,
							 QtCore.SIGNAL('currentItemChanged(QListWidgetItem*, QListWidgetItem*)'),
							 self.set_current_item)
				
				#Connect the buttons
				self.connect(self.select_button, QTCore.SIGNAL('clicked()'), self.checkout)
				self.connect(self.cancel_button, QTCore.SIGNAL('clicked()'), self.close_dialog)
		
		def update_selection(self, selection):
				#Remove all items from the list before repopulating
				self.selection_list.clear()
				
				#Add the list to select from
				for s in selection:
						item = QTGui.QListWidgetItem(s) #TODO might need to be basename
						self.selection_list.addItem(item)
		
		def refresh(self):
				if self.animation_radio.isChecked():
						selections = glob.glob(os.path.join(os.environ['ANIMATION_DIR'], '*'))
				else:
						selections = glob.glob(os.path.join(os.environ['ASSETS_DIR'], '*'))
				update_selection(self, selections)
		
		def get_checkout_mode(self):
				if self.animation_radio.isChecked():
						return ''
		
		def get_filename(self, parentdir):
				return os.path.basename(os.path.dirname(parentdir))+'_'+os.path.basename(parentdir)
		
		########################################################################
		# SLOTS
		########################################################################
		def checkout(self):
				asset_name = str(current_item.text())
				if self.animation_radio.isChecked():
						toCheckout = os.path.join(os.environ['ANIMATION_DIR'], asset_name)
						destpath = amu.checkout(toCheckout, True)
						toOpen = os.path.join(destpath, get_filename(toCheckout)+'.mb')
						print toOpen
						#TODO open the file
		
		def close_dialog(self):
				self.close()
		
		def set_current_item(self, item):
				self.current_item = item
		
		
if __name__ == '__main__':
		dialog = CheckoutDialog()
		dialog.show()