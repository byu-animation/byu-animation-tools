#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI2.ui'
#
# Created: Mon May  7 16:38:31 2012
#	  by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os, types, sys
import controller

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class DeselectableTreeWidget(QTreeWidget):
    def mousePressEvent(self, event):
        if self.itemAt(event.pos()) is None:
            self.clearSelection()
        self.setCurrentItem(self.itemAt(event.pos()))
        QTreeWidget.mousePressEvent(self, event)
        

class FileSelectDialog(QDialog):
    def setup(self):
        self.setObjectName(_fromUtf8("file_select_dialog"))
        self.resize(330, 475)
        self.hl = QHBoxLayout(self)
        self.hl.setObjectName(_fromUtf8("horizontalLayout"))
        self.tw = QTreeWidget(self)
        self.tw.setObjectName(_fromUtf8("treeWidget"))
        self.hl.addWidget(self.tw)
        self.bb = QDialogButtonBox(self)
        self.bb.setOrientation(Qt.Vertical)
        self.bb.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.bb.setObjectName(_fromUtf8("buttonBox"))
        self.hl.addWidget(self.bb)
        self.setModal(True)
        self.setWindowTitle(QApplication.translate("Select a File", "", None, QApplication.UnicodeUTF8))
        self.tw.headerItem().setText(0, QApplication.translate("FileSelectDialog", "File", None, QApplication.UnicodeUTF8))
        QObject.connect(self.bb, SIGNAL(_fromUtf8("accepted()")), self.accept)
        QObject.connect(self.bb, SIGNAL(_fromUtf8("rejected()")), self.reject)
        QMetaObject.connectSlotsByName(self)
    
    def selectFile(self, filesToDisplay):
        self.tw.clear()
        self.tw.addTopLevelItems(filesToDisplay)
        if self.exec_() == 1:
            return self.tw.currentItem()
        else:
            return None

class NewFolderDialog(QDialog):
    def setup(self):
        self.setObjectName(_fromUtf8("newFolderDialog"))
        #self.resize(330, 475)
        self.hl = QHBoxLayout(self)
        self.hl.setObjectName(_fromUtf8("horizontalLayout"))
        #self.cb = QComboBox(self)
        #self.cb.setObjectName(_fromUtf8("comboBox"))
        #self.cb.addItems(QStringList(["Project Folder", "Versioned Folder"]))
        #self.hl.addWidget(self.cb)
        self.le = QLineEdit(self)
        self.le.setObjectName(_fromUtf8("lineEdit"))
        self.hl.addWidget(self.le)
        self.bb = QDialogButtonBox(self)
        self.bb.setOrientation(Qt.Vertical)
        self.bb.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.bb.setObjectName(_fromUtf8("buttonBox"))
        self.hl.addWidget(self.bb)
        self.setModal(True)
        self.setWindowTitle(QApplication.translate("New Asset", "", None, QApplication.UnicodeUTF8))
        QObject.connect(self.bb, SIGNAL(_fromUtf8("accepted()")), self.accept)
        QObject.connect(self.bb, SIGNAL(_fromUtf8("rejected()")), self.reject)
        QMetaObject.connectSlotsByName(self)
    
    def getNewFolder(self):
        #self.cb.setCurrentIndex(0)
        self.le.setText("NewAsset")
        self.le.selectAll()
        if self.exec_() == 1:
            #folderType = self.cb.currentIndex()
            folderName = str(self.le.text())
            return folderName
            #return [folderType, folderName]
        else:
            return [None, None]

