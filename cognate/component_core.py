"""The *ComponentCore* class provides the means to add some basic features for
construction of service modules.
"""
import argparse
import logging
from logging.handlers import WatchedFileHandler
import os
import shlex
import sys

class ComponentCore(object):
    """The *ComponentCore* class provides configuration services for components.

    :Command Line Usage:

    *ComponentCore* supports the following command line options::

        usage:  [-h] [--service_name SERVICE_NAME]
                [--log_level {debug,info,warn,error}]
                [--log_path LOG_PATH] [--verbose]

        optional arguments:
          -h, --help            show this help message and exit
          --service_name SERVICE_NAME
                                This will set the name for the current instance.
                                This will be reflected in the log output.
                                (default:ComponentCore)
          --log_level {debug,info,warn,error}
                                Set the log level for the log output.
                                (default: error)
          --log_path LOG_PATH   Set the path for log output. The default file
                                created is "<log_path>/<service_name>.log". If
                                the path ends with a ".log" extension,
                                then the path be a target file.
                                (default: None)
          --verbose             Enable verbose log output to console. Useful for
                                debugging. (default: False)

    .. note:: *ComponentCore* will cause the application to exit if the ``-h``
      or ``--help`` cognate_configure arguments are one of the options. In
      addition to exiting, *ComponentCore* will display the command line help
      message.

    Any classes sharing a base class chain with *ComponentCore* may implement:

      - cognate_options(self, arg_parser)

      - cognate_configure(self, args)

    This method operates by taking an options list in *argparse* format and
    creates an argument list. The argument list is generated by processing
    *argv* through *argparse.ArgumentParser*. The resultant arguments are
    applied to `self`.

    .. note: File name sniffing.

    The argument list that is obtained from *sys.argv* will have the path of
    the invoking python file. For purposes of *ComponentCore* configuration this
    argument is irrelevant. The *_execute_configuration* method will detect
    for this state and removes the path argument.
    """
    # A map for setting ``logging`` level upon log configuration during
    # invocation of :meth:`~cognate.ComponentCore._
    LOG_LEVEL_MAP = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'error': logging.ERROR,
    }

    def __init__(self,
                 argv=None,
                 log_level='error',
                 log_path=None,
                 service_name=None,
                 verbose=False):
        """ Initializes the ComponentCore support infrastructure.

        :param argv: An array of arguments of the form
                     ['--verbose', '--name', 'my_name', ...] or an argument
                     string of the form '--verboxe --name my_name'.
        :type argv: str, list<str>
        :param log_level: The log level setting. The options for leg_level are:
            debug, info, warn, error. The default is error.
        :type log_level: str
        :param log_path: 'Set the path for log output. The default file created
            is "<log_path>/<service_name>.log". If the path ends with a ".log"
            extension, then the path be a target file.'
        :type log_path: str
        :param service_name: This will set the name for the current instance.
            This will be reflected in the log output.'
        :type service_name: str
        :param verbose: Enable verbose log output to console. Defaults to False.
        :type verbose: bool
        :return: `ComponentCore` child instance

        A default ComponentCore will assume the name of the instantiating
        class. In
        addition, it will not consider the name to have been set.

        >>> class Foo(ComponentCore):
        ...     def __init__(self, **kwargs):
        ...         ComponentCore.__init__(self, **kwargs)
        >>> foo = Foo()
        >>> assert foo.service_name == 'Foo'
        >>> assert foo.service_name_set == False
        >>> assert foo.log_level == logging.ERROR
        >>> assert foo.log_path == None
        >>> assert foo.verbose == False

        A ComponentCore can be configured utilizing the an array style
        argument list.

        >>> bar = ComponentCore(['--service_name','Bar','--log_level','debug'])
        >>> assert bar.service_name == 'Bar'
        >>> assert bar.service_name_set == True
        >>> assert bar.log_level == logging.DEBUG
        >>> assert bar.log_path == None
        >>> assert bar.verbose == False

        In addition, the ComponentCore can be configured from a string.

        >>> dude = ComponentCore(
        ...   '--service_name Dude --log_level info')
        >>> assert dude
        >>> assert dude.service_name == 'Dude'
        >>> assert dude.service_name_set == True
        >>> assert dude.log_level == logging.INFO
        >>> assert dude.verbose == False
        """
        # Current log level, set to logging.DEBUG, INFO, WARNING, OR ERROR at
        # runtime.
        self.log_level = log_level
        # The path to the log file, if one is set.
        self.log_path = log_path
        # Set to true if the '--app-name' is utilized
        self.service_name_set = False
        # The name of the application. Overridden by '--service_name' option.
        if service_name is None:
            self.service_name = self.__class__.__name__
        else:
            self.service_name = service_name
            self.service_name_set = True
        # Set to true if '--verbose' option flag is utilized
        self.verbose = verbose

        # : The log attribute to use for logging message
        self.log = None
        # helper to allow using string for configuration
        if argv is not None and isinstance(argv, basestring):
            argv = shlex.split(argv)  # convert string to args style list

        # determine if a name has been set for the instantiating class instance
        # from command line
        if argv and '--service_name' in argv:
            self.service_name_set = True

        self._execute_configuration(argv)

    def cognate_options(self, arg_parser):
        """This method will be called to get the *ComponentCore* configuration
        options.

        :param arg_parser: An *ArgumentParser* instance to add configuration
            options.
        :type arg_parser: argparse.ArgumentParser
        :return: None
        """
        arg_parser.add_argument('--service_name',
                                default=self.service_name,
                                help='This will set the name for the current '
                                     'instance. This will be reflected in the '
                                     'log output.')
        arg_parser.add_argument('--log_level',
                                default=self.log_level,
                                choices=['debug', 'info', 'warn', 'error'],
                                help='Set the log level for the log output.')
        arg_parser.add_argument('--log_path',
                                default=self.log_path,
                                help='Set the path for log output. The default '
                                     'file created is '
                                     '"<log_path>/<service_name>.log". If the '
                                     'path ends with a ".log" extension, then '
                                     'the path be a target file.')
        arg_parser.add_argument('--verbose',
                                action='store_true',
                                default=self.verbose,
                                help='Enable verbose log output to console. '
                                     'Useful for debugging.')

    def cognate_configure(self, args):
        """ This method is called by *ComponentCore* during instance
        initialization.

        :param args: An object with configuration properties.
        :type args: object
        :return: None

        .. note:: Properties set to `self`.

        In addition to setting the configuration options to *self*, the *args*
        parameter has the configuration. This should allow for most complex
        configuration scenarios.
        """
        assert args

        self._configure_logging()

    def _configure_logging(self):
        """This method configures the self.log entity for log handling.

        :return: None

        The method will cognate_configure the logging facilities for the
        derive service instance. This includes setting up logging to files
        and console. The configured log will be available to the service
        instance with `self.log`
        """
        self.log_level = ComponentCore.LOG_LEVEL_MAP.get(self.log_level,
                                                         logging.ERROR)

        # if log level is debug, then we add source information to log output
        formatter = logging.Formatter(
            '%(threadName)s:%(asctime)s -%(name)s - %(levelname)s -- %('
            'message)s')
        if self.log_level == logging.DEBUG:
            formatter = logging.Formatter(
                '%(threadName)s:%(asctime)s -%(name)s - %(levelname)s -- '
                '%(pathname)s:%(lineno)d -- %(message)s')

        # assign the windmill instance logger
        self.log = logging.getLogger(self.service_name)
        self.log.setLevel(self.log_level)

        # cognate_configure log file output if necessary
        if self.log_path:
            file_path = self.log_path
            if not self.log_path.endswith('.log'):
                file_path = os.path.join(self.log_path,
                                         self.service_name + '.log')

            file_handler = WatchedFileHandler(file_path)
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
            self.log.addHandler(file_handler)

        # if we are in verbose mode, the we send log output to console
        if self.verbose:
            # add the console logger for verbose mode
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(formatter)
            self.log.addHandler(console_handler)

        self.log.info('Logging configured for: %s', self.service_name)


    def _execute_configuration(self, argv):
        """This method assigns an argument list to attributes assigned to self.

        :param argv: A list of arguments.
        :type argv: list<str>
        :return: None

        This is the work horse method that does the work of invoking
        *configuration_option* and *cognate_configure* methods on progenitor
        classes of *ComponentCore*. In addition it takes the resolved
        arguments from *argparse.ArgumentParser* and assigns them to `self`.

        :Example Usage:

        >>> foo = ComponentCore()
        >>> argv = [
        ... '/Users/neoinsanity/samples/samples/my-argparse/simple_argparse.py',
        ... '--verbose']
        >>> foo._execute_configuration(argv=argv)
        >>> assert foo.verbose == True
        """
        if argv is None:
            argv = []  # just create an empty arg list

        # ensure that sys.argv is not modified in case it was passed.
        if argv is sys.argv:
            argv = list(sys.argv)

        # If this is the command line args directly passed, then we need to
        # remove the first argument which is the python execution command.
        # The first argument is the name of the executing python script.
        if len(argv) > 0 and argv[0].endswith('.py'):
            argv.pop(0)

        # execute configuration_option method on all child classes of
        # ComponentCore to gather all of the runtime options.
        arg_parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.invoke_method_on_children(func_name='cognate_options',
                                        arg_parser=arg_parser)

        # resolve configuration options necessary for runtime execution
        property_list = []
        # noinspection PyProtectedMember
        for action in arg_parser._get_positional_actions():
            property_list.append(action.dest)
            # noinspection PyProtectedMember
        for action in arg_parser._get_optional_actions():
            property_list.append(action.dest)
        property_list.remove('help')  # remove the help option

        args = arg_parser.parse_args(argv)

        # map the properties to attributes assigned to self instance
        copy_attribute_values(source=args,
                              target=self,
                              property_names=property_list)

        # now execute the configuration call on each base class
        # in the class inheritance chain
        self.invoke_method_on_children(func_name='cognate_configure',
                                        args=args)

        self.log.info(
            'Component service configuration complete with argv: %s', args)

    def invoke_method_on_children(self, func_name=None, *args, **kwargs):
        """This helper method will walk the primary base class hierarchy to
        invoke a method if it exists for a given child base class.

        :param func_name: The name of a function to search for invocation.
        :type func_name: str
        :param args: An argument list to pass to the target function.
        :type args: list
        :param kwargs: A dictionary of name/value pairs to pass to the target
            function as named arguments.
        :type kwargs: dict
        :return: None
        :raises ValueError: Thrown if no function name is provided.

        In an effort to explain, assume that a class hierarchy has been defined
        as in the image below:

        .. image:: images/invoke_method_on_children_class_hierarchy.png

        *invoke_method_on_children* will traverse the class hierarchy
        invoking target method *the_func* on each child class. This is different
        from normal python resolution, which will only invoke the first instance
        of the method defined in the class hierarchy, which would be
        *Child3.the_func*.

        .. image:: images/invoke_method_on_children.png

        .. note:: Mind the flow of invocation on the class hierarchy.

        Invocation of target *func_name* is from the *ComponentCore* class
        as the starting point, and the search continuing out toward the final
        ancestor class.

        ::Example Usage:

        To utilize this method, a function name must be provided.

        .. warning:: Beware mistyped method names.

        If a method name is supplied for a method that does not exist,
        the *invoke_method_on_children* will raise no exception.

        >>> foo = ComponentCore()
        >>> foo.invoke_method_on_children()
        Traceback (most recent call last):
        ...
        ValueError: invoke_method_on_children:func_name parameter required
        >>> # Now correctly
        >>> foo.invoke_method_on_children(func_name='the_func')

        In actual usage, declare a *ComponentCore* derived child class with a
        target function. It is possible to have more than one ancestor class
        with the target function defined. The *invoke_method_on_children* will
        execute the function on each of the child classes.

        >>> class Bar(ComponentCore):
        ...   def the_func(self, a_key=None):
        ...     print 'a_key:', a_key
        >>> bar = Bar()

        With an instance of a *AttributeHelper* child class, we can invoke
        the method in two ways, as exampled below.

        >>> # Create a keyword argument dictionary or argument list
        >>> kwargs = {'a_key':'a_value'}
        >>> bar.invoke_method_on_children(func_name='the_func', **kwargs)
        a_key: a_value
        >>> # Simply pass the argument keyword and value
        >>> bar.invoke_method_on_children(
        ...     func_name='the_func', a_key='value')
        a_key: value
        """
        if func_name is None:
            raise ValueError(
                'invoke_method_on_children:func_name parameter required')

        class_stack = []
        base = self.__class__  # The root class in the hierarchy.
        while base is not None and base is not object:
            class_stack.append(base)
            base = base.__base__  # iterate to the next base class

        while len(class_stack) is not 0:
            base = class_stack.pop()
            if func_name in base.__dict__:  # check the func exist on class
                # instance
                func = getattr(base, func_name)
                func(self, *args,
                     **kwargs)  # This is the function getting invoked


