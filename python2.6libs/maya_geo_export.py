# Created by a lot of people
# Compiled by Josh Davis 2013

import maya.cmds as mc
import os
import subprocess as sp
import sys
import shutil

from ui_tools import ui, messageSeverity, fileMode

def objExport(selected, path):
	'''
		Creates .obj files from a selection of objects
	
		@param: selected - a list of strings representing the geometry
		@param: path - a string to the path of the directory for .obj files to go
	
		@return: a list of strings that contain the full paths to all of the .obj
				files that were created
	
		@post: directory for 'path' is created if it wasn't already
	'''
        # load the objExport plugin	
        mc.loadPlugin("objExport")

	# Create directory if it doesn't exist
	if not os.path.exists(path):
		os.makedirs(path)
	
	size = len(selected)
	
	mc.sysFile(path, makeDir=True)
	optionsStr = "groups=0;ptgroups=0;materials=0;smoothing=0;normals=0;uvs=1"
	exportType = "OBJexport"
	
	objfiles = []
	
	for geo in selected:
		mc.select(geo, r=True)
		geoName = geo + ".obj"
		geoName = geoName.replace("Shape", "")
		geoName = geoName.replace(":", "_")
		geoName = geoName.replace("|", "_")
		filename = os.path.join(path, geoName)
		print("Exporting \'" + filename + "\'...")
		mc.file(filename, force=True, options=optionsStr, type=exportType, preserveReferences=True, exportSelected=True)
		print("\tCOMPLETED")
		objfiles.append(filename)
		
	return objfiles
	
	
def bjsonExport(objfiles, path):    
	'''
		Creates .bjson files from existing .obj files
	
		@param: objfiles - a list of strings representing full paths to .obj files
		@param: path - a string to the path of the directory for .bjson files to go
	
		@return: a list of strings that contain the full paths to all of the .bjson
				files that were created
			
		@post: directory for 'path' is created if it wasn't already
	'''
	
	# Create directory if it doesn't exist
	if not os.path.exists(path):
		os.makedirs(path)
	
	bjsonfiles = []

	for objfile in objfiles:
		filebase = os.path.splitext(os.path.basename(objfile))[0]    
		filename = filebase + '.bjson'
		outfile = os.path.join(path, filename)
		cmdstr = '/opt/hfs.current/bin/gwavefront ' + objfile + ' ' + outfile
		print("Converting '" + objfile + "' to '" + outfile + "'...")
		sp.Popen(cmdstr, shell=True)
		os.wait()
		print("\nCOMPLETED")
		bjsonfiles.append(outfile)
	
	return bjsonfiles


def checkFiles(files):
	'''
		Checks the list of output files against which files were actually created
	
		@param: files - a list of strings representing full paths
			
		@return: a list of paths to files that do not exist
	'''

	missingFiles = []
	
	for filename in files:
		if not os.path.exists(filename):
			missingFiles.append(filename)
	
	if not len(missingFiles) == 0:
		errorMessage = ""
		for f in missingFiles:
			errorMessage += "MISSING FILE: " + f + "\n"
		print(errorMessage)
		errorMessage = str(len(missingFiles)) + " Files Missing:\n\n" + errorMessage
		#mc.confirmDialog(title="Error exporting files", message=errorMessage)
		ui.infoWindow(errorMessage, wtitle="Error exporting files", msev=messageSeverity.Error)
	
	return missingFiles


def decodeFileName():
        '''
                Decodes the base name of the folder to get the asset name, assetType, and asset directory.

                @return: Array = [assetName:- the asset name, assetType:- the asset Type, version:- the asset version]
        '''
        # get the encoded folder name from the filesystem        
        encodedFolderName = os.path.basename(os.path.dirname(mc.file(q=True, sceneName=True)))

        # split the string based on underscore delimiters
        namesAry = encodedFolderName.split("_")
        
        # pop off the version and asset type information
        version   = namesAry.pop()
        assetType = namesAry.pop()

        #combine the array into a string to form the assetname
        assetName = '_'.join(namesAry)
        
        # return the assetName, assetType, and version
        return [assetName, assetType, version] 

def installGeometry(path=os.path.dirname(mc.file(q=True, sceneName=True))):
	'''
		Function to install the geometry into the PRODUCTION asset directory

		Moves the geometry into os.path.join(os.environ['ASSETS_DIR'], assetName, 'geo')

		@return: True is the files were moved successfully
		@throws: a shutil exception if the move failed
	'''
	assetName, assetType, version = decodeFileName()

	srcOBJ = os.path.join(path, 'geo/objFiles')
	srcBJSON = os.path.join(path, 'geo/bjsonFiles')
	destOBJ = os.path.join(os.environ['ASSETS_DIR'], assetName, 'geo/objFiles')
	destBJSON = os.path.join(os.environ['ASSETS_DIR'], assetName, 'geo/bjsonFiles')

	if os.path.exists(destOBJ):
		shutil.rmtree(destOBJ)
	if os.path.exists(destBJSON):
		shutil.rmtree(destBJSON)

	print 'Copying '+srcOBJ+' to '+destOBJ
	try:
		shutil.copytree(srcOBJ, destOBJ)
	except Exception as e:
		print e

	print 'Copying '+srcBJSON+' to '+destBJSON
	try:
		shutil.copytree(src=srcBJSON, dst=destBJSON)
	except Exception as e:
		print e

	print 'Removing '+os.path.join(path, 'geo')
	shutil.rmtree(os.path.join(path, 'geo'))

	return True




def generateGeometry(path=os.path.dirname(mc.file(q=True, sceneName=True))):	
	'''
		Function for generating geometry for Maya files.
	
		Creates the following output formats:
			.obj
			.bjson
	
		@return: True if all files were created successfully
				False if some files were not created
			
		@post: Missing filenames are printed out to both the Maya terminal as well
				as presented in a Maya confirm dialog.
	'''
	print 'generateGeometry start'
	if not os.path.exists (os.path.join(path, 'geo')):
		os.makedirs(os.path.join(path, 'geo'))

	# Define output paths
	OBJPATH = os.path.join(path, "geo/objFiles")
	BJSONPATH = os.path.join(path, "geo/bjsonFiles")
	
	# Make initial selection
	selection = mc.ls(geometry=True, visible=True)

	# Delete old obj and bjson folders
	if os.path.exists(OBJPATH):
		shutil.rmtree(OBJPATH)
	if os.path.exists(BJSONPATH):
		shutil.rmtree(BJSONPATH)
	
	# Export meshes to .obj files
	objs = objExport(selection, OBJPATH)
	
	# Check to see if all .obj files were created
	if not len(checkFiles(objs)) == 0:
		return False
	
	# Convert .obj files to .bjson
	bjsons = bjsonExport(objs, BJSONPATH)
	
	# Check to see if all .bjson files were created
	if not len(checkFiles(bjsons)) == 0:
		return False
		
	return True

if __name__ == "__main__":	
	# Uncomment this line if you want to read in a new destination from
	# command line. Intended to be a new destination for files to go.
	#dest = sys.argv[1]
	
	generateGeometry()
