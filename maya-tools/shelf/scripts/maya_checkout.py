from PyQt4.QtCore import *
from PyQt4.QtGui import *

#import maya.cmds as mc
#import maya.OpenMayaUI as omu
import sip
import os, glob
import utilities as amu

#def maya_main_window():
	#ptr = omu.MQtUil.mainWindow()
	#return sip.wrapinstance(long(ptr), QObject)
#	return QMainWindow()

class CheckoutDialog(QDialog):
	#def __init__(self, parent=maya_main_window()):
	def setup(self, parent):
		QDialog.__init__(self, parent)
		self.setWindowTitle('Checkout')
		self.setFixedSize(330, 475)
		self.create_layout()
		self.create_connections()
		self.refresh()
	
	def create_layout(self):
		#Create the selected item list
		self.selection_list = QListWidget()
		
		#Create Models, Rig, Animation
		radio_button_group = QVBoxLayout()
		self.model_radio = QRadioButton('Model')#, self.radio_button_group)
		self.rig_radio = QRadioButton('Rig')#, self.radio_button_group)
		self.animation_radio = QRadioButton('Animation')#, self.radio_button_group)
		self.model_radio.setChecked(True)
		radio_button_group.setSpacing(2)
		radio_button_group.addStretch()
		radio_button_group.addWidget(self.model_radio)
		radio_button_group.addWidget(self.rig_radio)
		radio_button_group.addWidget(self.animation_radio)
		
		#Create Select and Cancel buttons
		self.select_button = QPushButton('Select')
		self.cancel_button = QPushButton('Cancel')
		
		#Create button layout
		button_layout = QHBoxLayout()
		button_layout.setSpacing(2)
		button_layout.addStretch()
		button_layout.addWidget(self.select_button)
		button_layout.addWidget(self.cancel_button)
		
		#Create main layout
		main_layout = QVBoxLayout()
		main_layout.setSpacing(2)
		main_layout.setMargin(2)
		main_layout.addWidget(self.selection_list)
		main_layout.addLayout(radio_button_group)
		main_layout.addLayout(button_layout)
		
		self.setLayout(main_layout)
	
	def create_connections(self):
		#Connect the selected item list widget
		self.connect(self.selection_list,
					SIGNAL('currentItemChanged(QListWidgetItem*, QListWidgetItem*)'),
					self.set_current_item)
			
		#Connect the buttons
		self.connect(self.model_radio, SIGNAL('clicked()'), self.refresh)
		self.connect(self.rig_radio, SIGNAL('clicked()'), self.refresh)
		self.connect(self.animation_radio, SIGNAL('clicked()'), self.refresh)
		self.connect(self.select_button, SIGNAL('clicked()'), self.checkout)
		self.connect(self.cancel_button, SIGNAL('clicked()'), self.close_dialog)
	
	def update_selection(self, selection):
		#Remove all items from the list before repopulating
		self.selection_list.clear()
		
		#Add the list to select from
		for s in selection:
			item = QListWidgetItem(os.path.basename(s)) #TODO might need to be basename
			self.selection_list.addItem(item)
	
	def refresh(self):
		if self.animation_radio.isChecked():
			selections = glob.glob(os.path.join(os.environ['ANIMATION_DIR'], '*'))
		else:
			selections = glob.glob(os.path.join(os.environ['ASSETS_DIR'], '*'))
		self.update_selection(selections)
	
	def get_checkout_mode(self):
		if self.animation_radio.isChecked():
			return ''
	
	def get_filename(self, parentdir):
		return os.path.basename(os.path.dirname(parentdir))+'_'+os.path.basename(parentdir)
	
	########################################################################
	# SLOTS
	########################################################################
	def checkout(self):
		asset_name = str(self.current_item.text())
		if self.model_radio.isChecked():
			toCheckout = os.path.join(os.environ['ASSETS_DIR'], asset_name, 'model')
		elif self.rig_radio.isChecked():
			toCheckout = os.path.join(os.environ['ASSETS_DIR'], asset_name, 'rig')
		elif self.animation_radio.isChecked():
			toCheckout = os.path.join(os.environ['ANIMATION_DIR'], asset_name)
		
		destpath = amu.checkout(toCheckout, True)
		toOpen = os.path.join(destpath, self.get_filename(toCheckout)+'.mb')
		#TODO open the file
		print toCheckout
		print toOpen
	
	def close_dialog(self):
		self.close()
	
	def set_current_item(self, item):
		self.current_item = item
		

def go():
	import sys
	app = QApplication(sys.argv)
	MainWindow = QMainWindow()
	dialog = CheckoutDialog()
	dialog.setup(MainWindow)
	#MainWindow.show()
	dialog.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	go()
	
	
	
	
	
	
	
	
	
	
