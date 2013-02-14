#!/bin/sh

# project_maya.sh: opens maya with the project environment
# @author Brian Kingery

# source project environment
DIR=`dirname $0`
source ${DIR}/project_env.sh

echo "Starting Maya..."
maya -script ${MAYA_SHELF_DIR}/byu_shelf.mel &

