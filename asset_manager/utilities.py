"""
This module contains functionality to manage the animation project.
@author: Morgan Strong, Brian Kingery
"""

import os, time, shutil, glob
from ConfigParser import ConfigParser
from subprocess import call

def getProjectName():
	return os.environ['PROJECT_NAME']
def getProductionDir():
	return os.environ['PRODUCTION_DIR']
def getUsername():
	return os.environ['USER']
def getUserCheckoutDir():
	return os.path.join(os.environ['USER_DIR'], 'checkout')

def getHoudiniPython():
	"""precondition: HFS environment variable is set correctly"""
	return "/opt/hfs.current/python/bin/python"
	#return os.path.join(os.environ['HFS'], "python", "bin", "python")

def getMayapy():
	"""precondition: MAYA_LOCATION environment variable is set correctly"""
	return os.path.join(os.environ['MAYA_LOCATION'], "bin", "mayapy")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Folder Management

def _writeConfigFile(filePath, configParser):
       """
       Will update the config file specified by filePath with the contents of configParser
       @precondition: filePath is a valid path
       @precondition: confgParser is an instance of ConfigParser()
       """
       configFile = open(filePath, 'wb')
       configParser.write(configFile)


def createNodeInfoFile(dirPath):
	"""
	Creates the .nodeInfo file in the directory specified by dirPath.
	The Node:Type must be set by concrete nodes
	@precondition: dirPath is a valid directory
	@postcondition: All sections/tags are created and set except "Type".
		"Type" must be set by concrete nodes.
	"""
	username = getUsername()
	timestamp = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
	
	nodeInfo = ConfigParser()
	nodeInfo.add_section('Node')
	nodeInfo.set('Node', 'Type', '')
	
	nodeInfo.add_section('Versioning')
	nodeInfo.set('Versioning', 'LatestVersion', '0')
	nodeInfo.set('Versioning', 'Locked', 'False')
	nodeInfo.set('Versioning', 'LastCheckoutTime', timestamp)
	nodeInfo.set('Versioning', 'LastCheckoutUser', username)
	nodeInfo.set('Versioning', 'LastCheckinTime', timestamp)
	nodeInfo.set('Versioning', 'LastCheckinUser', username)
	
	_writeConfigFile(os.path.join(dirPath, ".nodeInfo"), nodeInfo)
	
def addVersionedFolder(parent, name):
	new_dir = os.path.join(parent, name)
	os.makedirs(os.path.join(new_dir, "src", "v0"))
	os.makedirs(os.path.join(new_dir, "stable"))
	os.makedirs(os.path.join(new_dir, 'stable', 'backups'))

	#os.symlink(os.path.join(new_dir, 'stable', getNullReference()), os.path.join(new_dir, 'stable','stable'))
	#TODO change for stable selection
	#os.symlink(getNullReference(), os.path.join(new_dir, 'stable','stable'))
	createNodeInfoFile(new_dir)
	return new_dir

def addProjectFolder(parent, name):
	newPath = os.path.join(parent, name)
	os.makedirs(newPath)
	return newPath

def createNewAssetFolders(parent, name):
	new_dir = os.path.join(parent, name)
	addProjectFolder(parent, name)
	addVersionedFolder(new_dir, 'model')
	addVersionedFolder(new_dir, 'rig')
	os.makedirs(os.path.join(new_dir, "geo"))
	os.makedirs(os.path.join(new_dir, "images"))
	return new_dir

def createNewShotFolders(parent, name):
	if parent != os.environ['SHOTS_DIR']:
		raise Exception("Shot folders must be created in "+os.environ['SHOTS_DIR'])
	
	new_dir = os.path.join(parent, name)
	print 'creating :'+new_dir
	addProjectFolder(parent, name)
	addVersionedFolder(new_dir, 'animation')
	addVersionedFolder(new_dir, 'lighting')
	addVersionedFolder(new_dir, 'compositing')
	addProjectFolder(new_dir, 'animation_cache')
	addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'abc')
	addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'geo_sequences')

def isEmptyFolder(dirPath):
	return not bool(glob.glob(os.path.join(dirPath, '*')))

