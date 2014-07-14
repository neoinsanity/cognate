from logging import DEBUG, INFO, WARNING
from os import path, remove

from cognate_test_case import CognateTestCase, TEST_OUT

from cognate.component_core import ComponentCore


class TestComponentCore(CognateTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_default_file_logging(self):

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
