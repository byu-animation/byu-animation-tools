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

# Root directory for assets
export ASSETS_DIR=${PRODUCTION_DIR}/assets

# Root directory for animation
export ANIMATION_DIR=${PRODUCTION_DIR}/animation

# Root directory for lighting files
export LIGHTING_DIR=${PRODUCTION_DIR}/lighting

# Directory for otls
export OTLS_DIR=${PRODUCTION_DIR}/otls

# Append to python path so batch scripts can access our modules
export PYTHONPATH=${PROJECT_TOOLS}:${PROJECT_TOOLS}/asset_manager:${PROJECT_TOOLS}/python2.6libs:${PYTHONPATH}

# Function to build directory structure
buildDirs()
{
    # Create Production directory
    if [ ! -d "$PRODUCTION_DIR" ]; then
        mkdir -p "$PRODUCTION_DIR"
    fi

    # Create User directory for checkout files, testing, ect.
    if [ ! -d "$USER_DIR" ]; then
        mkdir -p "$USER_DIR"
        mkdir -p "$USER_DIR"/checkout
        mkdir -p "$USER_DIR"/otls
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
}

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
export HOUDINI_OTL_PATH=${OTLS_DIR}:${USER_DIR}/checkout/otls:${HOUDINI_PATH}

###############################################################################
# Maya specific environment
###############################################################################

# SOMEONE WRITE ME!

