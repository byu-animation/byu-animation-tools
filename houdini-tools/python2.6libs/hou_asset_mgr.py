# Digital Asset management
# Provides New, Add, Checkin, Checkout, Revert, and other functionality for .otl files
# Author: Brian Kingery

import sqlite3 as lite
import os, glob
import hou
import subprocess as sp
import tempfile

import utilities as amu #asset manager utilites

JOB=os.environ['JOB']
USERNAME=os.environ['USER']
OTLDIR=os.environ['OTLS_DIR']
ASSETSDIR=os.environ['ASSETS_DIR']
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
        # try/except statement is needed for assets that generate code, like shaders.
        try:
            node.type().definition().updateFromNode(node)
        except:
            pass
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

def isContainer(node):
    ndef = node.type().definition()
    nsec = ndef.sections()['Tools.shelf']
    contents = str(nsec.contents())
    if contents.find('Container Assets') != -1:
        return True
    else:
        return False

def lockAsset(node, lockit):
    if isContainer(node):
        ndef = node.type().definition()
        nsec = ndef.sections()['Tools.shelf']
        contents = str(nsec.contents())
        opts = ndef.options()
        opts.setLockContents(lockit)
        ndef.setOptions(opts)

def lockedBy(logname):
    """Returns the true name of based on the login name passed in."""
    tfd = tempfile.NamedTemporaryFile(mode='r+') # Create temp file to write to
    myargs = ["/usr/bin/ldapsearch", "-LLL", "uid=" + str(logname), "cn"] # Command args
    try:
        sp.check_call(myargs, executable="ldapsearch", stdout=tfd)
        tfd.seek(0) # Return to start of file
        fstr = str(tfd.read()) # Read contents of file and cast to string
        tfd.close() # Close and delete our temp file
        fstr = fstr.strip() # Strip leading and trailing whitespace
        lastline = fstr.splitlines()[-1] # Get last line
        truename = lastline[4:] # Strip off first four characters of line

        lockstr = "This asset is locked by the following user:\n\n"
        lockstr += "User Name: " + logname + "\n"
        lockstr += "Real Name: " + truename
        return lockstr # Return lock string
    except Exception as ex:
        exstr = "Encountered exception: " + str(ex) + "\nUser's name not found."# Uh-oh... We jacked something up...
        return exstr

def get_filename(parentdir):
    return os.path.basename(os.path.dirname(parentdir))+'_'+os.path.basename(parentdir)

def checkoutLightingFile():
    shotPaths = glob.glob(os.path.join(os.environ['SHOTS_DIR'], '*'))
    selections = []
    for sp in shotPaths:
        selections.append(os.path.basename(sp))
    selections.sort()
    answer = hou.ui.selectFromList(selections, exclusive=True, message='Select shot file to checkout:')
    if answer:
        answer = answer[0]
        toCheckout = os.path.join(os.environ['SHOTS_DIR'], selections[answer], 'lighting')

        try:
            destpath = amu.checkout(toCheckout, True)
        except Exception as e:
            if not amu.checkedOutByMe(toCheckout):
                hou.ui.displayMessage('Can Not Checkout: '+str(e))
                return
            else:
                destpath = amu.getCheckoutDest(toCheckout)

        toOpen = os.path.join(destpath, get_filename(toCheckout)+'.hipnc')

        if os.path.exists(toOpen):
            hou.hipFile.load(toOpen)
        else:
            hou.hipFile.clear()
            hou.hipFile.save(toOpen)

def checkinLightingFile():
    print 'checkin lighting file'
    filepath = hou.hipFile.path()
    toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filepath)))
    if amu.canCheckin(toCheckin):
        hou.hipFile.save()
        hou.hipFile.clear()
        dest = amu.checkin(toCheckin)
    else:
        hou.ui.displayMessage('Checkin Failed')

