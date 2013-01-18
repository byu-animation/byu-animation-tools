#!/usr/bin/env hython

"""
File:        abc2bjson_hou.py
Author:      Taylor Sorenson, Morgan Strong
Date:        11/26/12
Project:     BYU Senior Animation: Chasm

This module is designed to automate the process of exporting animated geometry
from the Alembic file format to a series of geometry sequences using Houdini's
Object Model to do the heavy lifting of interpreting the Alembic file. We assume
that the hou module has already been imported. The driving shelf tool code is
contained in a comment below. Tested with H12.0.581.
"""


##### START HOUDINI SHELF TOOL CODE #####
"""
import abc2bjson_hou as a2b

try:
	# Get Alembic file from user.
	inputFile = a2b.getInputFile()
	
	# Get Output Directory. User selects from list of options
	outDir = a2b.getOutputDir(getChasmShotList())
    
    # Set the Geometry Dictionary
    a2b.setGeoDict(a2b.getAddisonGeoDict())
    
	# Generate geometry sequences    
	a2b.abc2bjson(inputFile, outputDir)

except Exception as e:
	print "Exiting: " + str(e)
"""
##### END HOUDINI SHELF TOOL CODE #####



##### START CHASM SPECIFIC CODE #####
def getAddisonGeoDict():
    # Hard Coded Pieces of Addison
    eI = []
    eO = []
    mtl = ['/model01/lower_body/grp_Boot_L/eyelets_L',\
           '/model01/lower_body/grp_Boot_L/buckle_top_L',\
           '/model01/lower_body/grp_Boot_L/buckle_bottom_L',\
           '/model01/lower_body/grp_Boot_R/eyelets_R',\
           '/model01/lower_body/grp_Boot_R/buckle_top_R',\
           '/model01/lower_body/grp_Boot_R/buckle_bottom_R',\
           '/model01/upper_body/grp_Vest/zipper/polySurface14',\
           '/model01/upper_body/grp_Vest/zipperPullTrain',\
           '/model01/upper_body/grp_Vest/zipperPullLink',\
           '/model01/upper_body/grp_Vest/zipperPull',\
           '/model01/upper_body/grp_Vest/vestBuckle_L',\
           '/model01/upper_body/grp_Vest/vestBuckle_R',\
           '/model01/upper_body/grp_Vest/vestButton_L',\
           '/model01/upper_body/grp_Vest/vestButton_R',\
           '/model01/upper_body/grp_Vest/vestButton1',\
           '/model01/upper_body/grp_Vest/vestButton2',\
           '/model01/upper_body/grp_Vest/vestButton3']
    btLcs= []
    btns = []
    shrt= []
    vst = []
    pnts= []
    hd= []
    arms = []
    btM = []
    btS = []
    pcs ={'eyesInner':eI,\
          'eyesOuter':eO,\
          'metal':mtl,\
          'bootLaces':btLcs,\
          'buttons':btns,\
          'shirt':shrt,\
          'vest':vst,\
          'pants':pnts,\
          'head':hd,\
          'arms':arms,\
          'bootsMain':btM,\
          'bootSoles':btS}
    
    # Prepend the namespace to each level of the geoemtry path hard coded above.
    for key in pcs.keys():
        path_list = pcs[key]
        new_path_list = []
        for geo_path in path_list:
            new_path = ""
            for x in geo_path.split("/"):
                if not x:
                    continue
                new_path += "/" + _namespace + "_" + x
            new_path_list.append(new_path)
        pcs[key] = new_path_list
    
    return pcs

def getChasmShotList():
    A = ["A"+str(n).zfill(2) for n in range(1,12)]
    B = ["B"+str(n).zfill(2) for n in range(1,15)]
    C = ["C"+str(n).zfill(2) for n in range(1,13)]
    D = ["D"+str(n).zfill(2) for n in range(1,18)]
    E = ["E"+str(n).zfill(2) for n in range(1,6)]
    return A+B+C+D+E

# Converts shot name to a directory path for our output
def _interpretChoice(shot_num):
    path = os.path.join("$JOB/CHASM_PROJECT/sequences/",\
                        shot_num[0],\
                        str(shot_num[1:]),\
                        "Animation_" + shot_num,\
                        "addison_bjson") + os.sep
    return path

##### END CHASM SPECIFIC CODE #####



##### START MODULE DEFINITION #####
import hou
import _alembic_hom_extensions
import os

## PRIVATE ##
# Module Variables #
_namespace = "stable"
_geo_dict = {}
_frame_start = 1
_frame_end = 240
_frame_step = 1