def canRemove(dirPath):
	return canRename(dirPath)

def removeFolder(dirPath):
	if not canRemove(dirPath):
		raise Exception ("Cannot remove directory: " + str(dirPath))
	shutil.rmtree(dirPath)

def canRename(assetDirPath, newName='__null_asset_path'):
	head, tail = os.path.split(assetDirPath)
	dest = os.path.join(head, newName)
	modelDir = os.path.join(assetDirPath, 'model')
	rigDir = os.path.join(assetDirPath, 'rig')
	if not isCheckedOut(modelDir) and not isCheckedOut(rigDir) and not os.path.exists(dest):
		return True
	return False

def renameFolder(oldDir, newName):
	head, tail = os.path.split(oldDir)
	dest = os.path.join(head, newName)
	if os.path.exists(dest):
		raise Exception ("Folder already exists")
	os.renames(oldDir, dest)

def renameVersionedFiles(vDirPath, oldname, newName):
	src = glob.glob(os.path.join(vDirPath, 'src', '*', '*.mb'))
	stable = glob.glob(os.path.join(vDirPath, 'stable', '*', '*.mb'))
	stable = stable+glob.glob(os.path.join(vDirPath, 'stable', '*.mb'))
	for s in src+stable:
		head, tail = os.path.split(s)
		dest = os.path.join(head, newName+tail.split(oldname)[1])
		os.renames(s, dest)

def renameAsset(oldDirPath, newName):
	if not canRename(oldDirPath, newName):
		raise Exception ("Can not rename")
	head, tail = os.path.split(oldDirPath)
	dest = os.path.join(head, newName)
	modelDir = os.path.join(oldDirPath, 'model')
	rigDir = os.path.join(oldDirPath, 'rig')
	renameVersionedFiles(modelDir, tail, newName)
	renameVersionedFiles(rigDir, tail, newName)
	os.renames(oldDirPath, dest)

def hasInstalledChild(dirPath):
	if isVersionedFolder(dirPath) and isInstalled(dirPath) or isCheckedOut(dirPath):
		return True
	
	found = False
	if os.path.isdir(dirPath):
		children = glob.glob(os.path.join(dirPath, '*'))
		for c in children:
			found = hasInstalledChild(c)
			if found:
				break
	return found


def isVersionedFolder(dirPath):
	if os.path.exists(os.path.join(dirPath, ".nodeInfo")):
		return True
	else:
		return False

def isCheckedOutCopyFolder(dirPath):
	if os.path.exists(os.path.join(dirPath, ".checkoutInfo")):
		return True
	else:
		return False

def isInstalled(dirPath):
	return bool(glob.glob(os.path.join(dirPath, 'stable', '*stable*')))

def getVersionedFolderInfo(dirPath):
	if not isVersionedFolder(dirPath):
		raise Exception("Not a versioned folder")
	
	nodeInfo = []
	cp = ConfigParser()
	cp.read(os.path.join(dirPath, ".nodeInfo"))
	if cp.getboolean("Versioning", "locked"):
		nodeInfo.append(cp.get("Versioning", "lastcheckoutuser"))
	else:
		nodeInfo.append("")
	nodeInfo.append(cp.get("Versioning", "lastcheckinuser"))
	nodeInfo.append(cp.get("Versioning", "lastcheckintime"))
	if isInstalled(dirPath):
		nodeInfo.append("Yes")
		nodeInfo.append(glob.glob(os.path.join(dirPath, 'stable', '*stable*'))[0])
	else:
		nodeInfo.append("No")
		nodeInfo.append("")
	return nodeInfo

