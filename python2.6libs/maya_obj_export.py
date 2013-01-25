import maya.cmds as mc
import os

def objExport(selected, path):
        geoPath = os.path.join(path,"geo")
        size = len(selected)

        mc.sysFile(geoPath, makeDir=True)
        optionsStr = "groups=0;ptgroups=0;materials=0;smoothing=0;normals=0;uvs=1"
        exportType = "OBJexport"

        for geo in selected:
                mc.select(geo, r=True)
                geoName = geo + ".obj"
                geoName = geoName.replace(":", "_")
                filename = os.path.join(geoPath, geoName)
                print("Exporting \'" + filename + "\'...")
                mc.file(filename, force=True, options=optionsStr, type=exportType, preserveReferences=True, exportSelected=True)
                print("\tCOMPLETED")

def objExport_Default():
        selection = mc.ls(geometry=True, visible=True)
        outPath = os.path.dirname(mc.file(q=True, sceneName=True))
        objExport(selection, outPath)

def alembicExport():
    # TODO: Finish this
    print("NOT IMPLEMENTED: This needs to be finished")

objExport_Default()
