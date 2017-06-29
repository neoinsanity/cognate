#!/usr/bin/env bash

###########################################################
##### Create virtualenv for development.
# Virtualenv needs to be installed for this to work.
# If you don't have virtualenv installed please visit:
# https://pypi.python.org/pypi/virtualenv
# for instructions on installing virtualenv.
###########################################################

### Create the virtual environment.
# The virtualenv will attempt to make python 2.7 environment.
virtualenv venv

echo
echo "---------------------------------------------------"
echo "- Virtual environment created in directory 'venv'"
echo "---------------------------------------------------"


# Activate the virtual environment.
echo
echo "---------------------------------------------------"
echo "----- Activating virtual environment. -----"
echo "---------------------------------------------------"

source venv/bin/activate

echo "---------------------------------------------------"
echo

###########################################################
##### Install development related packages.
###########################################################
echo
echo "---------------------------------------------------"
echo "------ Installing development packages ------"
echo "---------------------------------------------------"
echo

pip install -r bin/dev_requirements.txt

echo
echo "---------------------------------------------------"
echo "------ Creating default config.py ------"
echo "---------------------------------------------------"
echo
