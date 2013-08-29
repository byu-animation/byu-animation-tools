import hou as h

#unlock all objects
objects= h.node("/obj")
objects= objects.children()
count=0
num=len(objects)
while count<num:
    objects[count].allowEditingOfContents(True)
    count= count+1

#unlock apartment children
apt= h.node("/obj/owned_jeffs_apartment1")
childs= apt.children()
num=len(childs)
count=0
while count<num:
    childs[count].allowEditingOfContents(True)
    count= count+1

#unlock jeffs children
jeff= h.node("/obj/owned_jeff1")
childs= jeff.children()
num=len(childs)
count=0
while count<num:
    childs[count].allowEditingOfContents(True)
    count= count+1

#remove patch textures
allNodes= h.node("/obj").allSubChildren()
number= len(allNodes)
count= 0
while count<number:
    nodetype= allNodes[count].type().name()
    if nodetype=="material":
        culprit= str(allNodes[count].path())
        fpath= h.node(culprit)
        fpath.destroy()
    count=count+1

#edit shader nodes
allNodes= h.node("/obj").allSubChildren()
number= len(allNodes)
count=0
while count<number:
    nodetype= allNodes[count].type().name()
    if nodetype=="byu_uber_shader":
        uber= str(allNodes[count].path())
        upath= h.node(uber)
        upath.setParms({'baseColorr': 1, 'baseColorg': 1, 'baseColorb': 1})
        upath.setParms({'diff_int': .5, 'diff_rough': 0, 'useBaseColor': 1, 'useDiffNoise': 0, 'useColorMap': 0})
        upath.setParms({'usePointColor': 0})
        upath.setParms({'Shift': 0, 'Saturation': 1, 'Intensity': 1,'Gamma': 1})
        upath.setParms({'sss_enable': 0, 'baseRefl_enable': 0, 'coatRefl_enable2': 0, 'refr_enable': 0, 'emit_enable': 0})
    count=count+1