class SettingsDialog(QDialog):
    def setup(self):
        self.setObjectName(_fromUtf8("SettingsDialog"))
        self.resize(572, 349)
        self.setWindowTitle(QApplication.translate("SettingsDialog", "Settings", None, QApplication.UnicodeUTF8))
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(210, 300, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        #self.OKButton = QDialogButtonBox.Ok
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        
        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(20, 20, 531, 231))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        
        self.userlabel = QLabel(self.gridLayoutWidget)
        self.userlabel.setText(QApplication.translate("SettingsDialog", "User Name:", None, QApplication.UnicodeUTF8))
        self.userlabel.setObjectName(_fromUtf8("userlabel"))
        self.gridLayout.addWidget(self.userlabel, 0, 0, 1, 1)
        
        self.projectlabel = QLabel(self.gridLayoutWidget)
        self.projectlabel.setText(QApplication.translate("SettingsDialog", "Project Folder:", None, QApplication.UnicodeUTF8))
        self.projectlabel.setObjectName(_fromUtf8("projectlabel"))
        self.gridLayout.addWidget(self.projectlabel, 1, 0, 1, 1)
        
        self.locallabel = QLabel(self.gridLayoutWidget)
        self.locallabel.setText(QApplication.translate("SettingsDialog", "Local Folder:", None, QApplication.UnicodeUTF8))
        self.locallabel.setObjectName(_fromUtf8("locallabel"))
        self.gridLayout.addWidget(self.locallabel, 2, 0, 1, 1)
        
        self.userLE = QLineEdit(self.gridLayoutWidget)
        self.userLE.setObjectName(_fromUtf8("userLE"))
        self.gridLayout.addWidget(self.userLE, 0, 1, 1, 1)
        
        self.projectLE = QLineEdit(self.gridLayoutWidget)
        self.projectLE.setObjectName(_fromUtf8("projectLE"))
        self.gridLayout.addWidget(self.projectLE, 1, 1, 1, 1)
        
        self.localLE = QLineEdit(self.gridLayoutWidget)
        self.localLE.setObjectName(_fromUtf8("localLE"))
        self.gridLayout.addWidget(self.localLE, 2, 1, 1, 1)
        
        self.projectBrowseButton = QPushButton(self.gridLayoutWidget)
        self.projectBrowseButton.setText(QApplication.translate("SettingsDialog", "Browse", None, QApplication.UnicodeUTF8))
        self.projectBrowseButton.setObjectName(_fromUtf8("projectBrowseButton"))
        self.gridLayout.addWidget(self.projectBrowseButton, 1, 2, 1, 1)
        
        self.localBrowseButton = QPushButton(self.gridLayoutWidget)
        self.localBrowseButton.setText(QApplication.translate("SettingsDialog", "Browse", None, QApplication.UnicodeUTF8))
        self.localBrowseButton.setObjectName(_fromUtf8("localBrowseButton"))
        self.gridLayout.addWidget(self.localBrowseButton, 2, 2, 1, 1)
        
        self.setupDirsDialog = QFileDialog(self)
        
        # Variables
        self.userName = ""
        self.projDir = ""
        self.localDir = ""
        
        QObject.connect(self.buttonBox, SIGNAL(_fromUtf8("accepted()")), self.accept)
        QObject.connect(self.buttonBox, SIGNAL(_fromUtf8("rejected()")), self.reject)
        QObject.connect(self.projectBrowseButton, SIGNAL("clicked()"), self.browseProject)
        QObject.connect(self.localBrowseButton, SIGNAL("clicked()"), self.browseLocal)
        QObject.connect(self.userLE, SIGNAL("textChanged(QString)"), self.setUserName)
        QObject.connect(self.projectLE, SIGNAL("textChanged(QString)"), self.setProjDir)
        QObject.connect(self.localLE, SIGNAL("textChanged(QString)"), self.setLocalDir)
        #QMetaObject.connectSlotsByName(self)
    
    def setUserName(self, text):
        self.userName = text
        self.enableComponents()
    def setProjDir(self, text):
        self.projDir = text
        self.enableComponents()
    def setLocalDir(self, text):
        self.localDir = text
        self.enableComponents()
    
    def enableComponents(self):
        if self.userName == "" or self.projDir == "" or self.localDir == "":
            #self.OKButton.setEnabled(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        elif not os.path.exists(self.projDir) or not os.path.exists(self.localDir):
            #self.OKButton.setEnabled(True)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
    
    def browseProject(self):
        path = self.setupDirsDialog.getExistingDirectory(self, "Choose Project Dir", os.environ['HOME'])
        if not path.isNull():
            self.projectLE.setText(path)
    
    def browseLocal(self):
        path = self.setupDirsDialog.getExistingDirectory(self, "Choose Local Directory", os.environ['HOME'])
        if not path.isNull():
            self.localLE.setText(path)
    
    def run(self):
        #self.userName = self.userLE.text()
        #self.projectPath = self.projectLE.text()
        #self.localPath = self.localLE.text()
        self.setUserName(self.userLE.text())
        self.setProjDir(self.projectLE.text())
        self.setLocalDir(self.localLE.text())
        
        if self.exec_() == 1:
            self.userName = self.userLE.text()
            self.projectPath = self.projectLE.text()
            self.localPath = self.localLE.text()
            return [self.userName, self.projectPath, self.localPath]
        else:
            return [None, None, None]
    
    def loadSettings(self, userName, projectPath, localPath):
        self.userLE.setText(userName)
        self.projectLE.setText(projectPath)
        self.localLE.setText(localPath)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self._MainWindow = MainWindow
        
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1000, 654)
        icon = QIcon()
        icon.addPixmap(QPixmap(_fromUtf8("images/./Disconnected.png")), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.mainWidget = QWidget(MainWindow)
        self.mainWidget.setObjectName(_fromUtf8("mainWidget"))
        self.horizontalLayout = QHBoxLayout(self.mainWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        #Tree Widgets and Tabs
        self.fileTabs = QTabWidget(self.mainWidget)
        self.fileTabs.setObjectName(_fromUtf8("fileTabs"))
        self.localFilesTab = QWidget()
        self.localFilesTab.setObjectName(_fromUtf8("localFilesTab"))
        self.verticalLayout_2 = QVBoxLayout(self.localFilesTab)
        self.verticalLayout_2.setMargin(5)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        #self.localFilesTreeWidget = QTreeWidget(self.localFilesTab)
        self.localFilesTreeWidget = DeselectableTreeWidget(self.localFilesTab)
        self.localFilesTreeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.localFilesTreeWidget.setObjectName(_fromUtf8("localFilesTreeWidget"))
        self.localFilesTreeWidget.header().setDefaultSectionSize(200)
        self.localFilesTreeWidget.setIndentation(12)
        self.verticalLayout_2.addWidget(self.localFilesTreeWidget)
        self.fileTabs.addTab(self.localFilesTab, _fromUtf8(""))
        
        self.projectFilesTab = QWidget()
        self.projectFilesTab.setObjectName(_fromUtf8("projectFilesTab"))
        self.verticalLayout = QVBoxLayout(self.projectFilesTab)
        self.verticalLayout.setMargin(5)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        #self.projectFilesTreeWidget = QTreeWidget(self.projectFilesTab)
        self.projectFilesTreeWidget = DeselectableTreeWidget(self.projectFilesTab)
        self.projectFilesTreeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.projectFilesTreeWidget.setObjectName(_fromUtf8("projectFilesTreeWidget"))
        self.projectFilesTreeWidget.header().setDefaultSectionSize(120)
        self.projectFilesTreeWidget.setIndentation(12)
        self.verticalLayout.addWidget(self.projectFilesTreeWidget)
        self.fileTabs.addTab(self.projectFilesTab, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.fileTabs)
        
        # Status Bar
        MainWindow.setCentralWidget(self.mainWidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        
        # Tool Bar
        self.toolbar = QToolBar(MainWindow)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolbar.sizePolicy().hasHeightForWidth())
        self.toolbar.setSizePolicy(sizePolicy)
        self.toolbar.setContextMenuPolicy(Qt.NoContextMenu)
        self.toolbar.setAllowedAreas(Qt.AllToolBarAreas)
        self.toolbar.setIconSize(QSize(48, 48))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar.setObjectName(_fromUtf8("toolbar"))
        MainWindow.addToolBar(Qt.RightToolBarArea, self.toolbar)
        
        # Define Actions
        self.actionSettings = QAction(MainWindow)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(_fromUtf8("images/Computer.png")), QIcon.Normal, QIcon.Off)
        self.actionSettings.setIcon(icon1)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        
        self.actionCheckout = QAction(MainWindow)
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(_fromUtf8("images/Download.png")), QIcon.Normal, QIcon.Off)
        self.actionCheckout.setIcon(icon2)
        self.actionCheckout.setObjectName(_fromUtf8("actionCheckout"))
        
        self.actionCheckin = QAction(MainWindow)
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(_fromUtf8("images/Upload.png")), QIcon.Normal, QIcon.Off)		
        self.actionCheckin.setIcon(icon3)
        self.actionCheckin.setObjectName(_fromUtf8("actionCheckin"))
        
        self.actionCache_to_Alembic = QAction(MainWindow)
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(_fromUtf8("images/alembic_logo_Darkest.png")), QIcon.Normal, QIcon.Off)
        self.actionCache_to_Alembic.setIcon(icon4)
        self.actionCache_to_Alembic.setObjectName(_fromUtf8("actionCache_to_Alembic"))
        
        self.actionInstall = QAction(MainWindow)
        icon5 = QIcon()
        icon5.addPixmap(QPixmap(_fromUtf8("images/Favourites.png")), QIcon.Normal, QIcon.Off)
        self.actionInstall.setIcon(icon5)
        self.actionInstall.setObjectName(_fromUtf8("actionInstall"))
        
        self.actionRefresh = QAction(MainWindow)
        icon6 = QIcon()
        icon6.addPixmap(QPixmap(_fromUtf8("images/Refresh.png")), QIcon.Normal, QIcon.Off)
        self.actionRefresh.setIcon(icon6)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        
        self.actionOpen_File = QAction(MainWindow)
        icon7 = QIcon()
        icon7.addPixmap(QPixmap(_fromUtf8("images/Format.png")), QIcon.Normal, QIcon.Off)
        self.actionOpen_File.setIcon(icon7)
        self.actionOpen_File.setObjectName(_fromUtf8("actionOpen_File"))
        
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        
        self.actionRename = QAction(MainWindow)
        self.actionRename.setObjectName(_fromUtf8("actionRename"))
        
        self.actionRemove = QAction(MainWindow)
        self.actionRemove.setObjectName(_fromUtf8("actionRemove"))
        icon8 = QIcon()
        icon8.addPixmap(QPixmap(_fromUtf8("images/Trash.png")), QIcon.Normal, QIcon.Off)
        self.actionRemove.setIcon(icon8)

        self.actionDiscard = QAction(MainWindow)
        self.actionDiscard.setObjectName(_fromUtf8("actionDiscard"))
        self.actionDiscard.setIcon(icon8)
        
        # Add Actions to Tool Bar
        self.toolbar.addAction(self.actionCheckout)
        self.toolbar.addAction(self.actionInstall)
        self.toolbar.addAction(self.actionCache_to_Alembic)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionCheckin)
        self.toolbar.addAction(self.actionOpen_File)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionRefresh)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionSettings)
        
        # Housekeeping...
        self.retranslateUi(MainWindow)
        self.fileTabs.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)
        
        # Popup Menus
        self.localPopMenu = QMenu(MainWindow)
        self.localPopMenu.addAction(self.actionCheckin)
        self.localPopMenu.addSeparator()
        self.localPopMenu.addAction(self.actionDiscard)
        self.localPopMenu.addAction(self.actionOpen_File)
        
        self.projectPopMenu = QMenu(MainWindow)
        self.projectPopMenu.addAction(self.actionCheckout)
        self.projectPopMenu.addAction(self.actionInstall)
        self.projectPopMenu.addSeparator()
        self.projectPopMenu.addAction(self.actionNew)
        self.projectPopMenu.addAction(self.actionRename)
        self.projectPopMenu.addAction(self.actionRemove)
        
        # Dialog Menus
        ## File Dialog
        self.file_select_dialog = FileSelectDialog(MainWindow)
        self.file_select_dialog.setup()
        
        ## Error Message
        self.errorMessage = QErrorMessage(MainWindow)
        
        ## Message Box
        self.messageBox = QMessageBox(MainWindow)
        
        ## Rename Dialog
        #QInputDialog.getText(MainWindow, "title", "label")
        
        ## New Folder Dialog
        self.newFolderDialog = NewFolderDialog(MainWindow)
        self.newFolderDialog.setup()
        
        ## Settings Dialog
        self.settingsDialog = SettingsDialog(MainWindow)
        self.settingsDialog.setup()
    
    def retranslateUi(self, MainWindow):
        #Set Titles
        MainWindow.setWindowTitle(QApplication.translate("MainWindow", "Asset Manager", None, QApplication.UnicodeUTF8))
        self.localFilesTreeWidget.headerItem().setText(0, QApplication.translate("MainWindow", "File Name", None, QApplication.UnicodeUTF8))
        self.localFilesTreeWidget.headerItem().setText(1, QApplication.translate("MainWindow", "Check Out Time", None, QApplication.UnicodeUTF8))
        self.localFilesTreeWidget.headerItem().setText(2, QApplication.translate("MainWindow", "Last Opened", None, QApplication.UnicodeUTF8))
        self.localFilesTreeWidget.header().resizeSection(0, 150)
        self.fileTabs.setTabText(self.fileTabs.indexOf(self.localFilesTab), QApplication.translate("MainWindow", "Checked Out", None, QApplication.UnicodeUTF8))
        
        #Set Section Sizes
        #self.projectFilesTreeWidget.setStyleSheet("QTreeView::item{border-right: 1px solid #d9d9d9;border-bottom: 1px solid #d9d9d9;}")
        self.projectFilesTreeWidget.headerItem().setText(0, QApplication.translate("MainWindow", "File Name", None, QApplication.UnicodeUTF8))
        self.projectFilesTreeWidget.headerItem().setText(1, QApplication.translate("MainWindow", "Checked Out By:", None, QApplication.UnicodeUTF8))
        self.projectFilesTreeWidget.headerItem().setText(2, QApplication.translate("MainWindow", "Checked In By:", None, QApplication.UnicodeUTF8))
        self.projectFilesTreeWidget.headerItem().setText(3, QApplication.translate("MainWindow", "Check In Time:", None, QApplication.UnicodeUTF8))
        self.projectFilesTreeWidget.headerItem().setText(4, QApplication.translate("MainWindow", "Installed?", None, QApplication.UnicodeUTF8))
        self.projectFilesTreeWidget.headerItem().setText(5, QApplication.translate("MainWindow", "File Reference:", None, QApplication.UnicodeUTF8))
        self.projectFilesTreeWidget.header().resizeSection(0, 200)
        self.projectFilesTreeWidget.header().resizeSection(1, 120)
        self.projectFilesTreeWidget.header().resizeSection(2, 120)
        self.projectFilesTreeWidget.header().resizeSection(3, 140)
        self.projectFilesTreeWidget.header().resizeSection(4, 80)
        self.projectFilesTreeWidget.header().resizeSection(5, 200)
        self.fileTabs.setTabText(self.fileTabs.indexOf(self.projectFilesTab), QApplication.translate("MainWindow", "Production Assets", None, QApplication.UnicodeUTF8))
        
        #Set Actions Text
        self.toolbar.setWindowTitle(QApplication.translate("MainWindow", "Tool Bar", None, QApplication.UnicodeUTF8))
        self.actionSettings.setText(QApplication.translate("MainWindow", "Settings", None, QApplication.UnicodeUTF8))
        self.actionSettings.setToolTip(QApplication.translate("MainWindow", "Configure Your Settings", None, QApplication.UnicodeUTF8))
        self.actionCheckout.setText(QApplication.translate("MainWindow", "Checkout", None, QApplication.UnicodeUTF8))
        self.actionCheckout.setToolTip(QApplication.translate("MainWindow", "Checkout Project File", None, QApplication.UnicodeUTF8))
        self.actionCheckin.setText(QApplication.translate("MainWindow", "Checkin", None, QApplication.UnicodeUTF8))
        self.actionCheckin.setToolTip(QApplication.translate("MainWindow", "Checkin a Local File", None, QApplication.UnicodeUTF8))
        self.actionCache_to_Alembic.setText(QApplication.translate("MainWindow", "Alembic", None, QApplication.UnicodeUTF8))
        self.actionInstall.setText(QApplication.translate("MainWindow", "Install", None, QApplication.UnicodeUTF8))
        self.actionInstall.setToolTip(QApplication.translate("MainWindow", "Install / Flatten a File", None, QApplication.UnicodeUTF8))
        self.actionRefresh.setText(QApplication.translate("MainWindow", "Refresh", None, QApplication.UnicodeUTF8))
        self.actionRefresh.setToolTip(QApplication.translate("MainWindow", "Refresh", None, QApplication.UnicodeUTF8))
        self.actionOpen_File.setText(QApplication.translate("MainWindow", "Open File", None, QApplication.UnicodeUTF8))
        self.actionOpen_File.setToolTip(QApplication.translate("MainWindow", "Open a Local or Project File in Maya or Houdini", None, QApplication.UnicodeUTF8))
        
        self.actionNew.setText(QApplication.translate("MainWindow", "New", None, QApplication.UnicodeUTF8))
        self.actionNew.setToolTip(QApplication.translate("MainWindow", "Create a new folder, asset, or shot.", None, QApplication.UnicodeUTF8))
        self.actionRename.setText(QApplication.translate("MainWindow", "Rename", None, QApplication.UnicodeUTF8))
        self.actionRename.setToolTip(QApplication.translate("MainWindow", "Rename this folder", None, QApplication.UnicodeUTF8))
        self.actionRemove.setText(QApplication.translate("MainWindow", "Remove", None, QApplication.UnicodeUTF8))
        self.actionRemove.setToolTip(QApplication.translate("MainWindow", "Remove this folder and its contents", None, QApplication.UnicodeUTF8))
        self.actionDiscard.setText(QApplication.translate("MainWindow", "Discard", None, QApplication.UnicodeUTF8))
        self.actionDiscard.setToolTip(QApplication.translate("MainWindow", "Discard Changes, and release lock", None, QApplication.UnicodeUTF8))

    
    def connectSignalsAndSlots(self, MainWindow):
        # Action calls
        QObject.connect(self.actionCache_to_Alembic, SIGNAL("triggered()"), self.alembic)
        QObject.connect(self.actionCheckout, SIGNAL("triggered()"), self.checkout)
        QObject.connect(self.actionCheckin, SIGNAL("triggered()"), self.checkin)
        QObject.connect(self.actionInstall, SIGNAL("triggered()"), self.install)
        QObject.connect(self.actionOpen_File, SIGNAL("triggered()"), self.openFile)
        QObject.connect(self.actionSettings, SIGNAL("triggered()"), self.settings)
        QObject.connect(self.actionRefresh, SIGNAL("triggered()"), self.refresh)
        QObject.connect(self.actionNew, SIGNAL("triggered()"), self.newFolder)
        QObject.connect(self.actionRename, SIGNAL("triggered()"), self.rename)
        QObject.connect(self.actionRemove, SIGNAL("triggered()"), self.remove)
        QObject.connect(self.actionDiscard, SIGNAL("triggered()"), self.discard)
        
        # Tabs
        QObject.connect(self.fileTabs, SIGNAL("currentChanged(int)"), self.tabSwitch)
        
        # File Selection Widgets
        QObject.connect(self.localFilesTreeWidget, SIGNAL("itemSelectionChanged()"), self.localItemSelectionChanged)
        QObject.connect(self.localFilesTreeWidget, SIGNAL("customContextMenuRequested(QPoint)"), self.localFilesContextMenu)
        QObject.connect(self.projectFilesTreeWidget, SIGNAL("itemSelectionChanged()"), self.projectItemSelectionChanged)
        QObject.connect(self.projectFilesTreeWidget, SIGNAL("customContextMenuRequested(QPoint)"), self.projectFilesContextMenu)
    
    def refresh(self):
    	controller.refreshTree(self)
    
    def alembic(self):
        controller.runAlembic(self)
    
    def checkout(self):
        controller.runCheckout(self)
    
    def checkin(self):
        controller.runCheckin(self)

    def discard(self):
        controller.runDiscard(self)
    
    def install(self):
        controller.runInstall(self)
    
    def openFile(self):
        controller.runOpen(self)
    
    def settings(self):
        controller.runSettings(self)
    
    def newFolder(self):
        controller.runNew(self)
    
    def rename(self):
        controller.runRename(self)
    
    def remove(self):
        controller.runRemove(self)
    
    def tabSwitch(self, tabNum):
        controller.tabSwitch(self, tabNum)
    
    def localItemSelectionChanged(self):
        controller.localItemSelectionChanged(self)
    
    def projectItemSelectionChanged(self):
        controller.projectItemSelectionChanged(self)
    
    def localFilesContextMenu(self, point):
        controller.localFilesContextMenu(self, point)
    
    def projectFilesContextMenu(self, point):
        controller.projectFilesContextMenu(self, point)
    
    def getTreeItemPath(self, treeItem, path):
        if not type(treeItem.parent()) == types.NoneType:
            path = self.getTreeItemPath(treeItem.parent(), path)
        
        path = os.path.join(path, str(treeItem.text(0)))
        return path
    
    def removeTreeItem(self, item):
        parent = item.parent()
        if not type(parent) == types.NoneType:
            parent.takeChild(parent.indexOfChild(item))
        else:
            tree = item.treeWidget()
            index = tree.indexOfTopLevelItem(item)
            tree.takeTopLevelItem(index)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.connectSignalsAndSlots(MainWindow)
    
    MainWindow.show()
    controller.setup(ui)
    sys.exit(app.exec_())
