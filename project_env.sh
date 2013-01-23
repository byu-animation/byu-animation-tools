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

# Root directory for the projcet (ie: /grp5/owned)
# This directory should be created manually.
export JOB=/home/bkingery/Storage/byu-animation/${PROJECT_NAME}

# Tools/scripts directory. This project_env.sh script should be placed here.
# along with the other tools and scripts.
# Yes, its a chicken egg problem...
export PROJECT_TOOLS=${JOB}/byu-animation-tools

# Production directory
export PRODUCTION_DIR=${JOB}/PRODUCTION
if [ ! -d "$PRODUCTION_DIR" ]; then
    mkdir -p "$PRODUCTION_DIR"
fi

# User directory for checkout files, testing, ect.
export USER_DIR=${JOB}/users/${USER}
if [ ! -d "$USER_DIR" ]; then
	mkdir -p "$USER_DIR"
	mkdir -p "$USER_DIR"/checkout
	mkdir -p "$USER_DIR"/otls
fi

# Root directory for assets
export ASSETS_DIR=${PRODUCTION_DIR}/assets
if [ ! -d "$ASSETS_DIR" ]; then
	mkdir -p "$ASSETS_DIR"
	mkdir -p "$ASSETS_DIR"/chars
	mkdir -p "$ASSETS_DIR"/props
	mkdir -p "$ASSETS_DIR"/set
fi

# Directory for models
#export MODELS_DIR=${PRODUCTION_DIR}/models
#if [ ! -d "$MODELS_DIR" ]; then
#	mkdir -p "$MODELS_DIR"
#fi

# Directory for rigs
#export RIGS_DIR=${PRODUCTION_DIR}/rigs
#if [ ! -d "$RIGS_DIR" ]; then
#	mkdir -p "$RIGS_DIR"
#fi

# Directory for animations
#export ANIMATIONS_DIR=${PRODUCTION_DIR}/animations
#if [ ! -d "$ANIMATION_DIR" ]; then
#	mkdir -p "$ANIMATION_DIR"
#fi

# Directory for otls
export OTLS_DIR=${PRODUCTION_DIR}/otls
if [ ! -d "$OTLS_DIR" ]; then
    mkdir -p "$OTLS_DIR"
fi


###############################################################################
# Houdini specific environment
###############################################################################

# The Python that ships with RHEL is too old.
export HOUDINI_USE_HFS_PYTHON=1

# HSITE doesn't currently point to anything useful...
export HSITE=/grp5

# Include GLOBAL_DIR in Houdini path, so we will pick up project settings and assets.
export HOUDINI_PATH=${HOME}/houdini${HOUDINI_MAJOR_RELEASE}.${HOUDINI_MINOR_RELEASE}:${HSITE}/houdini${HOUDINI_MAJOR_RELEASE}.${HOUDINI_MINOR_RELEASE}:${HFS}/houdini

# Add our custom python scripts
export HOUDINI_PYTHON_LIB=${PRODUCTION_TOOLS}/python2.6libs:${HOUDINI_PYTHON_LIB}

# Add our custom shelf tools
export HOUDINI_TOOLBAR_PATH=${PRODUCTION_TOOLS}/toolbar:${HOUDINI_TOOLBAR_PATH}

# Add production and checkout otls to the OTL PATH.
export HOUDINI_OTL_PATH=${OTLS_DIR}:${USER_DIR}/checkout/otls:${HOUDINI_PATH}

###############################################################################
# Maya specific environment
###############################################################################
















