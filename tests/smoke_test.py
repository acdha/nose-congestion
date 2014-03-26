from __future__ import absolute_import, print_function, unicode_literals

import time
import unittest


class SmokeTests(unittest.TestCase):
    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        time.sleep(2)

    def test_universe(self):
        a = 1
        b = 1
        self.assertEqual(a, b)
