==========================================
Cognate - Related to the Same Common Root
==========================================

*Cognate* is a package to make development of configurable component services
easy to implement. Configurable here pertains to options settings, logging
configuration, and service naming. Component here means the creation of isolated
bits of code with well defined configuration and interfaces.

To be less cryptic, lets demonstrate the *HelloWorld* example. To begin,
create a component service class::

    from cognate.component_core import ComponentCore
    import sys

    class HelloWorld(ComponentCore):
        def __init__(self, name='World', **kwargs):
            self.name = name

            super(HelloWorld, self).__init__(**kwargs)

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

The ``HelloWorld`` class defines a property ``name`` that will be used to
construct the log output during execution of the ``run`` method. The
``cognate_options`` method is used to declare any attributes of the service
utilizing an **argparse.ArgumentParser** instance passed as the ``arg_parser``
parameter. Child classes of *ComponentCore* can use all the features of the
python **argparse.ArgumentParser**, and these will be automatically mapped to
attributes of the same name for a given service instance.

With the ``HelloWorld`` component service above, the complete service features
can be demonstrated with the listing of the service usage. As in::

    /cognate > python example/hello_world.py -h
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

Note how *ComponentCore* adds the features for app naming, log configuration
and output. Also folded in, is the configuration option for the *name*
that is provided by the ``HelloWorld`` class.

Simply running ``python example/helloworld.py`` will cause silent execution as
default *log_level* is *error*. In addition, the logging output is silent,
as the *verbose* option is *False*.

To demonstrate *HelloWorld* with output, run::

    /cognate > python example/hello_world.py  --verbose --log_level info
    MainThread:2014-08-02 13:30:57,988 -HelloWorld - INFO -- Logging configured for: HelloWorld
    MainThread:2014-08-02 13:30:57,988 -HelloWorld - INFO -- Component service configuration complete with argv: Namespace(log_level='info', log_path=None, name='World', service_name='HelloWorld', verbose=True)
    MainThread:2014-08-02 13:30:57,989 -HelloWorld - INFO -- Hello World

Note the setting of the `verbose` flag to enable logging output to console.
In addition, the `log_level` flag is set to info, to enable logging output of
the *HelloWorld* execution.

The *ComponentCore* will map arg_parser defined options to an attribute name
and apply that value to the service instance.  In the *HelloWorld* example,
the arg_parser `--name` option is mapped to the `self.name` attribute. The
net effect is to allow configuration of the service via command line args,
as in::

    /cognate > python example/hello_world.py  --verbose --log_level info --name Dog
    MainThread:2014-08-02 13:30:16,022 -HelloWorld - INFO -- Logging configured for: HelloWorld
    MainThread:2014-08-02 13:30:16,022 -HelloWorld - INFO -- Component service configuration complete with argv: Namespace(log_level='info', log_path=None, name='Dog', service_name='HelloWorld', verbose=True)
    MainThread:2014-08-02 13:30:16,022 -HelloWorld - INFO -- Hello Dog

A benefit to defining component services with *ComponentCore* is the ability
to  utilize the component as an instance. For example::

    from hello_world import HelloWorld

    # Configure with argv string
    argv = '--verbose --log_level info --service_name CatWorld --name Cat'
    hello_cat = HelloWorld(argv=argv)

    # Configure with parameters
    hello_dog = HelloWorld(verbose=True,
                           log_level='info',
                           service_name='DogWorld',
                           name='Dog')

    hello_cat.run()
    hello_dog.run()

The script above demonstrates how the component service can be configured
utilizing a string passed via the `argv` parameter, as well as being
instantiated via direct parameter passing. The script above would give output
such as::

    /cognate > python example/hello_script.py
    MainThread:2014-08-02 13:32:11,237 -CatWorld - INFO -- Logging configured for: CatWorld
    MainThread:2014-08-02 13:32:11,237 -CatWorld - INFO -- Component service configuration complete with argv: Namespace(log_level='info', log_path=None, name='Cat', service_name='CatWorld', verbose=True)
    MainThread:2014-08-02 13:32:11,237 -DogWorld - INFO -- Logging configured for: DogWorld
    MainThread:2014-08-02 13:32:11,237 -DogWorld - INFO -- Component service configuration complete with argv: Namespace(log_level='info', log_path=None, name='Dog', service_name='DogWorld', verbose=True)
    MainThread:2014-08-02 13:32:11,238 -CatWorld - INFO -- Hello Cat
    MainThread:2014-08-02 13:32:11,238 -DogWorld - INFO -- Hello Dog

The ability to treat component services as isolated code with well defined
interfaces make reuse of components much easier, as well as usage in
multi-threaded environments.

Be sure to checkout :ref:`getting-started-with-cognate` to delve into all the
goodness.

**Share and Enjoy**


Indices and Tables
===================

 * :ref:`genindex`
 * :ref:`modindex`
 * :ref:`search`
