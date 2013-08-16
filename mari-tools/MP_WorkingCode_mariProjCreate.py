# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
# ------------------------------------------------------------------------------

import os
import mari
import random
import PythonQt.QtGui as gui
import MP_WorkingCodeDIRCreate

# ------------------------------------------------------------------------------
#GLOBALS & ENVIROMENT VARIABLES
JOB = "/groups/owned/PRODUCTION/assets/"

projectName = "MariPipe"

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
mariProjectCreate()



mari.projects.showCreateDialog()
