'''
Houdini weekly render script
Author: Elizabeth Brayton
Last Modified: 28 Mar 2013
'''

import shutil
import string
import os
import hou

JOB_DIR = os.environ['JOB']
SHOT_DIR = os.environ['SHOTS_DIR']
DAILIES_DIR = os.environ['DAILIES_DIR']

TMPDIR = os.path.join(DAILIES_DIR, 'tmp')
RENDERDIR = os.path.join(DAILIES_DIR, 'renders')

LIGHTING_SUFFIX = "_lighting_stable"
LIGHTING_FOLDER_NAME = "lighting/stable"
HOUDINI_EXTENSION = ".hipnc"
FRAME_SUFFIX = "_$F3"
FILE_TYPE = ".tif"

MANTRA_NODES_PATH = "/out/owned_render_nodes1"
MANTRA_NAME = "Main"

#HQ_SERVER = "hqueue:5000"
#HQ_JOB_NAME = "${USER}_${OS}_${HIPNAME}"

# Validation Functions #
def _isValidTextFile(p):
    ext = p[-4:]
    if ext.lower() == ".txt":
        return True
    else:
        hou.ui.displayMessage("Please Select a Shot List file (.txt)")
        return False

# OS Functions #    
def copyFileToTmp(shotname, srcPath):
    newfilepath = TMPDIR
    fileName = getHouFileName(shotname)
    oldfilepath = os.path.join(srcPath, fileName)
    shutil.copy(oldfilepath, newfilepath)


# Parsing #
def parseShotLine(line):
    if line.startswith('#'):
        return False
    else:
        return line.split()

def parseDefinitionFile(filePath):
    '''
    This ignores lines preceded by #
    '''
    shotList = []
    f = open(filePath, 'r')
    for line in f:
        shotInfo = parseShotLine(line)
        if shotInfo:
            shotList.append(shotInfo)
    return shotList

def getHouFileName(shotname):
    fileName = string.lower(shotname) + LIGHTING_SUFFIX + HOUDINI_EXTENSION
    return fileName

def getOutFileName(shotName):
    fileName = string.lower(shotName) + FRAME_SUFFIX + FILE_TYPE
    return fileName

# Houdini UI #
# Return the path to the .txt file to be read.
def getInputFile():
    inputFile = ''
    while(not _isValidTextFile(inputFile)):
        inputFile = hou.ui.selectFile(start_directory = hou.expandString(DAILIES_DIR),\
                                      title = "Select Definition (.txt) File",\
                                      collapse_sequences = False,\
                                      pattern = ('*.txt'),\
                                      multiple_select = False,\
                                      chooser_mode = hou.fileChooserMode.Read)
        if inputFile == '':
            raise Exception("No input file chosen. Exiting...")
    
    return hou.expandString(inputFile)
    
def getOutputDir(output = None):
    if not output:
        hou.ui.displayMessage("Please Select a Render Output Directory.")
        outputDir= ''
        outputDir = hou.ui.selectFile(start_directory = None,\
                                          title = "Select Output Directory for Renders",\
                                          collapse_sequences = False,\
                                          file_type = hou.fileType.Directory,\
                                          multiple_select = False,\
                                          chooser_mode = hou.fileChooserMode.Read)
        if not outputDir:
            return hou.expandString(output)

        return hou.expandString(outputDir)

    else:
        return hou.expandString(output)

def getRenderContext():
    local = hou.ui.displayMessage("Render locally (Mantra) or on the farm (HQueue)?", 
                                    buttons=('Local', 'Farm'),
                                    default_choice=1, 
                                    title="Render Mode")
    return (local == 0)

def setUpMantraNode(shotName, frameRange):
    cameraPath = "/obj/owned_cameras_%s1/shot_%s" % (shotName[0], shotName[1:])

    outputDir = RENDERDIR.replace(JOB_DIR, "$JOB")
    outputLoc = os.path.join(outputDir, getOutFileName(shotName))

    renderNodes = hou.node(MANTRA_NODES_PATH)
    renderNodes.allowEditingOfContents()
    man = renderNodes.node(MANTRA_NAME)
    
    man.parm("vm_picture").set(outputLoc)
    man.parm("trange").set("normal")

    man.parm("f1").set(frameRange[0])
    man.parm("f2").set(frameRange[1])
    man.parm("f3").set(1)

    return man

def setUpHQueueNode(man):
    hq = hou.node("/out").createNode("hq_render")
    hq.parm("hq_driver").set(man.path())
    return hq

# Main #
def weeklyRender(inputFile, local):
    #cleanup tmp folder
    for root, dirs, files in os.walk(TMPDIR):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    
    #go through each shot in the list and run a render
    shotList = parseDefinitionFile(inputFile)
    for shot in shotList:
        shotName = shot[0]
        frameRange = (shot[1], shot[2])

        fileDir = os.path.join(SHOT_DIR, shotName)
        fileDir = os.path.join(fileDir, LIGHTING_FOLDER_NAME)

        copyFileToTmp(shotName, fileDir)
        filePath = os.path.join(TMPDIR, getHouFileName(shotName))
        try:
            hou.hipFile.load(filePath, suppress_save_prompt = True)
        except hou.OperationFailed:
            hou.ui.displayMessage("Failed to open " + filePath + ". Moving on...")
            continue
        
        mantra = setUpMantraNode(shotName, frameRange)
        if local:
            mantra.render()
        else:
            hqueue = setUpHQueueNode(mantra)
            hqueue.render()
    hou.ui.displayMessage("Finished rendering! Check %s for renders." % (os.path.join(DAILIES_DIR, 'renders')))