import shutil
import os

LIGHTING_DIR = os.environ['LIGHTING_DIR']
DAILIES_DIR = os.environ['DAILIES_DIR']

# Validation Functions #
def _isValidTextFile(p):
    ext = p[-4:]
    if ext.lower() == ".txt":
        return True
    else:
        hou.ui.displayMessage("Please Select a Shot List file (.txt)")
        return False

# OS Functions #    
def copyFileToTmp(filename, srcPath):
    newfilepath = os.path.join(TMPDIR, filename)
    oldfilepath = os.path.join(srcPath, filename)
    copyfile(oldfilepath, newfilepath)

# Parsing #
def parseShotLine(line):
    if line.startswith('#')
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
    '''

## Hou Main ##
inputFile = getInputFile()
outputDir = getOutputDir(os.path.join(DAILIES_DIR, "renders"))
shotList = parseDefinitionFile(inputFile)
try:
    weeklyRender(shotList)
except SyntaxError:
    print ("A syntax error occurred.")
