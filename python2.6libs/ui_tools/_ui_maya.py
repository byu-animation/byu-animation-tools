import _ui_base
import maya.cmds as mc

# TODO: Everything!

# Make local functions aliases of the functions we ought to use
def infoWindow(wmessage, wtitle=None, wbuttons=('Ok',), msev=ms.Message):
    '''Pop up an informational window with various buttons

This function returns the index of the button pressed.'''
    retval = mc.confirmDialog(message=wmessage, title=wtitle, button=wbutton)
    return False # Put real logic here

listWindow = _ui_base.listWindow
warningWindow = _ui_base.warningWindow
inputWindow = _ui_base.inputWindow
passwordWindow = _ui_base.passwordWindow
fileChooser = _ui_base.fileChooser
shotDialog = _ui_base.shotDialog

