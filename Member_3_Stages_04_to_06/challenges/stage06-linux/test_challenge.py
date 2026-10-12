#!/usr/bin/env python3
import unittest
from check_permissions import assess

class LabPolicyParserTests(unittest.TestCase):
    def test_detect_sample_rule(self):
        self.assertEqual(len(assess('    (root) NOPASSWD: /usr/bin/find\n')),1)
    def test_not_a_false_positive(self):
        self.assertEqual(assess('    (root) NOPASSWD: /usr/bin/ls\n'),[])
if __name__=='__main__':unittest.main(verbosity=2)
