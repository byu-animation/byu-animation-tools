from pymel.core import *
import sys, os

src_path = sys.argv[1]
dest_path = sys.argv[2]
print src_path
print dest_path

openFile(src_path, force=True)

def exportTo():
    parent = os.path.dir

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

def build_alembic_command():
    tagged = list_tagged_nodes()

    roots_string = ""
    for node in tagged:
        roots_string = " ".join([roots_string, "-root %s"%(node.name())])
    start_frame = playbackOptions(q=1, minTime=True) - 5
    end_frame = playbackOptions(q=1, maxTime=True) + 5
    file_name = dest_path
    command = 'AbcExport -j "%s -frameRange %s %s -step 0.25 -writeVisibility -nn -uv -file %s"'%(
                                    roots_string, 
                                    str(start_frame), 
                                    str(end_frame), 
                                    file_name)
    return command 

loadPlugin("AbcExport")
command = build_alembic_command()
print command
Mel.eval(command)
os._exit(0)
