#!/usr/bin/env bash

###########################################################
##### Create virtualenv for development.
###########################################################

### Create the virtual environment.
# The virtualenv will attempt to make python 2.7 environment.
python3 -m venv .venv

echo
echo "---------------------------------------------------"
echo "- Virtual environment created in directory '.venv'"
echo "---------------------------------------------------"


# Activate the virtual environment.
echo
echo "---------------------------------------------------"
echo "----- Activating virtual environment. -----"
echo "---------------------------------------------------"

source .venv/bin/activate

echo "---------------------------------------------------"
echo

###########################################################
##### Install the cognate package in development mode.
###########################################################
echo
echo "------------------------------------------------"
echo "------ Setting up development environment ------"
echo "------------------------------------------------"

python setup.py develop

###########################################################
##### Install development related packages.
###########################################################
echo
echo "---------------------------------------------------"
echo "------ Installing development packages ------"
echo "---------------------------------------------------"
echo

pip install -r bin/dev_requirements.txt