def setVersion(dirPath, version):	
    """
    Sets the 'latest version' as the specified version and deletes later versions
    @precondition: dirPath is a valid path
    @precondition: version is an existing version
    @precondition: the folder has been checked out by the user

    @postcondition: the folder will be checked in and unlocked
    """

    chkoutInfo = ConfigParser()
    chkoutInfo.read(os.path.join(dirPath, ".checkoutInfo"))
    chkInDest = chkoutInfo.get("Checkout", "checkedoutfrom")
    lockedbyme = chkoutInfo.getboolean("Checkout", "lockedbyme")
    
    nodeInfo = ConfigParser()
    nodeInfo.read(os.path.join(chkInDest, ".nodeInfo"))
    newVersionPath = os.path.join(chkInDest, "src", "v"+str(version))

    if lockedbyme == False:
        print "Cannot overwrite locked folder."
        raise Exception("Can not overwrite locked folder.")
        
    # Set version
    timestamp = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
    nodeInfo.set("Versioning", "lastcheckintime", timestamp)
    nodeInfo.set("Versioning", "lastcheckinuser", getUsername())
    nodeInfo.set("Versioning", "latestversion", str(version))
    nodeInfo.set("Versioning", "locked", "False")
    _writeConfigFile(os.path.join(chkInDest, ".nodeInfo"), nodeInfo)
    
    # Clean up
    purgeAfter(os.path.join(chkInDest, "src"), version)
    shutil.rmtree(dirPath)
    #os.remove(os.path.join(newVersionPath, ".checkoutInfo"))

#################################################################################
# Checkout
#################################################################################
def _createCheckoutInfoFile(dirPath, coPath, version, timestamp, lock):
	"""
	Creates a .checkoutInfo file in the directory specified by dirPath
	@precondition: dirPath is a valid path
	@postcondition: dirPath/.checkoutInfo contains complete [Checkout] section
	"""
	chkoutInfo = ConfigParser()
	chkoutInfo.add_section("Checkout")
	chkoutInfo.set("Checkout", "checkedoutfrom", coPath)
	chkoutInfo.set("Checkout", "checkouttime", timestamp)
	chkoutInfo.set("Checkout", "version", version)
	chkoutInfo.set("Checkout", "lockedbyme", str(lock))
	
	_writeConfigFile(os.path.join(dirPath, ".checkoutInfo"), chkoutInfo)

def isCheckedOut(dirPath):
	nodeInfo = os.path.join(dirPath, ".nodeInfo")
	if not os.path.exists(nodeInfo):
		return False
	cp = ConfigParser()
	cp.read(nodeInfo)
	return cp.getboolean("Versioning", "locked")

def checkedOutByMe(dirPath):
	nodeInfo = os.path.join(dirPath, ".nodeInfo")
	if not os.path.exists(nodeInfo):
		return False
	cp = ConfigParser()
	cp.read(nodeInfo)
	return cp.get("Versioning", "lastcheckoutuser") == getUsername()

def getFilesCheckoutTime(filePath):
	checkoutInfo = os.path.join(filePath, ".checkoutInfo")
	#print checkoutInfo
	if not os.path.exists(checkoutInfo):
		raise Exception("No checkout info available")
	cp = ConfigParser()
	cp.read(checkoutInfo)
	return cp.get("Checkout", "checkouttime")

def canCheckout(coPath):
	result = True
	if not os.path.exists(os.path.join(coPath, ".nodeInfo")):
		result = False
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(coPath, ".nodeInfo"))
	if nodeInfo.get("Versioning", "locked") == "True":
		result = False
	return result

def getCheckoutDest(coPath):
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(coPath, ".nodeInfo"))
	version = nodeInfo.get("Versioning", "latestversion")
	return os.path.join(getUserCheckoutDir(), os.path.basename(os.path.dirname(coPath))+"_"+os.path.basename(coPath)+"_"+version)

