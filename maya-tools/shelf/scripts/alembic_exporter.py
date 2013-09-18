import maya.cmds as cmds
from pymel.core import *
import utilities as amu #asset manager utilities
import os

def saveFile():
  if not cmds.file(q=True, sceneName=True) == '':
    cmds.file(save=True, force=True) #save file

def getAssetName(filepath):
  return os.path.basename(filepath).split('.')[0]

def showConfirmAlembicDialog(references):
  return cmds.confirmDialog( title         = 'Export Alembic'
                           , message       = 'Export Alembic for:\n'+str(references)
                           , button        = ['Yes', 'No']
                           , defaultButton = 'Yes'
                           , cancelButton  = 'No'
                           , dismissString = 'No')

def get_root_nodes():
    root_nodes = ls(assemblies=True)
    ignoreables = ["persp", "top", "front", "side"]
    returnables = []
    for node in root_nodes:
        if node in ignoreables: 
            continue
        returnables.append(node)
    return returnables

def check_tag(node):
    if node.hasAttr("BYU_Alembic_Export_Flag"):
        return True

def tagged_children_generator(node):
    if check_tag(node):
        yield node
    else:
        for child in node.listRelatives(c=True):
            for tagged in tagged_children_generator(child):
                yield tagged

def list_tagged_nodes():
    for root in get_root_nodes():
        for tagged in tagged_children_generator(root):
            yield tagged

def build_alembic_command(abcfilepath):
    tagged = list_tagged_nodes()

    roots_string = ""
    for node in tagged:
        roots_string = " ".join([roots_string, "-root %s"%(node.name())])
    start_frame = playbackOptions(q=1, minTime=True) - 5
    end_frame = playbackOptions(q=1, maxTime=True) + 5
    command = 'AbcExport -j "%s -frameRange %s %s -step 0.25 -writeVisibility -nn -uv -file %s"'%(
                                    roots_string, 
                                    str(start_frame), 
                                    str(end_frame), 
                                    abcfilepath)
    return command

def convert(abcfilepath):
  loadPlugin("AbcExport")
  command = build_alembic_command(abcfilepath)
  print command
  Mel.eval(command)

def export_alembic():
  print "Exporting Alembic"

  saveFile()

  filePath = cmds.file(q=True, sceneName=True)
  toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
  dest = amu.getCheckinDest(toCheckin)


  references = cmds.ls(references=True)
  loaded=[]
  for ref in references:
    if cmds.referenceQuery(ref, isLoaded=True):
      loaded.append(ref)
      cmds.file(unloadReference=ref)

  if showConfirmAlembicDialog(loaded) == 'Yes':
    print loaded
    for ref in loaded:
      print "\n\n\n\n**************************************************************\n"
      constraints = []
      #TODO refactor the controller stuff to work with a 'prop list' it will scale easier
      if 'controller' in ref:
        for c in loaded:
          if 'owned_tommy_rig_stable' in c or 'owned_abby_rig_stable' in c or 'owned_jeff_rig_stable' in c:
            constraints.append(c);
      
      cmds.file(loadReference=ref)
      for c in constraints:
        print c
        cmds.file(loadReference=c)

      refPath = cmds.referenceQuery(ref, filename=True)
      assetName = getAssetName(refPath)
      print dest
      print filePath
      print refPath
      print assetName
      saveFile()
      abcfilepath = os.path.join(os.path.dirname(dest), 'animation_cache', 'abc', assetName+'.abc')
      convert(abcfilepath)
      cmds.file(unloadReference=ref)

    for ref in loaded:
      cmds.file(loadReference=ref)

saveFile()

def go():
  export_alembic()
