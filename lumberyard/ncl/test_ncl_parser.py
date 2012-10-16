# -*- coding: utf-8 -*-
"""
test_parser.py

unit tests for parser
"""
import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from ncl_parser import parse_ncl_string, InvalidNCLString
from commands import \
    ncl_list_collections, \
    ncl_list_collection, \
    ncl_create_collection, \
    ncl_set_collection, \
    ncl_delete_collection, \
    ncl_list_files, \
    ncl_list_file_versions, \
    ncl_list_file, \
    ncl_archive_file, \
    ncl_retrieve_file, \
    ncl_delete_file

_test_cases = [
    ("*** invalid string ***", "exception"),
    ("list collections", {"command" : ncl_list_collections}),
    ("list collection 111111111111111-", "exception"),
    ("list collection aaa", {"command" : ncl_list_collection,
                             "collection_name" : "aaa"}),
    ("create collection 1111--11111111111", "exception"),
    ("create collection aaa", {"command" : ncl_create_collection,
                             "collection_name" : "aaa"}),
    ("create collection aaa versioning=true", 
        {"command" : ncl_create_collection,
         "collection_name" : "aaa",
         "versioning" : True}),
]

class TestBucket(unittest.TestCase):
    """
    test the ncl parser with various strings
    """
    def test_all_test_cases(self):
        for test_string, expected_result in _test_cases:
            print >>sys.stderr, test_string
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

