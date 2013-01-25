from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os, glob, types, subprocess, sys
import utilities
from utilities import *

_tabNum = 0

def setup(ui):
    #os.putenv("MAYA_LOCATION", "/usr/autodesk/maya")
    #print os.environ["MAYA_LOCATION"]
    #os.putenv("HFS", "/opt/hfs.current")
    #print os.environ["HFS"]
    #if not os.path.exists(os.path.abspath(os.path.join(sys.path[0], ".myConfig.ini"))):
    #    runSettings(ui)
    #else:
    #    configureProject(os.path.abspath(os.path.join(sys.path[0],'.myConfig.ini')))
    populateLocalTree(ui)
    populateProjectTree(ui)
    enableComponents(ui)
    
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Common User Actions

def runAlembic(ui):
	ui.errorMessage.showMessage("Not Implemented")
	print "Alembic"

def runCheckout(ui):
    tabNum = ui.fileTabs.currentIndex()
    if tabNum == 1:
        curItem = ui.projectFilesTreeWidget.currentItem()
        coPath = ui.getTreeItemPath(curItem, getProductionDir())
        try:
            #TODO ask about locking?
            checkout(coPath, True)
            setProjectTreeVersionedItemInfo(curItem, coPath)
            populateLocalTree(ui)
        except Exception:
            ui.errorMessage.showMessage("Error")
    else:
        ui.errorMessage.showMessage("You can only checkout project files")

def runCheckin(ui):
    tabNum = ui.fileTabs.currentIndex()
    if tabNum == 0:
        curItem = ui.localFilesTreeWidget.currentItem()
        toCheckin = ui.getTreeItemPath(curItem, getUserCheckoutDir())
        if canCheckin(toCheckin):
            checkin(toCheckin)
            populateLocalTree(ui)
            populateProjectTree(ui)
        else:
            ui.errorMessage.showMessage("Can not checkin: file is locked or newer verion is available")
    else:
        ui.errorMessage.showMessage("You can only checkin local files")

def runDiscard(ui):
	if ui.fileTabs.currentIndex() == 0:
		curItem = ui.localFilesTreeWidget.currentItem()
		toDiscard = ui.getTreeItemPath(curItem, getUserCheckoutDir())
		discard(toDiscard)
		populateLocalTree(ui)
		populateProjectTree(ui)

def runInstall(ui):
    tabNum = ui.fileTabs.currentIndex()
    if tabNum == 1:
        curItem = ui.projectFilesTreeWidget.currentItem()
        vDirPath = ui.getTreeItemPath(curItem, getProductionDir())
        files = getAvailableInstallFiles(vDirPath)
        selected = ui.file_select_dialog.selectFile(convertToFileSelectionDialogItems(files))
        if not selected == None:
            srcFilePath = str(selected.text(1))
            install(vDirPath, srcFilePath)
            setProjectTreeVersionedItemInfo(curItem, vDirPath)
    else:
        ui.errorMessage.showMessage("You can only install project files")


def runNew(ui):
	if ui.fileTabs.currentIndex() == 1:
		curItem = ui.projectFilesTreeWidget.currentItem()
		if curItem != None and curItem.isSelected() and isVersionedFolder(ui.getTreeItemPath(curItem, getProductionDir())):
			return
		folderName = ui.newFolderDialog.getNewFolder()
		#ui.projectFilesTreeWidget.addTopLevelItems(convertToProjectTreeItems([newPath]))
		#if folderType == None or folderName == None:
		#    return
		if curItem != None and curItem.isSelected():
			if curItem.text(0) == 'assets':
				newPath = createNewAssetFolders(ui.getTreeItemPath(curItem, getProductionDir()), folderName)
				refreshTree(ui)
			elif curItem.text(0) == 'lighting' or curItem.text(0) == 'animation':
				newPath = addVersionedFolder(ui.getTreeItemPath(curItem, getProductionDir()), folderName)
				curItem.addChildren(convertToProjectTreeItems([newPath]))
		#    if folderType == 0:
		#        newPath = addProjectFolder(ui.getTreeItemPath(curItem, getProductionDir()), folderName)
		#    else:
		#        newPath = addVersionedFolder(ui.getTreeItemPath(curItem, getProductionDir()), folderName)
		#    curItem.addChildren(convertToProjectTreeItems([newPath]))
		#else:
		#    if folderType == 0:
		#        newPath = addProjectFolder(getProductionDir(), folderName)
		#    else:
		#        newPath = addVersionedFolder(getProductionDir(), folderName)
		#    ui.projectFilesTreeWidget.addTopLevelItems(convertToProjectTreeItems([newPath]))
		#createNewAssetFolders(getProductionDir(), folderName)
		#refreshTree(ui)
	else:
		print "local new"

