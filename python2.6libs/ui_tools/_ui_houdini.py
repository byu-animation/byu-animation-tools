import _ui_base
import hou
import messageSeverity as ms
import fileMode as fm
# TODO: Implement shotDialog function.

def _hsev(mesSev):
    if mesSev == ms.Message:
        return hou.severityType.Message
    elif mesSev == ms.ImportantMessage:
        return hou.severityType.ImportantMessage
    elif mesSev == ms.Warning:
        return hou.severityType.Warning
    elif mesSev == ms.Error:
        return hou.severityType.Error
    elif mesSev == ms.Fatal:
        return hou.severityType.Fatal

def _hfcm(fmode):
    if fmode == fm.Read:
        return hou.fileChooserMode.Read
    elif fmode == fm.Write:
        return hou.fileChooserMode.Write
    elif fmode == fm.ReadAndWrite:
        return hou.fileChooserMode.ReadAndWrite

def infoWindow(wmessage, wtitle=None, wbuttons=('Ok',), wdefault_choice=0, msev=ms.Message):
    '''Pop up an informational window with various buttons
    This function returns the index of the button pressed.'''
    return hou.ui.displayMessage(wmessage, buttons=wbuttons, default_choice=wdefault_choice, title=wtitle, severity=_hsev(msev))

def warningWindow(wmessage, wtitle='Warning!', wbuttons=('Ok', 'Cancel',), wdefault_choice=1, msev=ms.Warning):
    '''Pop up a warning window with Ok and Cancel buttons
    Returns the index of the button pressed.'''
    return hou.ui.displayMessage(wmessage, buttons=wbuttons, default_choice=wdefault_choice, title = wtitle, severity=_hsev(msev))

def listWindow(dlist, wtitle=None, wmessage=None, multi_select=False):
    '''Pop up an window with a list of options to choose from
    This function returns a tuple of indices that were selected. When cancel is 
    pressed, the return value will be 'None'. '''
    print "listWindow"
    multi = not multi_select
    return hou.ui.selectFromList(dlist, title=wtitle, message=wmessage, exclusive=multi) 

def inputWindow(wmessage, wtitle=None, initial_text=None, msev=ms.Message):
    '''Pop up a window with a text box to enter information into

Returns the string entered or 'None' when the user cancels the window.'''
    resp = hou.ui.readInput(wmessage, title=wtitle, buttons=('Ok','Cancel'), initial_contents=initial_text, severity=_hsev(msev))
    if resp[0] == 0:
        return resp[1]
    else:
        return None

def passwordWindow(password, wtitle='Enter Password', wmessage='Enter Password', wlabel='Password'):
    '''Pop up a window with a text window to enter a password into

Returns true when the password entered matches the password given as a 
parameter and false otherwise.'''
    resp = ''
    ok = 0
    first = True
    label = (wlabel + ':',)
    while ok == 0 and resp != password:
        if not first:
            infoWindow('Incorrect!\nTry Again.', wtitle='Error', msev=ms.Error)
        ok, resp = hou.ui.readMultiInput(message=wmessage, input_labels=label, password_input_indices=(0,), buttons=('OK', 'Cancel'), title=wtitle)
        resp = resp[0]
        first = False
    return ok == 0

def fileChooser(start_dir=None, wtitle=None, mode=fm.ReadAndWrite, extensions=None, image=False):
    '''Pop up a file chooser window

Extensions is a comma separated string of extensions prepended with * (e.g. "*.png, *.exr").'''
    return hou.ui.selectFile(start_directory=start_dir, title=wtitle, chooser_mode=_hfcm(mode), pattern=extensions, image_chooser=image)

shotDialog = _ui_base.shotDialog

