#!/bin/bash

# project_evn.sh
#	Exports all project environment variables and creates missing directories
#	This script will need to be edited for each project.
#
#   Place this script and other tools inside the ${PROJECT_TOOLS} directory defined below.
#
# @author: Brian Kingery

###############################################################################
# Project specific environment variables
###############################################################################

# The name of the project (ie: owned)
export PROJECT_NAME=owned

# Root directory for the projcet (ie: /groups/owned)
# This directory should be created manually.
export JOB=/groups/${PROJECT_NAME}

# Tools/scripts directory. This project_env.sh script should be placed here.
# along with the other tools and scripts.
# Yes, its a chicken egg problem...
export PROJECT_TOOLS=${JOB}/byu-animation-tools

# Production directory
export PRODUCTION_DIR=${JOB}/PRODUCTION

# User directory for checkout files, testing, ect.
export USER_DIR=${JOB}/users/${USER}

# Directory for dailies
export DAILIES_DIR=${JOB}/dailies

# Root directory for assets
export ASSETS_DIR=${PRODUCTION_DIR}/assets

# Root directory for animation
export ANIMATION_DIR=${PRODUCTION_DIR}/animation

# Root directory for lighting files
export LIGHTING_DIR=${PRODUCTION_DIR}/lighting

# Directory for otls
export OTLS_DIR=${PRODUCTION_DIR}/otls

# Append to python path so batch scripts can access our modules
export PYTHONPATH=/usr/lib64/python2.6/site-packages:${PROJECT_TOOLS}:${PROJECT_TOOLS}/asset_manager:${PROJECT_TOOLS}/python2.6libs:${PYTHONPATH}

# Function to build directory structure
buildProjectDirs()
{
    # Create Dailies directory
    if [ ! -d "$DAILIES_DIR" ]; then
        mkdir -p "$DAILIES_DIR"
	mkdir -p "$DAILIES_DIR"/tmp
	mkdir -p "$DAILIES_DIR"/renders
    fi
    
    # Create Production directory
    if [ ! -d "$PRODUCTION_DIR" ]; then
        mkdir -p "$PRODUCTION_DIR"
    fi

    # Create Root directory for assets
    if [ ! -d "$ASSETS_DIR" ]; then
        mkdir -p "$ASSETS_DIR"
    fi

    # Create Root directory for animation
    if [ ! -d "$ANIMATION_DIR" ]; then
        mkdir -p "$ANIMATION_DIR"
    fi

    # Create Root directory for lighting files
    if [ ! -d "$LIGHTING_DIR" ]; then
        mkdir -p "$LIGHTING_DIR"
    fi

    # Create Directory for otls
    if [ ! -d "$OTLS_DIR" ]; then
        mkdir -p "$OTLS_DIR"
    fi

    # Create tmp directory for ifds
    if [ ! -d "$JOB"/tmp/ifds ]; then
	mkdir -p "$JOB"/tmp/ifds
    fi

    cp -u ${PROJECT_TOOLS}/otl_templates/*.otl ${OTLS_DIR}
}

# Uncomment to build the project directories
#buildProjectDirs

# Create User directory for checkout files, testing, ect.
if [ ! -d "$USER_DIR" ]; then
    mkdir -p "$USER_DIR"
    mkdir -p "$USER_DIR"/checkout
    mkdir -p "$USER_DIR"/otls
fi

###############################################################################
# Houdini specific environment
###############################################################################

# The Python that ships with RHEL5 is too old.
export HOUDINI_USE_HFS_PYTHON=1

# HSITE doesn't currently point to anything we can use right now...
export HSITE=/grp5

# Include GLOBAL_DIR in Houdini path, so we will pick up project settings and assets.
HOUDINI_PATH=${HOME}/houdini${HOUDINI_MAJOR_RELEASE}.${HOUDINI_MINOR_RELEASE}
HOUDINI_PATH=${HOUDINI_PATH}:${HSITE}/houdini${HOUDINI_MAJOR_RELEASE}.${HOUDINI_MINOR_RELEASE}
HOUDINI_PATH=${HOUDINI_PATH}:${PRODUCTION_DIR}:${HFS}/houdini
export HOUDINI_PATH

# Add our custom python scripts
export HOUDINI_PYTHON_LIB=${PYTHONPATH}:${HOUDINI_PYTHON_LIB}

# Add our custom shelf tools
export HOUDINI_TOOLBAR_PATH=${PROJECT_TOOLS}:${HOUDINI_PATH}

# Add production and checkout otls to the OTL PATH.
export HOUDINI_OTL_PATH=${OTLS_DIR}:${USER_DIR}/otls:${HOUDINI_PATH}

###############################################################################
# Maya specific environment
###############################################################################

# Add our custom python scripts
export BYU_MAYA_SHELF_DIR=${PROJECT_TOOLS}/maya-tools/shelf
export MAYA_SCRIPT_PATH=${MAYA_SCRIPT_PATH}:${PYTHONPATH}:${BYU_MAYA_SHELF_DIR}

###############################################################################
# BEGIN AWESOMENESS!!!
###############################################################################

