import shutil
import string
import os

JOB_DIR = os.environ['JOB']
LIGHTING_DIR = os.environ['LIGHTING_DIR']
DAILIES_DIR = os.environ['DAILIES_DIR']

TMPDIR = os.path.join(DAILIES_DIR, 'tmp')
RENDERDIR = os.path.join(DAILIES_DIR, 'renders')

LIGHTING_PREFIX = "lighting_"
HOUDINI_EXTENSION = ".hipnc"
FRAME_SUFFIX = "_$F3"
FILE_TYPE = ".tif"

HQ_SERVER = "hqueue:5000"

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
    fileName = LIGHTING_PREFIX + string.lower(shotname) + HOUDINI_EXTENSION
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

def setUpMantraNode(shotName, frameRange):
    man = hou.node("/out").createNode("ifd")
    outputDir = RENDERDIR.replace(JOB_DIR, "$JOB")
    outputLoc = os.path.join(outputDir, getOutFileName(shotName))

    man.parm("vm_picture").set(outputLoc)
    man.parm("trange").set("normal")

    man.parm("f1").set(frameRange[0])
    man.parm("f2").set(frameRange[1])
    man.parm("f3").set(1)
    
    man.parm("vm_renderengine").set("pbrraytrace")
    # TODO which camera?!
    # TODO other paramaters
    return man

def setUpHQueueNode(man):
    hq = hou.node("/out").createNode("hq_render")
    hq.parm("hq_driver").set(man.path())
    hq.parm("hq_server").set(HQ_SERVER)
    hq.parm("hq_autosave").set(1)
    #TODO other parameters?
    return hq

def weeklyRender(shotList):
    '''
    TODO:
    for each shot
    a. copy Lighting file (most recent one in the Lighting folder?) into my tmp dir
    b. open it up (run in houdini?)
    c. add a prescribed mantra node (settings all happy)
    \   c.i. create shot folder in output dir?
    d. set mantra frame range to that described in the file
    e. create hqueue attached to that mantra
    f. shoot off hqueue render
    g. wait for completion?
    h. delete temp file in tmp dir.
    i. repeat
    j. hperf (statistics)
    '''
    for shot in shotList:
        shotName = shot[0]
        frameRange = (shot[1], shot[2])
        copyFileToTmp(shotName, os.path.join(LIGHTING_DIR, shotName))
        filePath = os.path.join(TMPDIR, getHouFileName(shotName))
        try:
            hou.hipFile.load(filePath, suppress_save_prompt = True)
        except hou.OperationFailed:
            hou.ui.displayMessage("Failed to open " + filePath + ". Moving on...")
            continue
        mantra = setUpMantraNode(shotName, frameRange)
        hqueue = setUpHQueueNode(mantra)
        #hqueue.render() #TODO test
        #cleanup
        os.remove(os.path.join(TMPDIR, getHouFileName(shotName)))

## Hou Main ##
inputFile = getInputFile()
outputDir = getOutputDir(RENDERDIR)
shotList = parseDefinitionFile(inputFile)
try:
    weeklyRender(shotList)
except SyntaxError:
    print ("A syntax error occurred.")
