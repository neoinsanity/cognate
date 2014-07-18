from logging import DEBUG, ERROR, INFO, WARNING
from os import path, remove

from cognate_test_case import CognateTestCase, TEST_OUT

from cognate.component_core import ComponentCore


class TestComponentCoreArgsPassing(CognateTestCase):
    """Test various scenarios for passing args."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simplest_cognate(self):
        class Simplest(ComponentCore):
            pass

        simplest = Simplest(argv=None)
        self.assertIsNotNone(simplest)
        self.assertEqual(simplest.app_name, 'Simplest')
        self.assertEqual(simplest.app_name_set, False)
        self.assertIsNotNone(simplest.log)
        self.assertEqual(simplest.log_level, ERROR)
        self.assertIsNone(simplest.log_path)
        self.assertEqual(simplest.verbose, False)

        argv = ('--app_name Dog --verbose --log_level info --log_path %s' %
                TEST_OUT)
        simplest = Simplest(argv=argv)
        self.assertIsNotNone(simplest)
        self.assertEqual(simplest.app_name, 'Dog')
        self.assertEqual(simplest.app_name_set, True)
        self.assertIsNotNone(simplest.log)
        self.assertEqual(simplest.log_level, INFO)
        self.assertEqual(simplest.log_path, './TEST_OUT/')
        self.assertEqual(simplest.verbose, True)


    def test_positional_args(self):
        """"""

        class PositionalArgs(ComponentCore):
            def cognate_options(self, arg_parser):
                arg_parser.add_argument('file', nargs='?', default='input.dat')

        pos = PositionalArgs(argv=None)
        self.assertIsNotNone(pos)

    def test_optional_args(self):
        pass

    def test_positional_and_optional_args(self):
        pass


class TestComponentCoreLogSetup(CognateTestCase):
    """Test the logging features of the component core."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_default_file_logging(self):
        """Test the default file logging."""
        # The target path to the expected file created by component_core
        log_path = path.join(TEST_OUT, 'ComponentCore.log')
        if path.exists(log_path):
            remove(log_path)

        # create the test subject
        argv = '--log_level info --log_path TEST_OUT'
        component_core = ComponentCore(argv=argv)

        # test to make sure that log file is generated
        self.assertTrue(path.exists(log_path))

        # test to make sure component_core internal state is correct
        self.assertEqual(component_core.log_path, 'TEST_OUT')
        self.assertEqual(component_core.log_level, INFO)

    def test_app_name_file_logging(self):
        """Test overriding file name based on setting app_name."""
        # The target path to the expected file created by component_core
        log_path = path.join(TEST_OUT, 'Dude.log')
        if path.exists(log_path):
            remove(log_path)

        # create the test subject
        argv = '--app_name Dude --log_level debug --log_path TEST_OUT'
        component_core = ComponentCore(argv=argv)

        # test to make sure that log file is generated
        self.assertTrue(path.exists(log_path))

        # test to make sure component_core internal state is correct
        self.assertEqual(component_core.app_name, 'Dude')
        self.assertEqual(component_core.log_path, 'TEST_OUT')
        self.assertEqual(component_core.log_level, DEBUG)

    def test_explicit_log_file(self):
        """Test overriding log file path."""
        # The target path to the log file
        log_path = path.join(TEST_OUT, 'the_file.log')
        if path.exists(log_path):
            remove(log_path)

        # create the test subject
        argv = '--log_level warn --log_path TEST_OUT/the_file.log'
        component_core = ComponentCore(argv=argv)

        # test to make sure that log file is generated
        self.assertTrue(path.exists(log_path))

        # test to make sure component_core internal state is correct
        self.assertEqual(component_core.app_name, 'ComponentCore')
        self.assertEqual('./' + component_core.log_path, log_path)
        self.assertEqual(component_core.log_level, WARNING)
