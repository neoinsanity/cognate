from logging import DEBUG, ERROR, INFO, WARNING
from os import path, remove
from unittest import TestCase

from cognate_test_case import CognateTestCase, TEST_OUT

from cognate import component_core
from cognate.component_core import ComponentCore


class AttributeHelperTestCase(TestCase):
    def test_copy_attribute_values(self):
        """Ensure copy_attribute_value functionality and error handling."""
        src_property_bag = type('attr_bag', (object,), dict())
        src_property_bag.prop1 = 'value 1'
        src_property_bag.prop2 = 'value 2'
        src_property_bag.prop3 = 'value 3'
        src_property_bag.prop4 = 'value 4'
        trgt_property_bag = type('attr_bag', (object,), dict())
        trgt_property_bag.prop2 = 'another 2'
        trgt_property_bag.prop3 = 'another 3'
        property_names = {'prop1', 'prop3'}

        self.assertRaisesRegexp(
            ValueError,
            '"source" must be provided.',
            component_core.copy_attribute_values,
            None, trgt_property_bag, property_names)

        self.assertRaisesRegexp(
            ValueError,
            '"target" must be provided.',
            component_core.copy_attribute_values,
            src_property_bag, None, property_names)

        self.assertRaisesRegexp(
            ValueError,
            '"property_list" must be provided.',
            component_core.copy_attribute_values,
            src_property_bag, trgt_property_bag, None)

        self.assertRaisesRegexp(
            ValueError,
            '"property_names" must be a sequence type, such as list or set.',
            component_core.copy_attribute_values,
            src_property_bag, trgt_property_bag, 'Not a sequence')

        self.assertFalse(hasattr(trgt_property_bag, 'prop1'))
        self.assertEqual(trgt_property_bag.prop2, 'another 2')
        self.assertEqual(trgt_property_bag.prop3, 'another 3')
        self.assertFalse(hasattr(trgt_property_bag, 'prop4'))
        component_core.copy_attribute_values(
            src_property_bag, trgt_property_bag, property_names)
        self.assertEqual(trgt_property_bag.prop1, 'value 1')
        self.assertEqual(trgt_property_bag.prop2, 'another 2')
        self.assertEqual(trgt_property_bag.prop3, 'value 3')
        self.assertFalse(hasattr(trgt_property_bag, 'prop4'))


class TestComponentCoreArgsPassing(CognateTestCase):
    """Test various scenarios for passing args."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simplest_cognate(self):
        """Most basic component test configuration."""

        class Simplest(ComponentCore):
            pass

        simplest = Simplest(argv=None)
        self.assertIsNotNone(simplest)
        self.assertEqual(simplest.service_name, 'Simplest')
        self.assertEqual(simplest.service_name_set, False)
        self.assertIsNotNone(simplest.log)
        self.assertEqual(simplest.log_level, ERROR)
        self.assertIsNone(simplest.log_path)
        self.assertEqual(simplest.verbose, False)

        argv = ('--service_name Dog --verbose --log_level info --log_path %s' %
                TEST_OUT)
        simplest = Simplest(argv=argv)
        self.assertIsNotNone(simplest)
        self.assertEqual(simplest.service_name, 'Dog')
        self.assertEqual(simplest.service_name_set, True)
        self.assertIsNotNone(simplest.log)
        self.assertEqual(simplest.log_level, INFO)
        self.assertEqual(simplest.log_path, './TEST_OUT/')
        self.assertEqual(simplest.verbose, True)


    def test_positional_args(self):
        """Ensure positional argument configuration."""

        class PositionalArgs(ComponentCore):
            def cognate_options(self, arg_parser):
                arg_parser.add_argument('file', nargs='?', default='input.dat')

        pos = PositionalArgs(argv=None)
        self.assertIsNotNone(pos)
        self.assertEqual(pos.file, 'input.dat')

        argv = ['output.dat']
        pos = PositionalArgs(argv=argv)
        self.assertIsNotNone(pos)
        self.assertEqual(pos.file, 'output.dat')

    def test_optional_args(self):
        """Ensure optional argument configuration."""

        class OptionalArgs(ComponentCore):
            def cognate_options(self, arg_parser):
                arg_parser.add_argument('-f', '--file', default='input.dat')

        opt = OptionalArgs(argv=None)
        self.assertIsNotNone(opt)
        self.assertEqual(opt.file, 'input.dat')

        argv = '-f output.dat'
        opt = OptionalArgs(argv=argv)
        self.assertIsNotNone(opt)
        self.assertEqual(opt.file, 'output.dat')

    def test_positional_and_optional_args(self):
        """Ensure combo of postional and optional argument configuration."""

        class ComboArgs(ComponentCore):
            def cognate_options(self, arg_parser):
                arg_parser.add_argument('input_file', nargs='?',
                                        default='input.dat')
                arg_parser.add_argument('--output_file')

        combo = ComboArgs(argv=None)
        self.assertIsNotNone(combo)
        self.assertEqual(combo.input_file, 'input.dat')
        self.assertIsNone(combo.output_file)

        argv = 'input.txt --output_file output.txt'
        combo = ComboArgs(argv=argv)
        self.assertIsNotNone(combo)
        self.assertEqual(combo.input_file, 'input.txt')
        self.assertEqual(combo.output_file, 'output.txt')


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

    def test_service_name_file_logging(self):
        """Test overriding file name based on setting service_name."""
        # The target path to the expected file created by component_core
        log_path = path.join(TEST_OUT, 'Dude.log')
        if path.exists(log_path):
            remove(log_path)

        # create the test subject
        argv = '--service_name Dude --log_level debug --log_path TEST_OUT'
        component_core = ComponentCore(argv=argv)

        # test to make sure that log file is generated
        self.assertTrue(path.exists(log_path))

        # test to make sure component_core internal state is correct
        self.assertEqual(component_core.service_name, 'Dude')
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
        self.assertEqual(component_core.service_name, 'ComponentCore')
        self.assertEqual('./' + component_core.log_path, log_path)
        self.assertEqual(component_core.log_level, WARNING)