def checkout():
    """Checks out the selected node.  EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node must already exist in the database."""
    updateDB()
    node = getSelectedNode()
    if node != None:
        if not isDigitalAsset(node):
            hou.ui.displayMessage("Not a Digital Asset.")
        else:
            if node.type().name() == "geometryTemplate":
                hou.ui.displayMessage("Cannot checkout geometry template node.")
                return False
            libraryPath = node.type().definition().libraryFilePath()
            filename = os.path.basename(libraryPath)
            info = getFileInfo(filename)
            if info == None:
                hou.ui.displayMessage("Add OTL First.")
            elif not info[2]: #or (info[2] and info[3] == USERNAME):
                copyToUsrDir(node, filename)
                lockAsset(node, True)
                saveOTL(node)
                node.allowEditingOfContents()
                lockOTL(filename)
                hou.ui.displayMessage("Checkout Successful!")
            else:
                hou.ui.displayMessage(lockedBy(info[3].encode('utf-8')))
    else:
        #hou.ui.displayMessage("Select EXACTLY one node.")
        checkoutLightingFile()

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
                    saveOTL(node) # This save is not strictly necessary since we save again two lines down
                    lockAsset(node, False)
                    saveOTL(node)
                    moveToOtlDir(node, filename)
                    unlockOTL(filename)
                    hou.ui.displayMessage("Checkin Successful!")
                else:
                    hou.ui.displayMessage(lockedBy(info[3].encode('utf-8')))
            else:
                hou.ui.displayMessage("Already checked in.")
    else:
        #hou.ui.displayMessage("Select EXACTLY one node.")
        checkinLightingFile()

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
        name = str(os.environ['PROJECT_NAME']) + ' ' + name
    return name.lower()

def listContainers():
    dirlist = list()
    for root,dirs,files in os.walk(ASSETSDIR):
        if root != ASSETSDIR:
            break
        else:
            for dir in dirs:
                dirlist.append(str(dir))
    dirlist.sort()
    return dirlist

def newContainer(hpath):
    templateNode = hou.node(hpath).createNode("containerTemplate")
    templateNode.hide(True)
    ok, resp = hou.ui.readInput("Enter the New Operator Label", buttons=('OK', 'Cancel'), title="OTL Label")
    if ok == 0 and resp.strip() != '':
        name = formatName(resp)
        filename = name.replace(' ', '_')
        newfilepath = os.path.join(OTLDIR, filename+'.otl')
        if not os.path.exists(newfilepath):
            # create file heirarchy if container asset
            amu.createNewAssetFolders(ASSETSDIR, filename)
            templateNode.type().definition().copyToHDAFile(newfilepath, new_name=filename, new_menu_name=name)
            hou.hda.installFile(newfilepath, change_oplibraries_file=True)
            newnode = hou.node(hpath).createNode(filename)
        else:
            hou.ui.displayMessage("Asset by that name already exists. Cannot create asset.", title='Asset Name', severity=hou.severityType.Error)
        
    # clean up
    templateNode.destroy()

def rename():
    """Renames the selected node. EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node must already exist in the database.
    """
    updateDB()
    node = getSelectedNode()
    if node != None:
        if not isDigitalAsset(node):
            hou.ui.displayMessage("Not a Digital Asset.")
        else:
            if isContainer(node):
                oldlibraryPath = node.type().definition().libraryFilePath()
                oldfilename = os.path.basename(oldlibraryPath)
                oldAssetName = oldfilename.split('.')[0]
                assetDirPath = os.path.join(ASSETSDIR, oldAssetName)
                info = getFileInfo(oldfilename)
                if not info[2]:
                    pok, presp = hou.ui.readMultiInput("Enter the rename password...", input_labels=('Password:',), password_input_indices=(0,), buttons=('OK', 'Cancel'), title="Rename Password")
                    presp = presp[0]
                    if pok != 0 or presp != 'r3n@m3p@ssw0rd':
                        hou.ui.displayMessage("Incorrect password. Better luck next time.", title='Incorrect Password', severity=hou.severityType.Error)
                        return
                    ok, resp = hou.ui.readInput("Enter the New Operator Label", buttons=('OK', 'Cancel'), title="Rename OTL")
                    if ok == 0 and resp.strip() != '':
                        name = formatName(resp)
                        newfilename = name.replace(' ', '_')
                        newfilepath = os.path.join(OTLDIR, newfilename+'.otl')
                        if os.path.exists(newfilepath):
                            hou.ui.displayMessage("Asset by that name already exists. Cannot rename asset.", title='Asset Name', severity=hou.severityType.Error)
                        elif not amu.canRename(assetDirPath, newfilename):
                            hou.ui.displayMessage("Asset checked out in Maya. Cannot rename asset.", title='Asset Name', severity=hou.severityType.Error)
                        else:
                            node.type().definition().copyToHDAFile(newfilepath, new_name=newfilename, new_menu_name=name)
                            hou.hda.installFile(newfilepath, change_oplibraries_file=True)
                            newnode = hou.node(determineHPATH()).createNode(newfilename)
                            node.destroy()
                            hou.hda.uninstallFile(oldlibraryPath, change_oplibraries_file=False)
                            os.system('rm -f '+oldlibraryPath)
                            amu.renameAsset(assetDirPath, newfilename)
                else:
                    hou.ui.displayMessage(lockedBy(info[3].encode('utf-8')))
            
    else:
        hou.ui.displayMessage("Select EXACTLY one node.")

