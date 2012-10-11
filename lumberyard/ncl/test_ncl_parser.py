# -*- coding: utf-8 -*-
"""
test_parser.py

unit tests for parser
"""
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from ncl_parser import parse_ncl_string, InvalidNCLString

_test_cases = [
    ("*** invalid string ***", "exception"),
]

class TestBucket(unittest.TestCase):
    """
    test the ncl parser with various strings
    """
    def test_all_test_cases(self):
        for test_string, expected_result in _test_cases:
            if expected_result == "exception":
                self.assertRaises(InvalidNCLString, 
                                  parse_ncl_string, 
                                  test_string)
            else:
                result = parse_ncl_string(test_string)
                self.assertEqual(result, 
                                 expected_result, 
                                 (test_string, result)) 

if __name__ == "__main__":
    unittest.main()

