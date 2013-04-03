#!/bin/sh

# project_houdini.sh: opens houdini with the project environment
# @author Brian Kingery

# source current houdini setup
cd /opt/hfs.current
source ./houdini_setup
cd -

# source project environment
DIR=`dirname $0`
source ${DIR}/project_env.sh

# Change directories so $HIP is not in the tools folder
cd ${JOB}/tmp

echo "Starting Houdini..."
houdinifx

