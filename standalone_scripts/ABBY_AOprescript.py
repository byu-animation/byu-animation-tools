import hou as h

abby= h.node("/obj/owned_abby1")
abby.allowEditingOfContents(True)
apt= h.node("/obj/owned_abby_family_room1")
apt.allowEditingOfContents(True)
childs= apt.children()
num=len(childs)
count=0
while count<num:
    childs[count].allowEditingOfContents(True)
    count= count+1

allNodes= h.node("/obj").allSubChildren()
number= len(allNodes)
count=0
while count<number:
    type= allNodes[count].type().name()
    if type=="material":
        culprit= str(allNodes[count].path())
        fpath= h.node(culprit)
        parent= fpath.inputs()
        bob= str(parent[0].path())
        parentpath= h.node(bob)
        child= fpath.outputs()
        bob= str(child[0].path())
        childpath= h.node(bob)
        childpath.setFirstInput(parentpath)
    count=count+1
