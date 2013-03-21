import messageSeverity as ms
import fileMode as fm
# TODO: Create generic file chooser function.



def infoWindow(message, wtitle=None, wbuttons=('Ok',), msev=ms.Message):
    '''Pop up an informational window with various buttons
    This function returns the index of the button pressed.'''
    raise NotImplementedError

def warningWindow(message, wtitle='Warning', wbuttons=('Ok','Cancel',), msev=ms.Warning):
    '''Pop up a warning window with an Ok and Cancel button
    This function returns the index of the button pressed.'''
    raise NotImplementedError


def listWindow(dlist, wtitle=None, wmessage=None, multi_select=False):
    '''Pop up an window with a list of options to choose from
    This function returns a tuple of indices that were selected. When cancel is
    pressed, the return value will be 'None'. '''
    raise NotImplementedError 

def inputWindow(wmessage, wtitle=None, initial_text=None, msev=ms.Message):
    '''Pop up a window with a text box to enter information into
    Returns the string entered or 'None' when the user cancels the window.'''
    raise NotImplementedError 

def passwordWindow(password, wtitle='Enter Password', wmessage='Enter Password', wlabel='Password'):
    '''Pop up a window with a text box to enter a password into
    Returns true when the password entered matches the password given as a 
    parameter and false otherwise.'''
    raise NotImplementedError 

def fileChooser(start_dir=None, wtitle=None, mode=fm.ReadAndWrite):
    '''Pop up a file chooser window'''
    raise NotImplementedError 

def shotDialog(slist, wtitle=None, rbuttons=('Model','Rig','Animation'), newShotIndices=(2,), wbuttons=('Ok','Cancel')):
    raise NotImplementedError 

