#!/usr/bin/env python
"""
@author: Brian Kingery
Install script for Houdnini files.
This script should be called directly using Houdini's python at $HFS/python/bin/python
"""

import sys, os

def enableHouModule():
    '''Set up the environment so that "import hou" works.'''
    #import sys, os

    # Importing hou will load in Houdini's libraries and initialize Houdini.
    # In turn, Houdini will load any HDK extensions written in C++.  These
    # extensions need to link against Houdini's libraries, so we need to
    # make sure that the symbols from Houdini's libraries are visible to
    # other libraries that Houdini loads.  So, we adjust Python's dlopen
    # flags before importing hou.
    HFS = "/opt/hfs.current"
    if hasattr(sys, "setdlopenflags"):
        old_dlopen_flags = sys.getdlopenflags()
        import DLFCN
        sys.setdlopenflags(old_dlopen_flags | DLFCN.RTLD_GLOBAL)

    try:
        import hou
    except ImportError:
        # Add $HFS/houdini/python2.6libs to sys.path so Python can find the
        # hou module.
        sys.path.append(HFS + "/houdini/python%d.%dlibs" % sys.version_info[:2])
        #sys.path.append(os.environ['HFS'] + "/houdini/python2.6libs")
        import hou
    finally:
        if hasattr(sys, "setdlopenflags"):
            sys.setdlopenflags(old_dlopen_flags)
  
def isUnlockedAsset(node):
    return not node.isLocked() and node.type().definition() is not None

def isUnlockedSopNode(node):
    return isinstance(node, hou.SopNode) and not node.isHardLocked()

def needsToBeLocked(node):
    types = ["File"]
    return node.type().description() in types
    
def lockFileNodes(srcFilePath, newInstFilePath):
    """
    Locks digital assets, and HardLocks SopNodes
    Then saves the file to newInstFilePath
    """
    
    hou.hipFile.load(srcFilePath)
    
    for child in hou.node("/obj").allSubChildren():
        if isUnlockedAsset(child):
            #print child.name() + ": Unlocked Asset"
            #print child.isLocked()
            child.setLocked(on)
            #child.type().definition().updateFromNode(child)
            #child.matchCurrentDefinition()
        elif isUnlockedSopNode(child) and needsToBeLocked(child):
            #print child.name()
            try:
                child.setHardLocked(True)
            except hou.PermissionError:
                #print "CAN'T LOCK SOPNODE:: " + child.name()
                #print e
                print ""
    
    hou.hipFile.save(newInstFilePath)


# >>>>>>>>>>>>>>>>>>>>>>>> STARTS HERE <<<<<<<<<<<<<<<<<<<<<<<<<<<<
enableHouModule()
import hou

if len(sys.argv) == 3 and os.path.exists(str(sys.argv[1])) and not os.path.exists(str(sys.argv[2])):
    lockFileNodes(str(sys.argv[1]), str(sys.argv[2]))
else:
    raise Exception("Can not install file: File does not exist.")
