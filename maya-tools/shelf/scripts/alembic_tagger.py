from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
from pymel.core import *
import alembic_tagger_UI

import os
import maya.OpenMayaUI as omu
import sip

class AlembicTagger(object):
    def __init__(self, parent=None):
        self.TAGGED = set()

        self.dialog = self.make_ui()

        self.dialog.but_tag.clicked.connect(self.tag_selected)
        self.dialog.but_untag.clicked.connect(self.untag_selected)
        self.dialog.tree.clicked.connect(self.make_selection_from_tree)

        self.dialog.setParent(parent)
        self.dialog.show()
        self.populate_list()

    def make_ui(self):
        d = QtGui.QDialog(parent=maya_main_window())

        d.resize(394, 611)
        d.setWindowTitle("Alembic Tagger")
        verticalLayout = QtGui.QVBoxLayout(d)
        horizontalLayout = QtGui.QHBoxLayout()
        d.but_tag = QtGui.QPushButton(d)
        d.but_tag.setText("Tag")
        horizontalLayout.addWidget(d.but_tag)
        d.but_untag = QtGui.QPushButton(d)
        d.but_untag.setText("Untag")
        horizontalLayout.addWidget(d.but_untag)
        verticalLayout.addLayout(horizontalLayout)
        d.tree = QtGui.QTreeView(d)
        d.tree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        d.tree.setHeaderHidden(True)
        verticalLayout.addWidget(d.tree)
        return d


    def ls_geo(self, sl=False):
        return ls(sl=sl, tr=True)

    def populate_list(self):
        self.TAGGED = set()
        for obj in self.ls_geo():
            if obj.hasAttr("BYU_Alembic_Export_Flag"):
                self.TAGGED.add(str(obj))
        model = QtGui.QStringListModel()
        model.setStringList(list(self.TAGGED))
        self.dialog.tree.setModel(model)

    def tag_selected(self):
        print self.ls_geo(sl=True)
        for obj in self.ls_geo(sl=True):
            if not obj.hasAttr("BYU_Alembic_Export_Flag"):
                obj.addAttr("BYU_Alembic_Export_Flag", dv=True, at=bool, h=False, k=True)
        self.populate_list()

    def untag_selected(self):
        for obj in self.ls_geo(sl=True):
            if obj.hasAttr("BYU_Alembic_Export_Flag"):
                obj.deleteAttr("BYU_Alembic_Export_Flag")
        self.populate_list()

    def make_selection_from_tree(self, index):
        select([], cl=True)
        selectedindexes = self.dialog.tree.selectedIndexes()
        for i in selectedindexes:
            name = i.data().toString()
            select(str(name), add=True)

def maya_main_window():
    ptr = omu.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def go():
    parent.window = AlembicTagger(parent=maya_main_window())

if __name__ == '__main__':
    go()
