import os
import unittest

# Standard directory for test file
TEST_OUT = './TEST_OUT/'


class CognateTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # make sure that the test output directory is created
        # it assumes that the current working directory is correct
        d = TEST_OUT
        if not os.path.exists(d):
            os.makedirs(d)
