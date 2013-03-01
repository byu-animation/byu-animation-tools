# This script is automatically run whenever Houdini starts.
import hou
import os

try:
    testenv = os.environ['CURRENT_PROG']
except KeyError as ke:
    os.environ['CURRENT_PROG'] = 'Houdini'
    
hou.hscript("unitlength 0.01;")
hou.hscript("unitmass 0.01;")

