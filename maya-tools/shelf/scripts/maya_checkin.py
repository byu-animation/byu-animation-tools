import maya.cmds as cmds
import utilities as amu #asset manager utilities
import os

def save_file():
        cmds.file(save=True, force=True) #save file

def save_objs():
        pass

def showFailDialog(): 
        return cmds.confirmDialog( title         = 'Checkin Failed'
                                 , message       = 'Checkin was unsuccessful'
                                 , button        = ['Retry', 'Cancel']
                                 , defaultButton = 'Retry'
                                 , cancelButton  = 'Cancel'
                                 , dismissString = 'Cancel')

def checkin():
        save_file() # save the file before doing anything

        success = False
        while not success: # failure dialog loop 
                filePath = cmds.file(query=True, list=True)[0].encode('utf-8')
                toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
                if amu.canCheckin(toCheckin):
                        save_objs() # save objs first
                        cmds.file(force=True, new=True) #open new file
                        amu.checkin(toCheckin) #checkin
                        success = True
                else:
                        response = showFailDialog()
                        success = 'Cancel' == response

def go():
        checkin()