def copy_attribute_values(source, target, property_names):
    """Function to copy attributes from a source to a target object.

    This method copies the property values in a given list from a given
    source object to a target source object.

    :param src: The source object that is to be inspected for property
        values.
    :type src: type
    :param target: The target object that will be modified with values found
        in src.
    :type target: type
    :param property_names: List of property names whose values are to be
        copied from source to object.
    :type property_names: list, set
    :rtype: None
    :raises ValueError: If src is None.
    :raises ValueError: If target is None.
    :raises ValueError: If property list is not iterable or None.

    The *copy_attribute_values* method will only copy the values from src
    when a property name is found in the src. In cases where a property
    value is not found in the src object, then no change to the target object is
    made.

    :Example Usage:

    >>> src = type('attr_bag', (object,), dict())
    >>> src.property1 = 1
    >>> src.property2 = 2
    >>> src.property3 = 3
    >>> target = type('attr_bag', (object,), dict())
    >>> property_list = ['property1', 'property2', 'exist_not_property']
    >>> copy_attribute_values(src, target, property_list)
    >>> assert hasattr(target, 'property1')
    >>> assert hasattr(target, 'property2')
    >>> assert not hasattr(target, 'property3')
    >>> assert not hasattr(target, 'exist_not_property')
    """
    if source is None:
        raise ValueError('"source" must be provided.')
    if target is None:
        raise ValueError('"target" must be provided.')
    if property_names is None:
        raise ValueError('"property_list" must be provided.')
    if not hasattr(property_names, '__iter__'):
        raise ValueError(
            '"property_names" must be a sequence type, such as list or set.')

    for property_name in property_names:
        if hasattr(source, property_name):
            setattr(target, property_name, getattr(source, property_name))