def runRename(ui):
    if ui.fileTabs.currentIndex() == 1:
        curItem = ui.projectFilesTreeWidget.currentItem()
        a, ok = QInputDialog.getText(ui._MainWindow, "Rename Dialog", "New Name:", QLineEdit.Normal, curItem.text(0))
        #ui.renameDialog.setTextValue(curItem.text(0))
        if ok:
            name = str(a)
            try:
                renameFolder(ui.getTreeItemPath(curItem, getProductionDir()), name)
                curItem.setText(0, name)
            except Exception:
                ui.errorMessage.showMessage("Error")

def runRemove(ui):
    if ui.fileTabs.currentIndex() == 1:
        curItem = ui.projectFilesTreeWidget.currentItem()
        curItemPath = str(ui.getTreeItemPath(curItem, getProductionDir()))
        if not isEmptyFolder(curItemPath):
            warning = "Folder NOT empty! You will destroy data! \nContinue?"
            reply = ui.messageBox.question(ui._MainWindow,'Warning', warning, QMessageBox.Yes, QMessageBox.No)
        else:
            reply = QMessageBox.Yes
        if reply == QMessageBox.Yes:
            removeFolder(curItemPath)
            ui.removeTreeItem(curItem)

def runOpen(ui):
    if ui.fileTabs.currentIndex() == 0:
        curItem = ui.localFilesTreeWidget.currentItem()
        dirPath = ui.getTreeItemPath(curItem, getUserCheckoutDir())
        files = glob.glob(os.path.join(dirPath, "*"))
        selected = ui.file_select_dialog.selectFile(convertToFileSelectionDialogItems(files))
        if not selected == None:
            toOpen = str(selected.text(1))
            if utilities._isHoudiniFile(toOpen):
                subprocess.call([os.path.abspath(os.path.join(sys.path[0], "openHoudiniFile")), toOpen])
            else:
                os.system("gnome-open "+toOpen)

def refreshTree(ui):
	if ui.fileTabs.currentIndex() == 0:
		populateLocalTree(ui)
	else:
		populateProjectTree(ui)

def runSettings(ui):
    settings = 'Username: '+getUsername()+'\nProject Folder: '+getProductionDir()+'\nChecked Out Folder: '+getUserCheckoutDir()
    ui.messageBox.information(ui._MainWindow, 'Settings', settings)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Model to GUI Conversions

def convertToFileSelectionDialogItems(files):
    treeItems = []
    for f in files:
        item = QTreeWidgetItem()
        item.setText(0, os.path.basename(f))
        item.setText(1, f)
        treeItems.append(item)
    return treeItems

def convertToLocalTreeItems(files):
    treeItems = []
    for f in files:
        item = QTreeWidgetItem()
        item.setText(0, os.path.basename(f))
        item.setText(2, time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime(os.path.getmtime(f))))
        try:
        	item.setText(1, getFilesCheckoutTime(f))
        except:
        	item.setText(1, "Not a versioned Folder")
        	item.setText(2, "N/A") #TODO last opened stuff
        treeItems.append(item)
    return treeItems

def convertToProjectTreeItems(files):
    treeItems = []
    for f in files:
        item = QTreeWidgetItem()
        item.setText(0, os.path.basename(f))
        if isVersionedFolder(f):
            setProjectTreeVersionedItemInfo(item, f)
        treeItems.append(item)
    return treeItems

