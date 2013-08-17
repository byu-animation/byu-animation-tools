#!/bin/sh

# project_houdini.sh: opens houdini with the project environment
# @author Brian Kingery

if [ -z "${HFS}" ]
then
    # The default HFS directory if it isn't already defined
    export HFS=/opt/hfs12.1.current
fi

# source current houdini setup
cd ${HFS}
source ./houdini_setup
cd -

# source project environment
DIR=`dirname $0`
source ${DIR}/project_env.sh

# Change directories so $HIP is not initially in the tools folder
cd ${USER_DIR}

echo "Starting Houdini..."
houdinifx "$@"

