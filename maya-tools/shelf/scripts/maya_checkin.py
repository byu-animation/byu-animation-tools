import maya.cmds as cmds
import utilities as amu #asset manager utilities
import maya_obj_export as geo
import shutil
import re
import os

def decodeFileName():
        # get the encoded folder name from the filesystem        
        encodedFolderName = os.path.basename(os.path.dirname(getFilePath()))

        # split the string based on underscore delimiters
        namesAry = encodedFolderName.split("_")
        
        # pop off the version and asset type information
        version   = namesAry.pop()
        assetType = namesAry.pop()

        #combine the array into a string to form the assetname
        assetName = '_'.join(namesAry)
        
        # return the assetName, assetType, and version
        return [assetName, assetType, version]        

def saveFile():
        cmds.file(save=True, force=True) #save file

def getFilePath():
        return cmds.file(query=True, list=True)[0].encode('utf-8')

def isModelAsset():
        # unpack decoded entries and check if assetType is a 'model'
        assetName, assetType, version = decodeFileName()
        return assetType == 'model'

def saveObjs():
        # this is not a model asset. don't save objs
        if not isModelAsset():
                return True
        
        # if we can export the objs, export the objs to the asset folder
        if geo.objExport_Default() == None:
                # unpack asset variables and combine to form source and destination paths
                assetName, assetType, version = decodeFileName()                
                srcDir  = os.path.join(os.path.dirname(getFilePath()), 'geo')                
                destDir = os.path.join(os.environ['ASSETS_DIR'], assetName, 'geo')
                
                # remove any existing geo folders in asset directory
                shutil.rmtree(path=destDir, ignore_errors=True)

                # copy geo folder over to destDir
                shutil.copytree(src=srcDir, dst=destDir)
                
                # delete local geo folder when copy is completed
                shutil.rmtree(path=srcDir)
                
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
        filePath = getFilePath()
        toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
        if amu.canCheckin(toCheckin) and saveObjs(): # objs must be saved before checkin
                cmds.file(force=True, new=True) #open new file
                amu.checkin(toCheckin) #checkin
        else:
                showFailDialog()

def go():
        checkin()

