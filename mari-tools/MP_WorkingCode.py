# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
# ------------------------------------------------------------------------------

import os
import mari
import random
import PythonQt.QtGui as gui

# ------------------------------------------------------------------------------
#GLOBALS & ENVIROMENT VARIABLES
JOB = "/groups/owned/PRODUCTION/assets/"

projectName = "MariPipe"


# ------------------------------------------------------------------------------
def projectCreate():
	#DIR Creation
	projectName = "MariPipeTest"
	DIRpath = os.path.join(JOB, projectName, "mariFiles")
	print (DIRpath)
	if not os.path.exists(DIRpath): 
		os.makedirs(DIRpath)
	folderList = ["Maps", "OBJs", "Projectors", "Refrence", "TurnTables", "Archives"]
	for i in folderList:
		subDIRpath = os.path.join(DIRpath, i)
		print (subDIRpath)
		if not os.path.exists(subDIRpath): 
			os.makedirs(subDIRpath)

# ------------------------------------------------------------------------------
def mariProjectCreate():
	"This creates a project with a set of default options. Import each OBJ like this"
	mari.projects.close()
	obj_name = QFileDialog.getOpenFileName(None, "Select a .obj file", "/", "*.obj")
	if os.path.exists(obj_name):
		#What default layers are created
		mari.projects.create("projectName", obj_name,
			[mari.ChannelInfo('DIFF', 2048, 2048, 16, False, mari.Color(0, 0, 0), mari.setFileTemplate($ENTITY_$CHANNEL_$UDIM.png),mari.setPath(InsertPathHere),),
			mari.ChannelInfo('SPEC', 2048, 2048, 16, False, mari.Color(0.5, 0.5, 0.5), mari.setFileTemplate($ENTITY_$CHANNEL_$UDIM.png)),
			mari.ChannelInfo('DSP', 2048, 2048, 16, True, mari.Color(0.5, 0.5, 0.5), mari.setFileTemplate($ENTITY_$CHANNEL_$UDIM.png))])

# ------------------------------------------------------------------------------
def buildBYUSelf():
	#Menu Shelf Creation Set
	mari.actions.create("TestAction", "mari.utils.message("Test")")
	mari.menus.addAction(action,"MariWindow/BYU Tools")
	action.setShortcut("Ctrl + H")
	#SubDirs that need to be created... Projectors, Project Maps(Bypass texture Tool!)?, TurnTabels, Refrence

	#Palette Creation Set
	gui = PythonQt.QtGui
	mainPal = mari.palettes.create("BYU Mari Tools")
	widget = gui.QWidget()
	mainPal.setBodyWidget(widget)
	layout = gui.QVBoxLayout()
	widget.setLayout(layout)
	layout.addWidget(qui.QLabel("Welcome to the palette"))
	createProjectPB = qui.QPushButton("Create Project")
	layout.addWidget(createProjectPB)
	connect(createProjectPB.clicked, projectCreate)
	mainPal.show
# ------------------------------------------------------------------------------
def OBJUpdate():
	pass

# ------------------------------------------------------------------------------
def exportMaps():
	pass		

# ------------------------------------------------------------------------------
def archiveAsset():
	pass

# ------------------------------------------------------------------------------
def DSPAssetInfo():
	pass

# ------------------------------------------------------------------------------
def turnTableRender():
	pass

# ------------------------------------------------------------------------------
def saveAll():
	pass