def deleteAsset():
    """Deletes the selected node. EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node must already exist in the database. It may not be already checked out in Houdini
        or in Maya.
    """
    updateDB()
    node = getSelectedNode()
    if node != None:
        if not isDigitalAsset(node):
            hou.ui.displayMessage("Not a Digital Asset.", title='Non-Asset Node', severity=hou.severityType.Error)
            return
        else:
            if isContainer(node):
                oldlibraryPath = node.type().definition().libraryFilePath()
                oldfilename = os.path.basename(oldlibraryPath)
                oldAssetName = oldfilename.split('.')[0]
                assetDirPath = os.path.join(ASSETSDIR, oldAssetName)
                info = getFileInfo(oldfilename)
                if not info[2]:
                    ok, resp = hou.ui.readMultiInput("Enter the deletion password...", input_labels=('Password:',), password_input_indices=(0,), buttons=('OK', 'Cancel'), title="Delete Password")
                    resp = resp[0]
                    if ok == 0 and resp == 'd3l3t3p@ssw0rd':
                        name = formatName(resp)
                        if not amu.canRemove(assetDirPath):
                            hou.ui.displayMessage("Asset currently checked out in Maya. Cannot delete asset.", title='Maya Lock', severity=hou.severityType.Error)
                            return
                        else:
                            node.destroy()
                            hou.hda.uninstallFile(oldlibraryPath, change_oplibraries_file=False)
                            try:
                                amu.removeFolder(assetDirPath)
                                os.remove(oldlibraryPath)
                                message = "The following paths and files were deleted:\n" + assetDirPath + "\n" + oldlibraryPath
                                hou.ui.displayMessage(message, title='Asset Deleted', severity=hou.severityType.Message)
                            except Exception as ex:
                                hou.ui.displayMessage("The following exception occured:\n" + str(ex), title='Exception Occured', severity=hou.severityType.Error)
                                return

                else:
                    hou.ui.displayMessage(lockedBy(info[3].encode('utf-8')), title='Asset Locked', severity=hou.severityType.Error)
                    return
    else:
        hou.ui.displayMessage("Select EXACTLY one node.")
        return


def newGeo(hpath):
    templateNode = hou.node(hpath).createNode("geometryTemplate")
    alist = listContainers()
    ok, resp = hou.ui.readInput("Enter the New Operator Label", buttons=('OK', 'Cancel'), title="OTL Label")
    filename = str()
    if ok == 0 and resp.strip() != '':
        name = formatName(resp)
        filename = name.replace(' ', '_')
        templateNode.setName(filename, unique_name=True)
    answer = hou.ui.selectFromList(alist, exclusive=True, message='Select Container Asset this belongs to:')
    if not answer:
        hou.ui.displayMessage("Geometry must be associated with a container asset! Geometry asset not created.", severity=hou.severityType.Error)
        templateNode.destroy()
        return
    answer = answer[0]
    sdir = '$JOB/PRODUCTION/assets/'
    gfile = hou.ui.selectFile(start_directory=sdir + alist[answer]+'/geo', title='Choose Geometry', chooser_mode=hou.fileChooserMode.Read)
    if len(gfile) > 4 and gfile[:4] != '$JOB':
        hou.ui.displayMessage("Path must start with '$JOB'. Default geometry used instead.", title='Path Name', severity=hou.severityType.Error)
        templateNode.destroy()
    elif gfile != '':
        hou.parm(templateNode.path() + '/read_file/file').set(gfile)

def determineHPATH():
    hpane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    hpath = hpane.pwd().path()
    if not isinstance(hpane.pwd(), hou.ObjNode):
        hpath = "/obj"
    return hpath

def new():
    updateDB()
    otb = ('Container', 'Geometry', 'Cancel')
    optype = hou.ui.displayMessage("Choose operator type.", buttons=otb, title='Asset Type')
    hpath = determineHPATH()
    if optype == 0:
        newContainer(hpath)
    elif optype == 1:
        newGeo(hpath)

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

