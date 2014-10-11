==============
Cognate 0.0.1
==============

Source
-------

The latest stable release source of **Cognate** can be found on the master 
branch at https://github.com/neoinsanity/cognate/tree/master. 

For the latest development code, use the develop branch at 
https://github.com/neoinsanity/cognate. Please note that the development branch
may change without notification.

To install **Cognate** from source utilize the *setup.py*:

  > python setup.py install

Project Development
====================

If you are interested in developing **Cognate** code, 
utilize the helper scripts in the *cognate/bin* directory.

Setup the Development Environment
----------------------------------

Prior to running the dev setup scripts, ensure that you have *virtualenv* 
installed. All setup commands are assumed to be run from the project root, 
which is the directory containing the *setup.py* file.

Prep the development environment with the command:

  > bin/dev_setup.sh

This command will setup the virtualenv for the project in the 
directory */venv*. It will also install the **Cognate** in a develop mode, 
with the creation of a development egg file.

Enable the Development Environment
-----------------------------------

To make it easy to ensure a correctly configured development session, 
utilize the command:

  > . bin/enable_dev.sh
  
or

  > source bin/enable_dev.sh
  
Note that the script must be sourced, as it will enable a virtualenv session 
and add the *bin* directory scripts to environment *PATH*.

Running Tests
--------------

To run the unit tests:

  > run_tests.sh
  
A BUILD/COVERAGE_REPORT directory will be generated with the test coverage
report. To view the report, open index.html in the generated directory in 
a browser.

Building Documentation
-----------------------

To run the documentation generation:

  > doc_build.sh

A BUILD//doc/build directory will be generated with the documentation. To
view the documentation, open index.html in the generated directory in 
a browser.