def checkout(coPath, lock):
	"""
	Copies the 'latest version' from the src folder into the local directory
	@precondition: coPath is a path to a versioned folder
	@precondition: lock is a boolean value
	
	@postcondition: A copy of the 'latest version' will be placed in the local directory
		with the name of the versioned folder
	@postdondition: If lock == True coPath will be locked until it is released by checkin
	"""
	#if not os.path.exists(os.path.join(coPath, ".nodeInfo")):
	if not isVersionedFolder(coPath):
		raise Exception("Not a versioned folder.")
	
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(coPath, ".nodeInfo"))
	if nodeInfo.get("Versioning", "locked") == "False":
		version = nodeInfo.get("Versioning", "latestversion")
		toCopy = os.path.join(coPath, "src", "v"+version)
		dest = getCheckoutDest(coPath)
		
		if(os.path.exists(toCopy)):
			try:
				shutil.copytree(toCopy, dest) # Make the copy
			except Exception:
				print "asset_mgr_utils, checkout: Could not copy files."
				raise Exception("Could not copy files.")
			timestamp = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
			nodeInfo.set("Versioning", "lastcheckoutuser", getUsername())
			nodeInfo.set("Versioning", "lastcheckouttime", timestamp)
			nodeInfo.set("Versioning", "locked", str(lock))
			
			_writeConfigFile(os.path.join(coPath, ".nodeInfo"), nodeInfo)
			_createCheckoutInfoFile(dest, coPath, version, timestamp, lock)
		else:
			raise Exception("Version doesn't exist "+toCopy)
	else:
		whoLocked = nodeInfo.get("Versioning", "lastcheckoutuser")
		whenLocked = nodeInfo.get("Versioning", "lastcheckouttime")
		raise Exception("Can not checkout. Folder is locked by "+whoLocked+" at "+whenLocked)
	return dest

################################################################################
# Checkin
################################################################################
def canCheckin(toCheckin):
	"""
	@returns: True if destination is not locked by another user
		AND this checkin will not overwrite a newer version
	"""
	chkoutInfo = ConfigParser()
	chkoutInfo.read(os.path.join(toCheckin, ".checkoutInfo"))
	chkInDest = chkoutInfo.get("Checkout", "checkedoutfrom")
	version = chkoutInfo.getint("Checkout", "version")
	lockedbyme = chkoutInfo.getboolean("Checkout", "lockedbyme")
	
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(chkInDest, ".nodeInfo"))
	locked = nodeInfo.getboolean("Versioning", "locked")
	latestVersion = nodeInfo.getint("Versioning", "latestversion")
	
	result = True
	if lockedbyme == False:
		if locked == True:
			result = False
		if version < latestVersion:
			result = False
	
	return result

def purge(dirPath, upto):
	"""
	purges all folders in dirPath with a version less than upto
	"""
	files = glob.glob(os.path.join(dirPath, '*'))
	for f in files:
		if int(os.path.basename(f).split('v')[1]) < upto:
			shutil.rmtree(f)

def purgeAfter(dirPath, after):
    """
    purges all folders in dirPath with a version higher than after
    """
    files = glob.glob(os.path.join(dirPath, '*'))
    for f in files:
        if int(os.path.basename(f).split('v')[1]) > after:
            shutil.rmtree(f)

def discard(toDiscard):
	"""
	Discards a local checked out folder without creating a new version.
	"""
	chkoutInfo = ConfigParser()
	chkoutInfo.read(os.path.join(toDiscard, ".checkoutInfo"))
	chkInDest = chkoutInfo.get("Checkout", "checkedoutfrom")

	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(chkInDest, ".nodeInfo"))

	nodeInfo.set("Versioning", "locked", "False")
	_writeConfigFile(os.path.join(chkInDest, ".nodeInfo"), nodeInfo)

	shutil.rmtree(toDiscard)

def getCheckinDest(toCheckin):
	chkoutInfo = ConfigParser()
	chkoutInfo.read(os.path.join(toCheckin, ".checkoutInfo"))
	return chkoutInfo.get("Checkout", "checkedoutfrom")

def checkin(toCheckin):
	"""
	Checks a folder back in as the newest version
	@precondition: toCheckin is a valid path
	@precondition: canCheckin() == True OR all conflicts have been resolved
	"""
	chkoutInfo = ConfigParser()
	chkoutInfo.read(os.path.join(toCheckin, ".checkoutInfo"))
	chkInDest = chkoutInfo.get("Checkout", "checkedoutfrom")
	lockedbyme = chkoutInfo.getboolean("Checkout", "lockedbyme")
	
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(chkInDest, ".nodeInfo"))
	locked = nodeInfo.getboolean("Versioning", "locked")
	newVersion = nodeInfo.getint("Versioning", "latestversion") + 1
	newVersionPath = os.path.join(chkInDest, "src", "v"+str(newVersion))
	
	if not canCheckin(toCheckin):
		print "Can not overwrite locked folder."
		raise Exception("Can not overwrite locked folder.")
	
	# Checkin
	shutil.copytree(toCheckin, newVersionPath)
	
	timestamp = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
	nodeInfo.set("Versioning", "lastcheckintime", timestamp)
	nodeInfo.set("Versioning", "lastcheckinuser", getUsername())
	nodeInfo.set("Versioning", "latestversion", str(newVersion))
	nodeInfo.set("Versioning", "locked", "False")
	_writeConfigFile(os.path.join(chkInDest, ".nodeInfo"), nodeInfo)
	
	#print glob.glob(os.path.join(chkInDest, "src", "*"))
	purge(os.path.join(chkInDest, "src"), newVersion - 5)

	# Clean up
	shutil.rmtree(toCheckin)
	os.remove(os.path.join(newVersionPath, ".checkoutInfo"))

	return chkInDest

