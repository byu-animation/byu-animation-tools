import maya.cmds as cmds
import utilities as amu #asset manager utilities
import brent
import os

def showWarningDialog(): 
        return cmds.confirmDialog( title         = 'Discard Confirmation' 
                                 , message       = 'YOU ARE ABOUT TO IRREVOKABLY DISCARD ALL CHANGES YOU HAVE MADE. '
                                                   'Please think this through very carefully.\r\n\r\nNow that we have '
                                                   'gotten that straightened out, are you sure you want to discard '
                                                   'your changes?'
                                 , button        = ['Yes', 'No', 'Brent']
                                 , defaultButton = 'No'
                                 , cancelButton  = 'No'
                                 , dismissString = 'No')

def discard():
        filePath=cmds.file(q=True, sceneName=True)
        if not filePath:
          return
        print filePath
        dlgResult = showWarningDialog()
        if dlgResult == 'Yes':
                # get discard directory before opening new file
                toDiscard = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
                if(amu.isCheckedOutCopyFolder(toDiscard)): 
                        cmds.file(force=True, new=True) #open new file
                        amu.discard(toDiscard) # discard changes
                else:
                        cmds.confirmDialog(  title         = 'Invalid Command'
                                           , message       = 'This is not a checked out file. There is nothing to discard.'
                                           , button        = ['Ok']
                                           , defaultButton = 'Ok'
                                           , cancelButton  = 'Ok'
                                           , dismissString = 'Ok')

        elif dlgResult == 'Brent':
                brent.go()
        else:
                cmds.confirmDialog(  title         = 'Discard Cancelled'
                                   , message       = 'Thank you for being responsible.'
                                   , button        = ['Ok']
                                   , defaultButton = 'Ok'
                                   , cancelButton  = 'Ok'
                                   , dismissString = 'Ok')
                                   

def go():
        discard()

