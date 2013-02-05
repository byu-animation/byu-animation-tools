import maya.cmds as cmds

def speak_brent():
	cmds.confirmDialog(  title          = 'Speak Brent!'
                       , message       = "We're in finish mode. Kay?"
                       , button        = ['Ok']
                       , defaultButton = 'Ok'
                       , cancelButton  = 'Ok'
                       , dismissString = 'Ok')

## The shelf will call this method each time
## the button is pressed. If you want something
## to run each time, put it here.
def go():
    speak_brent()
