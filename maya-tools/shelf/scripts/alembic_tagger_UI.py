# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/alembic_tagger.ui'
#
# Created: Wed Feb 13 21:55:09 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AlembicTaggerDialog(object):
    def setupUi(self, AlembicTaggerDialog):
        AlembicTaggerDialog.setObjectName(_fromUtf8("AlembicTaggerDialog"))
        AlembicTaggerDialog.resize(394, 611)
        AlembicTaggerDialog.setWindowTitle(QtGui.QApplication.translate("AlembicTaggerDialog", "Alembic Tagger", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(AlembicTaggerDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.but_tag = QtGui.QPushButton(AlembicTaggerDialog)
        self.but_tag.setText(QtGui.QApplication.translate("AlembicTaggerDialog", "Tag", None, QtGui.QApplication.UnicodeUTF8))
        self.but_tag.setObjectName(_fromUtf8("but_tag"))
        self.horizontalLayout.addWidget(self.but_tag)
        self.but_untag = QtGui.QPushButton(AlembicTaggerDialog)
        self.but_untag.setText(QtGui.QApplication.translate("AlembicTaggerDialog", "Untag", None, QtGui.QApplication.UnicodeUTF8))
        self.but_untag.setObjectName(_fromUtf8("but_untag"))
        self.horizontalLayout.addWidget(self.but_untag)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tree = QtGui.QTreeView(AlembicTaggerDialog)
        self.tree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tree.setHeaderHidden(True)
        self.tree.setObjectName(_fromUtf8("tree"))
        self.verticalLayout.addWidget(self.tree)

        self.retranslateUi(AlembicTaggerDialog)
        QtCore.QMetaObject.connectSlotsByName(AlembicTaggerDialog)

    def retranslateUi(self, AlembicTaggerDialog):
        pass

