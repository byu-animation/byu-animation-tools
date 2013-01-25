# Digital Asset management
# Provides New, Add, Checkin, Checkout, Revert, and other functionality for .otl files
# Author: Brian Kingery

import sqlite3 as lite
import os, glob
import hou

import utilities as amu #asset manager utilites

JOB=os.environ['JOB']
USERNAME=os.environ['USER']
OTLDIR=os.environ['OTLS_DIR']
USERDIR=os.path.join(os.environ['USER_DIR'], 'otls')

database=os.path.join(OTLDIR, '.otl.db')
otlTableDef="otl_table(id INTEGER PRIMARY KEY, filename TEXT, locked INT, lockedby TEXT, UNIQUE(filename))"
insert_ignore_sql="INSERT OR IGNORE INTO otl_table (filename, locked, lockedby) VALUES (?, ?, ?)"

def createUsrDir():
	if not os.path.exists(USERDIR):
		os.makedirs(USERDIR)

def updateDB():
	"""Update the database with what is in OTLDIR"""
	con = lite.connect(database)
	with con:
		cur = con.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS "+otlTableDef+";")
		files = glob.glob(os.path.join(OTLDIR, '*.otl'))
		# Add any new files to the Database
		for file in files:
			cur.execute(insert_ignore_sql, (os.path.basename(file), 0, ""))
		con.commit()
		# Delete any files that are no longer with us
		cur.execute("SELECT filename FROM otl_table")
		rows = cur.fetchall()
		toDelete = []
		for row in rows:
			toDelete.append(row[0].encode('utf-8'))
		for file in files:
			f = os.path.basename(file)
			if f in toDelete:
				toDelete.remove(f)
		for d in toDelete:
			cur.execute("DELETE FROM otl_table WHERE filename='"+d+"'")
		con.commit()
	con.close()

def getSelectedNode():
	"""Returns the current node if EXACTLY ONE is selected
		Otherwise returns None"""
	node = None
	nodes = hou.selectedNodes()
	if len(nodes) == 1:
		node = nodes[0]
	return node

def isDigitalAsset(node):
	"""Returns True if node is a digital asset, False if not"""
	if node.type().definition() is None:
		return False
	else:
		return True

def saveOTL():
	"""Calls saveOTL with the selected node"""
	node = getSelectedNode()
	if node != None:
		saveOTL(node)

def saveOTL(node):
	"""If node is a digital asset,
		Saves node's operator type and marks node as the current defintion"""
	if isDigitalAsset(node):
		node.type().definition().updateFromNode(node)
		node.matchCurrentDefinition()

def switchOPLibraries(oldfilepath, newfilepath):
	hou.hda.uninstallFile(oldfilepath, change_oplibraries_file=False)
	hou.hda.installFile(newfilepath, change_oplibraries_file=True)
	hou.hda.uninstallFile("Embedded")

def copyToOtlDir(node, filename, newName, newDef):
	"""Moves the .otl file out of the USERDIR into the OTLDIR and removes it from USERDIR.
		Changes the oplibrary to the one in OTLDIR."""
	newfilepath = os.path.join(OTLDIR, filename)
	oldfilepath = os.path.join(USERDIR, filename)
	node.type().definition().copyToHDAFile(newfilepath, new_name=newName, new_menu_name=newDef)
	switchOPLibraries(oldfilepath, newfilepath)

def moveToOtlDir(node, filename):
	"""Calls copyToOtlDir and then removes the otl from USERDIR."""
	oldfilepath = os.path.join(USERDIR, filename)
	copyToOtlDir(node, filename, None, None)
	os.remove(oldfilepath)

def copyToUsrDir(node, filename):
	"""Copies the .otl file from OTLDIR to USERDIR
		Changes the oplibrary to the one in USERDIR"""
	if not os.path.exists(USERDIR):
		os.mkdir(USERDIR)
	newfilepath = os.path.join(USERDIR, filename)
	oldfilepath = os.path.join(OTLDIR, filename)
	node.type().definition().copyToHDAFile(newfilepath)
	switchOPLibraries(oldfilepath, newfilepath)

def lockOTL(filename):
	"""Updates the database entry specified by filename to locked=1 and lockedby=USERNAME"""
	con = lite.connect(database)
	with con:
		cur = con.cursor()
		cur.execute("UPDATE otl_table SET locked=1, lockedby='"+USERNAME+"' WHERE filename='"+filename+"'")
		con.commit()
	con.close()

def unlockOTL1():
	"""Calls unlockOTL with the selected node"""
	node = getSelectedNode()
	if node != None:
		if not isDigitalAsset(node):
			hou.ui.displayMessage("Not a Digital Asset.")
		else:
			libraryPath = node.type().definition().libraryFilePath()
			filename = os.path.basename(libraryPath)
			#TODO save this somewhere
			unlockOTL(filename)

def unlockOTL(filename):
	"""Updates the database entry specified by filename to locked=0 and lockedby=''"""
	con = lite.connect(database)
	with con:
		cur = con.cursor()
		cur.execute("UPDATE otl_table SET locked=0, lockedby='' WHERE filename='"+filename+"'")
		con.commit()
	con.close()

def addOTL(filename):
	"""Updates the database with a new table entry for filename"""
	con = lite.connect(database)
	with con:
		cur = con.cursor()
		cur.execute(insert_ignore_sql, (filename, 0, ""))
		con.commit()
	con.close()

