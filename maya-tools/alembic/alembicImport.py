from pymel.core import *
import sys, os

maya_file = sys.argv[1]
abc_file = sys.argv[2]
print maya_file
print abc_file

if os.path.exists(maya_file):
    openFile(maya_file, force=True)
else:
    newFile(force=True)
    renameFile(maya_file, force=True)
    saveFile(force=True)

loadPlugin("AbcImport")
command = 'AbcImport -mode import "%s"'%(abc_file)
print command
Mel.eval(command)
saveFile(force=True)
os._exit(0)