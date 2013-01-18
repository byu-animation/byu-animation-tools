import hou
import os.path as path
import glob


def projectPath():
    '''Returns the directory of the root project folder '''

    return '/$HSITE/'+os.environ['PROJECT_NAME']


def processObjPathStrings(objString):
#    objRelative = [o.strip() for o in objString.split(';')]
#    return [projectPath() + o for o in objRelative]
    return [o.strip() for o in objString.split(';')]


def getObjPaths():
    '''Open the houdini file manager and allow the user to multi-select a
    collection of .obj files.  This function then returns a list of absolute
    paths to the .objs, in terms of the $HSITE variable.
    '''

    objString = hou.ui.selectFile(start_directory=projectPath(),
            multiple_select=True)
    return processObjPathStrings(objString)


