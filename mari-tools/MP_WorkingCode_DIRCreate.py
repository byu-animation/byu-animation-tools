# Code by Andrew Rasmussen 2013... When it is terrible blame him. Or bake him pity cookies.
# ------------------------------------------------------------------------------

import os
import random

# ------------------------------------------------------------------------------
#GLOBALS & ENVIROMENT VARIABLES
#JOB = "home\username\groups\owned\PRODUCTION\assets\"
JOB = "/groups/owned/PRODUCTION/assets/"
#MARI_SCRIPT_PATH = whereEverBrianSays

#projectName = userSelection
projectName = "MariPipeTest"

# ------------------------------------------------------------------------------
def projectCreate():
	#DIR Creation
	projectName = "MariPipeTest"
	DIRpath = os.path.join(JOB, projectName, "mariFiles")
	print (DIRpath)
	if not os.path.exists(DIRpath): 
		os.makedirs(DIRpath)
	folderList = ["Maps", "OBJs", "Projectors", "Refrence", "TurnTables", "Archives"]
#	for (int i=0; i<w; i++)	
	for i in folderList:
		subDIRpath = os.path.join(DIRpath, i)
		print (subDIRpath)
		if not os.path.exists(subDIRpath): 
			os.makedirs(subDIRpath)

# ------------------------------------------------------------------------------
projectCreate()