# Validation Functions #
def _isValidAlembic(p):
    ext = p[-4:]
    if ext.lower() == ".abc":
        return True
    else:
        hou.ui.displayMessage("Please Select an Alembic (.abc) file.")
        return False

# Subprocess Functions #
# Write out the geometry sequence to the specified folder. 
def _generateOutput(iSOP, outDir, name):
    # Ensure Output Directory Exists
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    # Create a geometry ROP in the "out" context
    geoROP = hou.node("/out").createNode('geometry')

    # Set Geometry ROP Parameters
    ROPdict = {}
    ROPdict['soppath'] = iSOP.path()
    ROPdict['sopoutput'] = outDir + '/'+name+'.$F.bjson.gz'
    ROPdict['savebackground']= True
    ROPdict['trange'] = 1 # Render Frame Range
    ROPdict['f1'] = _frame_start
    ROPdict['f2'] = _frame_end
    ROPdict['f3'] = _frame_step
    geoROP.setParms(ROPdict)

    # Render ROP with our frame range
    geoROP.render(frame_range = (_frame_start, _frame_end))
    geoROP.destroy()

## PUBLIC FUNCTIONS##
# Module Options #
def setAlembicNamespace(n):
    global _namespace
    _namespace = n
def setGeoDict(d):
    # Define the Geometry Dictionary where key-value pairs are equivalent to:
    # bjson_output -> [abc_group_path*]
    # (str)           -> [(str)*]
    # Examples: Car exported as single mesh: {"Car":["/car_model"]}
    #           Car exported in pieces:      {"Car_Body":["/car_model/body],\
    #                                         "Car_Tires":["/car_model/tire1",\
    #                                                      "/car_model/tire2",\
    #                                                      "/car_model/tire3",\
    #                                                      "/car_model/tire4"]}
    global _geo_dict
    _geo_dict = d
def setFrameRange(s,e,p=1):
    global _frame_start
    global _frame_end
    global _frame_step
    _frame_start = s
    _frame_end = e
    _frame_step = p
    
# Houdini UI #
# Return the path to the .abc file to be read.
def getInputFile():
    inputFile = ''
    while(not _isValidAlembic(inputFile)):
        inputFile = hou.ui.selectFile(start_directory = None,\
                                      title = "Select Alembic (.abc) File",\
                                      collapse_sequences = False,\
                                      pattern = ('*.abc'),\
                                      multiple_select = False,\
                                      chooser_mode = hou.fileChooserMode.Read)
        if inputFile == '':
            raise Exception("No input file chosen. Exiting...")
    return hou.expandString(inputFile)

# Return the path to the export directory. Allows either a list of choices to
# be displayed or a file select dialog.
def getOutputDir(choices = None):
    if choices:
        c = hou.ui.selectFromList(choices,\
                                       exclusive = True,\
                                       title = 'Choose Directory',\
                                       num_visible_rows = len(choices))
        if not c:
            raise Exception("No Output Folder Selected. Exiting...")
        return hou.expandString(_interpretChoice(choices[c[0]]))
    else:
        outDir = ""
        while(not os.path.isdir(hou.expandString(outDir))):
            outDir = hou.ui.selectFile(start_directory = None,\
                                       title = "Select Output Folder",\
                                       collapse_sequences = False,\
                                       pattern = ('*'),\
                                       multiple_select = False,\
                                       chooser_mode = hou.fileChooserMode.Read)
            if outDir == '':
                return outDir
        return hou.expandString(outDir)


## Main Function ##
def abc2bjson(infile, outdir = '$TEMP/'):
    
    # Create a temporary Geometry Node
    temp_geo = hou.node("/obj").createNode('geo')
    
    # Generate .bjson.gz sequences in folders that correspond to the keys of the
    # geo_dict.
    for key in _geo_dict.keys():
        # Skip key if no object paths listed.
        if not _geo_dict[key]:
            continue
        
        # Tell us what key we're working on
        print key + ": " + " ".join(_geo_dict[key])
        
        # Clean out temp_geo Node
        for n in temp_geo.children():
        	n.destroy()
    	
    	# Create a merge node to merge all abcSOPs
    	temp_merge = temp_geo.createNode("merge")
    	
    	# Create an Alembic for each object path and connect to temp_merge
    	for p in _geo_dict[key]:
    	    abcSOP = temp_geo.createNode("alembic")
            abcSOP.setParms({'fileName': infile, 'objectPath': p})
            temp_merge.setNextInput(abcSOP)
        
        # Generate Output to a separate directory for this geometry sequence.
        seqDir = os.path.join(outdir,key) + os.sep
        _generateOutput(temp_merge, hou.expandString(seqDir), key)
    
    # Clean Up
    temp_geo.destroy()

##### END MODULE DEFINITION #####
