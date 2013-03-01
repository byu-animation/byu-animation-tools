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

def isRigAsset():
        # unpack decoded entries and check if assetType is a 'rig'
        assetName, assetType, version = geo.decodeFileName()
        return assetType == 'rig'

def isAnimationAsset():
        # unpack decoded entries and check if assetType is a 'rig'
        assetName, assetType, version = geo.decodeFileName()
        return assetType == 'animation'

def saveGeo():
        # this is not a model asset. don't save objs
        if not isModelAsset():
                return True
        
        print 'we have a model'
        # if we can export the objs, export the objs to the asset folder
        if geo.generateGeometry():
                print 'generateGeometry done'
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
        print 'checkin'
        saveFile() # save the file before doing anything
        print 'save'
        filePath = cmds.file(q=True, sceneName=True)
        print 'filePath: '+filePath
        toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
        print 'toCheckin: '+toCheckin
        rig = isRigAsset()
        anim = isAnimationAsset()
        if amu.canCheckin(toCheckin) and saveGeo(): # objs must be saved before checkin
                cmds.file(force=True, new=True) #open new file
                dest = amu.checkin(toCheckin) #checkin
                srcFile = amu.getAvailableInstallFiles(dest)[0]
                if rig:
                    amu.install(dest, srcFile)
                if anim:
                    amu.runAlembicConverter(dest, srcFile)
        else:
                showFailDialog()

def go():
        try:
                checkin()
        except Exception as ex:
                msg = "RuntimeException:" + str(ex)
                print msg
                cmds.confirmDialog( title         = 'Uh Oh!'
                                  , message       = 'An exception just occured!\r\nHere is the message: ' + msg
                                  , button        = ['Dismiss']
                                  , defaultButton = 'Dismiss'
                                  , cancelButton  = 'Dismiss'
                                  , dismissString = 'Dismiss')
                