################################################################################
# Install
################################################################################
def getAvailableInstallFiles(vDirPath):
	"""
	@returns: a list of all file paths in this directory
	"""
	#if not os.path.exists(os.path.join(vDirPath, ".nodeInfo")):
	if not isVersionedFolder(vDirPath):
		raise Exception("Not a versioned folder.")
	
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(vDirPath, ".nodeInfo"))
	version = nodeInfo.get("Versioning", "latestversion")
	latest = os.path.join(vDirPath, "src", "v"+version)
	
	files = glob.glob(os.path.join(latest,'*'))
	print files
	return files

def _isHoudiniFile(filename):
	"""
	@returns: True if filename has the extension '.hip' or '.hipnc' or '.picnc
	"""
	houdiniExts = ['.hip', '.hipnc', '.picnc']
	name, ext = os.path.splitext(filename)
	return ext in houdiniExts
	
def _isMayaFile(filename):
	"""
	@returns: True if filename has the extension '.ma' or '.mb'
	"""
	mayaExts = ['.ma', '.mb']
	name, ext = os.path.splitext(filename)
	return ext in mayaExts
	
def install(vDirPath, srcFilePath):
	"""
	Installs a file for production use and flattens maya/houdini dependencies.
	Use getAvailableInstallFiles(dirPath) to get a list of files.
	@precondition: vDirPath and srcFilePath are valid paths
	@postcondition: if setStable == True then stable symlink will point to filename
	"""
	print 'utilities, install'
	print vDirPath
	print srcFilePath
	stableDir = os.path.join(vDirPath, "stable")
	backupsDir = os.path.join(stableDir, 'backups')
	numFiles = len(glob.glob(os.path.join(backupsDir, '*')))
	
	srcName, srcExt = os.path.splitext(os.path.basename(srcFilePath))
	stableName = os.path.basename(os.path.dirname(vDirPath))+"_"+os.path.basename(vDirPath)+"_stable"
	
	# Backup old stable file
	if os.path.exists(os.path.join(stableDir, stableName+srcExt)):
		shutil.move(os.path.join(stableDir, stableName+srcExt), os.path.join(backupsDir, stableName+'_'+str(numFiles)+srcExt))
	
	newInstFilePath = os.path.join(stableDir, stableName+srcExt)
	print newInstFilePath
	
	#if _isHoudiniFile(newInstFilePath):
	#	call([getHoudiniPython(), "installHoudiniFile.py", srcFilePath, newInstFilePath])
	#elif _isMayaFile(newInstFilePath):
	#	call([getMayapy(), "installMayaFile.py", srcFilePath, newInstFilePath])
	#else:
	#	#Just copy the file
	#	print 'copying file...'
	#	
	shutil.copy(srcFilePath, newInstFilePath)

def runAlembicConverter(vDirPath, srcFilePath):
	filename, ext = os.path.splitext(os.path.basename(srcFilePath))
	dest_path = os.path.join(os.path.dirname(vDirPath), 'animation_cache', 'abc', filename+'.abc')
	converter = os.path.join(os.environ['MAYA_TOOLS_DIR'], 'alembic', 'alembicconvert.py')
	if os.path.exists(dest_path):
		os.remove(dest_path)
	os.system(getMayapy()+' '+converter+' '+srcFilePath+' '+dest_path)
