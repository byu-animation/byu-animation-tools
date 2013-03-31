#!/bin/sh

# project_maya.sh: opens maya with the project environment
# @author Brian Kingery

# source project environment
DIR=`dirname $0`
source ${DIR}/project_env.sh

export CURRENT_PROG='Nuke'

# Change directories so current directory is not in the tools folder
cd ${JOB}/tmp

echo "Starting Nuke..."
/usr/local/Nuke6.3v9/Nuke6.3 -b --nukex

