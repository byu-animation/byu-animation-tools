import maya.cmds as cmds
import utilities as amu #asset manager utilities
import os

def checkin():
	cmds.file(save=True, force=True) #save file
	filePath = cmds.file(query=True, list=True)[0].encode('utf-8')
	toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
	if amu.canCheckin(toCheckin):
		cmds.file(force=True, new=True) #open new file
		amu.checkin(toCheckin) #checkin

def go():
	checkin()
