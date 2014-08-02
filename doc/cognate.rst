.. _getting-started-with-cognate:

=============================
Getting Started with Cognate
=============================

For details, be sure to checkout the features described under the
:ref:`component_core_class_utilization` section.:

- :ref:`configuration_management_and_initialization`

- :ref:`logging_and_log_configuration`

- :ref:`dynamic_service_naming`

The intent is for *ComponentCore* to make your life easier in the implementation
of stand alone applications. The hope is to take some common service
requirements and make the expression of those requirements trivial.

.. _component_core_class_utilization:

ComponentCore Class Utilization
================================

*ComponentCore* operates by accepting an *argv* passed in the
:meth:'^cognate.ComponentCore.__init__ method`. During the initialization
of instance based on *ComponentCore* derived class, *ComponentCore* will drive
configuration by applying *argv* options to instance **self**.

By way of example, let's construct a hello world example. First we define
*HelloWorld* class as below:

.. _hello_world_class:

HelloWorld Class
-----------------

.. code-block:: python
  :linenos:

  from cognate import ComponentCore
  import sys

  class HelloWorld(ComponentCore):
    def __init__(self, **kwargs):
      self.response = 'Hello World'

      # !!! Very important, Do NOT forget. !!!
      ComponentCore.__init__(self, **kwargs)

    def configuration_options(self, arg_parser):
      arg_parser.add_argument('-response', default=self.response)

    def configure(self, args):
      if(args.response != 'Hello World':  # is default value
        self.response += ' You Rascal!'

    def run(self):
      print self.response

  if __name__ == '__main__':
    helloWorld = HelloWorld(argv=sys.argv)
    helloWorld.run

This gives the class hierarchy as in the image below.

.. figure:: images/cognate_utilization_example_hierarchy.png

  ComponentCore Example Hierarchy

The essence of how *ComponentCore* performs it's operations is via the use of
:mod:`cognate.attribute_helper` module to derive configuration of service stack.
The basic call sequence is depicted in the image below.

.. image:: images/cognate_utilization_example_sequence.png

:meth:`cognate.component_core.ComponentCore.cognate_options` and
:meth:`cognate.component_core.ComponentCore.cognate_configure` methods via the
use of the
:meth:`cognate.component_core.ComponentCore.__invoke_method_on_children__`.
This effectively calls the *cognate_options* and *cognate_configure* methods
on all primary base classes that derive from *ComponentCore*.

.. _configuration_management_and_initialization:

Configuration Management and Initialization
=============================================

*ComponentCore* helps out with configuration management and initialization of
runtime services. it does this by creating a configuration loop. Utilizing the
:ref:`hello_world_class` as an example.

.. _command_line_option_construction:

Command Line Option Construction
---------------------------------

*ComponentCore* provides the means for command line construction to inheriting
classes. This is achieved by the ingestion of command line options through
invocation of *configure_option* method on the chain of ancestor classes that
declare the *configuration_option* method.

The net effect is that *ComponentCore* will collect all of the configuration
options in one bundle, and manage them as a unified instance configuration.
This allows for the centralization of common options and the attending code.

For more detail on this feature, be sure to check out
:meth:`~cognate.ComponentCore._execute_configuration`.

.. _logging_and_log_configuration:

Logging and Log Configuration
------------------------------

*ComponentCore* supports console and file output. In addition *ComponentCore*
supports
the four basic log levels: `debug`,`info`,`warning`,`error`.

The configuration logging options are:

  :arg: --log_level {debug,info,warning,error}

    Set the log level for the log output.

  :arg: --log_path LOG_PATH

    Set the path for log output. The default file created is
    "<log_path>/<app_name>.log". If the path ends with a ".log"
    extension, then the path be a target file.

  :arg: --verbose

    Enable verbose log output to console. Useful for debugging.

*ComponentCore* log configuration takes advantage of the
:ref:`dynamic_service_naming` for log file naming, as well as in log name
output.

For example::

  2012-12-02 03:26:03,030 - <name> - INFO - Logging configured for:
  VentilatorWindmill

The <name> value will be assigned by default to the instance class utilizing
*ComponentCore*, but will be overridden by the use of the '--app_name <name>'
option.


.. _dynamic_service_naming:

Dynamic Service Naming
------------------------

*ComponentCore* provides a mechanism to allow for dynamic naming of
progenitor class
service instances. This is achieved through the use of the '--app_name <name>'
option. When this flag is set *ComponentCore* will set the `self.name`
instance to
the designated value. In addition, *ComponentCore* will set the `self.name_set`
flag to `True`.

By default *ComponentCore* will set the name of the instance class.

The assigned name can effect the output log name, as well as name of the log
output. The use of `self.name` may also effect features from other progenitor
classes that take advantage of *ComponentCore* dynamic naming.

Child classes of ComponentCore can access the configured service app name
through
`self.app_name`.
