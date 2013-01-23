#!/usr/bin/env python
"""
@author: Brian Kingery
Install script for Maya files.
This script should be called directly using Maya's mayapy at $MAYA_LOCATION/bin/mayapy
"""

import sys, os
import maya.cmds as mc
import maya.standalone

maya.standalone.initialize(name='python')

def importObjectsFromReference(srcFilePath, newInstFilePath):
    """
    Imports all references in srcFilePath and saves the result to newInstFilePath
    """
    mc.file(srcFilePath, force=True, open=True)
    
    #TODO which one do we want?
    #references = mc.ls(type='reference', long=True)
    references = mc.ls(references=True)
    for ref in references:
        filename = mc.referenceQuery(ref, filename=True)
        print filename
        #print mc.referenceQuery(ref, isLoaded=True)
        #refNode = mc.referenceQuery(ref, referenceNode=True)
        #print refNode
        #print mc.file(loadReference=mc.referenceQuery(ref, referenceNode=True))
        mc.file(filename, importReference=True)
    print "****************** Finished Importing References ********************"
    mc.file(rename=newInstFilePath)
    mc.file(save=True, force=True)

# >>>>>>>>>>>>>>>>>>>>>>>> STARTS HERE <<<<<<<<<<<<<<<<<<<<<<<<<<<<
if len(sys.argv) == 3 and os.path.exists(str(sys.argv[1])) and not os.path.exists(str(sys.argv[2])):
    importObjectsFromReference(str(sys.argv[1]), str(sys.argv[2]))
else:
    raise Exception("Can not install file: File does not exist.")
