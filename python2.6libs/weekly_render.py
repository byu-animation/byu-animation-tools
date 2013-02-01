import shutil
import os

LIGHTING_DIR = os.environ['LIGHTING_DIR']

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
        if not line.startswith('#'):
            shotInfo = parseShotLine(line)
            if shotInfo:
                shotList.append(shotInfo)
        #TODO

# Houdini UI #
# Return the path to the .txt file to be read.
def getInputFile():
    inputFile = ''
    while(not _isValidTextFile(inputFile)):
        inputFile = hou.ui.selectFile(start_directory = None,\
                                      title = "Select Definition (.txt) File",\
                                      collapse_sequences = False,\
                                      pattern = ('*.txt'),\
                                      multiple_select = False,\
                                      chooser_mode = hou.fileChooserMode.Read)
        if inputFile == '':
            raise Exception("No input file chosen. Exiting...")
    return hou.expandString(inputFile)
    
def getOutputDir():
    hou.ui.displayMessage("Please Select a Render Output Directory.")
    outputDir= ''
    outputDir = hou.ui.selectFile(start_directory = None,\
                                      title = "Select Output Directory for Renders",\
                                      collapse_sequences = False,\
                                      file_type = hou.fileType.Directory,\
                                      multiple_select = False,\
                                      chooser_mode = hou.fileChooserMode.Read)
        if outputDir == '':
            raise Exception("No output directory chosen. Exiting...") #TODO use tmp dir instead
        return hou.expandString(outputDir)
                                      
## Main ##
inputFile = getInputFile()
outputDir = getOutputDir()

