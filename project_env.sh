#!/bin/bash

# project_evn.sh
#	Exports all project environment variables and creates missing directories
#	This script will need to be edited for each project
# @author: Brian Kingery

###############################################################################
# Project specific environment variables
###############################################################################

# The name of the project (ie: owned)
export PROJECT_NAME=owned

# Root directory for the projcet (ie: /grp5/owned)
export JOB=/grp5/${PROJECT_NAME}
if [ ! -d "$JOB" ]; then
	mkdir -p "$JOB"
fi

# User directory for checkout files, testing, ect.
export USER_DIR=${JOB}/users/${USER}
if [ ! -d "$USER_DIR" ]; then
	mkdir -p "$USER_DIR"
	mkdir -p "$USER_DIR"/checkout
	mkdir -p "$USER_DIR"/checkout/otls
fi

# Directory for models
export MODELS=${JOB}/models
if [ ! -d "$MODELS" ]; then
	mkdir -p "$MODELS"
fi

# Directory for rigs
export RIGS=${JOB}/rigs
if [ ! -d "$RIGS" ]; then
	mkdir -p "$RIGS"
fi

# Directory for animations
export ANIMATION=${JOB}/animations
if [ ! -d "$ANIMATION" ]; then
	mkdir -p "$ANIMATION"
fi

###############################################################################
# Houdini specific environment
###############################################################################

export GLOBAL_DIR=${JOB}/global

# Directory for houdini digital assets
export OTL_DIR=${GLOBAL_DIR}/otls

# The Python that ships with RHEL is too old.
export HOUDINI_USE_HFS_PYTHON=1

# HSITE doesn't currently point to anything useful...
export HSITE=/grp5

# Include GLOBAL_DIR in Houdini path, so we will pick up project settings and assets.
export HOUDINI_PATH=${HOME}/houdini${HOUDINI_MAJOR_RELEASE}.${HOUDINI_MINOR_RELEASE}:${GLOBAL_DIR}:${HSITE}/houdini${HOUDINI_MAJOR_RELEASE}.${HOUDINI_MINOR_RELEASE}:${HFS}/houdini

# We also want to check for otls in a user's work folder.
export HOUDINI_OTL_PATH=${USER_DIR}:${HOUDINI_PATH}

###############################################################################
# Maya specific environment
###############################################################################
















