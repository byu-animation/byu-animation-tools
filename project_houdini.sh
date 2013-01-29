#!/bin/sh

# project_houdini.sh: opens houdini with the project environment
# @author Brian Kingery

# source current houdini setup
cd /opt/hfs.current
source ./houdini_setup
cd -

# source project environment
source ./project_env.sh

echo "Starting Houdini..."
houdinifx

