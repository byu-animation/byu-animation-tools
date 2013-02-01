# Created by a lot of people
# Compiled by Josh Davis 2013

import maya.cmds as mc
import os
import subprocess as sp
import sys
import shutil


def objExport(selected, path):
	'''
		Creates .obj files from a selection of objects
	
		@param: selected - a list of strings representing the geometry
		@param: path - a string to the path of the directory for .obj files to go
	
		@return: a list of strings that contain the full paths to all of the .obj
				files that were created
	
		@post: directory for 'path' is created if it wasn't already
	'''
	
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
		mc.confirmDialog(title="Error exporting files", message=errorMessage)
	
	return missingFiles

def installGeometry(path=os.path.dirname(mc.file(q=True, sceneName=True))):
	'''
		Function to install the geometry into the PRODUCTION asset directory

		Moves the geometry into os.path.join(os.environ['ASSETS_DIR'], assetName, 'geo')

		@return: True is the files were moved successfully
		@throws: a shutil exception if the move failed
	'''
	assetName = os.path.basename(path).split('_')[0]

	srcOBJ = os.path.join(path, 'geo/objfiles')
	srcBJSON = os.path.join(path, 'geo/bjsonfiles')
	destOBJ = os.path.join(os.environ['ASSETS_DIR'], assetName, 'geo/objfiles')
	destBJSON = os.path.join(os.environ['ASSETS_DIR'], assetName, 'geo/bjsonfiles')

	if os.path.exists(destOBJ):
		shutil.rmtree(destOBJ)
	if os.path.exists(destBJSON):
		shutil.rmtree(destBJSON)

	shutil.copytree(src=srcOBJ, dst=destOBJ)
	shutil.copytree(src=srcBJSON, dst=destBJSON)

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
