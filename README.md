========
Cognate
========

Welcome to **Cognate**, a package designed with making it easy to create
component services. **Cognate** strives to ease the burden of configuration
management and logging configuration, by providing the infrastructure.
**Cognate** fosters component service architectures by making the design,
implementation, and testing of services less of a chore.

A sample hello world component:

    from cognate.component_core import ComponentCore
    import sys

    class HelloWorld(ComponentCore):
        def __init__(self, name='World', **kwargs):
            self.name = name

            super().__init__(**kwargs)

        def cognate_options(self, arg_parser):
            arg_parser.add_argument(
                '--name',
                default=self.name,
                help='Whom will receive the salutation.')

        def run(self):
            self.log.info('Hello %s', self.name)


    if __name__ == '__main__':
        argv = sys.argv
        service = HelloWorld(argv=argv)
        service.run()

Allows for the executable:

    $ python hello_world.py -h
    usage: hello_world.py [-h] [--service_name SERVICE_NAME]
                          [--log_level {debug,info,warn,error}]
                          [--log_path LOG_PATH] [--verbose] [--name NAME]

    optional arguments:
      -h, --help            show this help message and exit
      --service_name SERVICE_NAME
                            This will set the name for the current instance.
                            This will be reflected in the log output.
                            (default: HelloWorld)
      --log_level {debug,info,warn,error}
                            Set the log level for the log output. (default: error)
      --log_path LOG_PATH   Set the path for log output. The default file created
                            is "<log_path>/<service_name>.log". If the path
                            ends with a ".log" extension, then the path be a
                            target file. (default: None)
      --verbose             Enable verbose log output to console. Useful for
                            debugging. (default: False)
      --name NAME           Whom will receive the salutation. (default: World)

Documentation
==============

For the latest documentation, visit http://neoinsanity.github.io/cognate.

Getting Cognate
==============

Installation
-------------

Use pip to install Cognate.

  > pip install cognate

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
