import os
import _ui_base

# Make _ui default to _ui_base
_ui = _ui_base

try:
    # Check to see what environment we are in and reassign _ui accordingly
    if os.environ['CURRENT_PROG'] == 'Houdini':
        import _ui_houdini
        _ui = _ui_houdini
    elif os.environ['CURRENT_PROG'] == 'Maya':
        import _ui_maya
        _ui = _ui_maya
except KeyError as ke:
    # No variable by this name exists
    pass
except:
    # Something else really bad happened
    pass

# Make local functions aliases of the functions we ought to use
infoWindow = _ui.infoWindow
warningWindow = _ui.warningWindow
listWindow = _ui.listWindow
inputWindow = _ui.inputWindow
passwordWindow = _ui.passwordWindow
fileChooser = _ui.fileChooser
shotDialog = _ui.shotDialog

