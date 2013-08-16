import sys, os
import maya.cmds as mc
import maya.standalone

maya.standalone.initialize(name='python')

def unloadReference(srcFilePath, refName):
    """
    Unloads all references containing refName
    """
    mc.file(srcFilePath, force=True, open=True)
    
    #references = mc.ls(type='reference', long=True)
    references = mc.ls(references=True)
    for ref in references:
        if refName in ref:
            mc.file(unloadReference=ref)
    print "****************** Finished Unloading References ********************"
    mc.file(save=True, force=True)

# >>>>>>>>>>>>>>>>>>>>>>>> STARTS HERE <<<<<<<<<<<<<<<<<<<<<<<<<<<<
if len(sys.argv) == 3 and os.path.exists(str(sys.argv[1])):
    unloadReference(str(sys.argv[1]), str(sys.argv[2]))
else:
    print "Unloads all references containg refName\nUSAGE: unloadReference.py $PATH $refName\n\tunloadReference.py string string"