def setProjectTreeVersionedItemInfo(pTreeItem, curDir):
    info = getVersionedFolderInfo(curDir)
    pTreeItem.setText(1, info[0])
    pTreeItem.setText(2, info[1])
    pTreeItem.setText(3, info[2])
    pTreeItem.setText(4, info[3])
    pTreeItem.setText(5, info[4])

def populateProjectTree(ui):
    ui.projectFilesTreeWidget.clear()
    recurseProjectFiles(ui, ui.projectFilesTreeWidget, getProductionDir())
    ui.projectFilesTreeWidget.sortItems(0,0)

def recurseProjectFiles(ui, parent, curDir):
    if isVersionedFolder(curDir):
        setProjectTreeVersionedItemInfo(parent, curDir)
        return
    if os.path.isdir(curDir):
        files = glob.glob(os.path.join(curDir, '*'))
        for f in files:
            item = QTreeWidgetItem(parent)
            item.setText(0, os.path.basename(f))
            recurseProjectFiles(ui, item, f)

def populateLocalTree(ui):
    ui.localFilesTreeWidget.clear()
    files = glob.glob(os.path.join(str(getUserCheckoutDir()),'*'))
    items = convertToLocalTreeItems(files)
    ui.localFilesTreeWidget.addTopLevelItems(items)
    ui.localFilesTreeWidget.sortItems(1,0)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Other Helper Functions

def enableComponents(ui):
	# Project Tab Open
	if ui.fileTabs.currentIndex():
		ui.actionCheckin.setEnabled(False)
		ui.actionOpen_File.setEnabled(False)
		
		ui.actionNew.setEnabled(True)
		ui.actionCheckout.setEnabled(False)
		ui.actionInstall.setEnabled(False)
		ui.actionCache_to_Alembic.setEnabled(False)
		ui.actionRename.setEnabled(False)
		ui.actionRemove.setEnabled(False)
		
		curItem = ui.projectFilesTreeWidget.currentItem()	

		if curItem and curItem.isSelected():
			curItemPath = ui.getTreeItemPath(curItem, getProductionDir())
			#if curItem.text(2):
			if isVersionedFolder(curItemPath):
				ui.actionNew.setEnabled(False)
				ui.actionCheckout.setEnabled(True)
				ui.actionInstall.setEnabled(True)
				ui.actionCache_to_Alembic.setEnabled(True)
			if canRename(curItemPath):
				ui.actionRename.setEnabled(True)
			if canRemove(curItemPath):
				ui.actionRemove.setEnabled(True)
			#ui.actionNew.setEnabled(True)
	# Local Tab Open
	else:
		ui.actionNew.setEnabled(False)
		ui.actionRename.setEnabled(False)
		ui.actionRemove.setEnabled(False)
		
		curItem = ui.localFilesTreeWidget.currentItem()
		ui.actionCheckout.setEnabled(False)
		ui.actionInstall.setEnabled(False)
		ui.actionCache_to_Alembic.setEnabled(False)
		if not type(curItem) == types.NoneType and curItem.isSelected():
			if not str(curItem.text(1)) == "Not a versioned Folder":
				ui.actionCheckin.setEnabled(True)
				ui.actionOpen_File.setEnabled(True)
		else:
			ui.actionCheckin.setEnabled(False)
			ui.actionOpen_File.setEnabled(False)

def tabSwitch(ui, tabNum):
    enableComponents(ui)

def localItemSelectionChanged(ui):
    enableComponents(ui)
    
def projectItemSelectionChanged(ui):
    enableComponents(ui)

def localFilesContextMenu(ui, point):
    enableComponents(ui)
    ui.localPopMenu.popup(ui.projectFilesTreeWidget.mapToGlobal(point))

def projectFilesContextMenu(ui, point):
    enableComponents(ui)
    ui.projectPopMenu.popup(ui.projectFilesTreeWidget.mapToGlobal(point))

def fileDialogAccept():
    print "Accepted"
def fileDialogRejected():
    print "Rejected"

