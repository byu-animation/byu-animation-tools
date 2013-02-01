import maya.cmds as cmds
import utilities as amu #asset manager utilities
import maya_geo_export as geo
import os

def saveFile():
        if not cmds.file(q=True, sceneName=True) == '':
                cmds.file(save=True, force=True) #save file

def isModelAsset():
        # unpack decoded entries and check if assetType is a 'model'
        assetName, assetType, version = geo.decodeFileName()
        return assetType == 'model'

def saveGeo():
        # this is not a model asset. don't save objs
        if not isModelAsset():
                return True
        
        # if we can export the objs, export the objs to the asset folder
        if geo.generateGeometry():
                geo.installGeometry()
                
                return True # copy was successful
        else:
                return False

def showFailDialog(): 
        return cmds.confirmDialog( title         = 'Checkin Failed'
                                 , message       = 'Checkin was unsuccessful'
                                 , button        = ['Ok']
                                 , defaultButton = 'Ok'
                                 , cancelButton  = 'Ok'
                                 , dismissString = 'Ok')

def checkin():
        saveFile() # save the file before doing anything
        filePath = cmds.file(q=True, sceneName=True)
        toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
        if amu.canCheckin(toCheckin) and saveGeo(): # objs must be saved before checkin
                cmds.file(force=True, new=True) #open new file
                amu.checkin(toCheckin) #checkin
        else:
                showFailDialog()

def go():
        checkin()

