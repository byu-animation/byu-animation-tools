#!/bin/sh

# project_maya.sh: opens maya with the project environment
# @author Brian Kingery

# source project environment
source ./project_env.sh

echo "Starting Maya..."
maya -script ${BYU_MAYA_SHELF_DIR}/byu_shelf.mel &

