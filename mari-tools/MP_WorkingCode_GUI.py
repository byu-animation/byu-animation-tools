# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
#Pop Up Gui and Shelf Gui
# ------------------------------------------------------------------------------


import os
import mari
import random
import PythonQt.QtGui as gui
#import MP_WorkingCode_archiveAsset
#import MP_WorkingCode_AssetInfo
#import MP_WorkingCode_exportMaps
#import MP_WorkingCode_mariProjCreate
#import MP_WorkingCode_OBJUpdate
#import MP_WorkingCode_saveAll
#import MP_WorkingCode_turnTableRender

# ------------------------------------------------------------------------------
def DSPAssetInfo():
	printInfoList = mari.projects.list()
	print "--------------------------------------"
	print (printInfoList)
	print "--------------------------------------"
# ------------------------------------------------------------------------------
mainPal = mari.palettes.create("BYU Mari Tools")
widget = gui.QWidget()
widget.resize(225, 275)
mainPal.setBodyWidget(widget)
layout = gui.QVBoxLayout()
widget.setLayout(layout)
layout.addWidget(gui.QLabel("Welcome to the uber palette."))

# ------------------------------------------------------------------------------
#ButtonCreation
createProjectPB = gui.QPushButton("Create Project")
layout.addWidget(createProjectPB)
#connect(createProjectPB.clicked, projectCreate)

updateOBJPB = gui.QPushButton("Update OBJs")
layout.addWidget(updateOBJPB)
#connect(updateOBJPB.clicked, OBJUpdate)

ExportMapsPB = gui.QPushButton("Export All Maps")
layout.addWidget(ExportMapsPB)
#connect(ExportMapsPB.clicked, exportMaps)

archiveAssetPB = gui.QPushButton("Archive Asset")
layout.addWidget(archiveAssetPB)
#connect(archiveAssetPB.clicked, archiveAsset)

AssetInfoPB = gui.QPushButton("Display Asset Info")
layout.addWidget(AssetInfoPB)
connect(AssetInfoPB.clicked, DSPAssetInfo)

turnTablePB = gui.QPushButton("Turntable Render")
layout.addWidget(turnTablePB)

#VersionSlider
#connect(turnTablePB.clicked, turnTableRender)

savePB = gui.QPushButton("Save and Close")
layout.addWidget(savePB)
#connect(savePB.clicked, saveAll)

# ------------------------------------------------------------------------------
mainPal.show
widget.resize(225, 275)