def getFileInfo(filename):
	"""Returns all of the table information for filename"""
	info = None
	con = lite.connect(database)
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM otl_table WHERE filename='"+filename+"'")
		info = cur.fetchone()
	con.close()
	return info

def checkout():
	"""Checks out the selected node.  EXACTLY ONE node may be selected, and it MUST be a digital asset.
		The node must already exist in the database."""
	updateDB()
	node = getSelectedNode()
	if node != None:
		if not isDigitalAsset(node):
			hou.ui.displayMessage("Not a Digital Asset.")
		else:
			libraryPath = node.type().definition().libraryFilePath()
			filename = os.path.basename(libraryPath)
			info = getFileInfo(filename)
			if info == None:
				hou.ui.displayMessage("Add OTL First.")
			elif not info[2]: #or (info[2] and info[3] == USERNAME):
				copyToUsrDir(node, filename)
				node.allowEditingOfContents()
				lockOTL(filename)
				hou.ui.displayMessage("Checkout Successful!")
			else:
				hou.ui.displayMessage("Locked By: "+info[3].encode('utf-8'))
	else:
		hou.ui.displayMessage("Select EXACTLY one node.")

def checkin():
	"""Checks in the selected node.  EXACTLY ONE node may be selected, and it MUST be a digital asset.
		The node must already exist in the database, and USERNAME must have the lock."""
	updateDB()
	node = getSelectedNode()
	if node != None:
		if not isDigitalAsset(node):
			hou.ui.displayMessage("Not a Digital Asset.")
		else:
			libraryPath = node.type().definition().libraryFilePath()
			filename = os.path.basename(libraryPath)
			info = getFileInfo(filename)
			if info == None:
				hou.ui.displayMessage("Add the OTL first")
			elif info[2]:
				if not node.isLocked() and info[3] == USERNAME:
					saveOTL(node)                	
					moveToOtlDir(node, filename)
					unlockOTL(filename)
					hou.ui.displayMessage("Checkin Successful!")
				else:
					hou.ui.displayMessage("Locked By: "+info[3].encode('utf-8'))
			else:
				hou.ui.displayMessage("Already checked in.")
	else:
		hou.ui.displayMessage("Select EXACTLY one node.")

def revertChanges():
	updateDB()
	node= getSelectedNode()
	if node != None:
		if not isDigitalAsset(node):
			hou.ui.displayMessage("Not a Digital Asset.")
		else:
			libraryPath = node.type().definition().libraryFilePath()
			filename = os.path.basename(libraryPath)
			info = getFileInfo(filename)
			if info == None:
				hou.ui.displayMessage("OTL not in globals folder. Can not revert.")
			elif info[2]:
				if not node.isLocked() and info[3] == USERNAME:
					newfilepath = os.path.join(OTLDIR, filename)
					oldfilepath = os.path.join(USERDIR, filename)
					switchOPLibraries(oldfilepath, newfilepath)
					os.remove(oldfilepath)
					createMe = node.type().name()
					node.destroy()
					hou.node('/obj').createNode(createMe)
					unlockOTL(filename)
					hou.ui.displayMessage("Revert Successful!")
	else:
		hou.ui.displayMessage("Select EXACTLY one node.")

def formatName(name):
	name = name.strip()
	name = name.replace('_', ' ')
	if name.split()[0].lower() != os.environ['PROJECT_NAME']:
		name = str(os.environ['PROJECT_NAME'])+' '+name
	return name.lower()

def new():
	updateDB()
	templateNode = hou.node("/obj").createNode("newGeoTemplate")
	templateNode.hide(True)
	b = ('OK', 'Cancel')
	done = False
	ok = 0
	while not done and ok ==0:
		ok, resp = hou.ui.readInput("Enter the New Operator Label", buttons=b, title="New OTL")
		if ok == 0:
			name = formatName(resp)
			filename = name.replace(' ', '_')
			newfilepath = os.path.join(OTLDIR, filename+'.otl')
			if not os.path.exists(newfilepath):
				templateNode.type().definition().copyToHDAFile(newfilepath, new_name=filename, new_menu_name=name)
				hou.hda.installFile(newfilepath, change_oplibraries_file=True)
				hou.node('/obj').createNode(filename)
				#clean up
				templateNode.destroy()
				#create file heirarchy
				amu.createNewAssetFolders(os.environ['ASSETS_DIR'], filename)
				done = True
			else:
				hou.ui.displayMessage("OTL Alread Exists. Choose a different name.")

def add():
	"""Adds the selected node. EXACTLY ONE node may be selected, and it MUST be a digital asset.
		The node CAN NOT already exist in the database."""
	updateDB()
	node = getSelectedNode()
	if node != None:
		if node.type().definition() is None:
			hou.ui.displayMessage("Not a Digital Asset.")
		else:
			libraryPath = node.type().definition().libraryFilePath()
			filename = os.path.basename(libraryPath)
			info = getFileInfo(filename)
			if info == None:
				saveOTL(node)
				moveToOtlDir(node, filename)
				addOTL(filename)
				hou.ui.displayMessage("Add Successful!")
			else:
				hou.ui.displayMessage("Already Added")
	else:
		hou.ui.displayMessage("Select EXACTLY one node.")







