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
    ncl_list_keys, \
    ncl_list_key_versions, \
    ncl_list_key, \
    ncl_archive_key, \
    ncl_retrieve_key, \
    ncl_delete_key

_test_cases = [
    (u"*** invalid string ***", "exception"),
    (u"list collections", {"command" : ncl_list_collections}),
    (u"list collection 111111111111111-", "exception"),
    (u"list collection aaa", {"command" : ncl_list_collection,
                             "collection_name" : "aaa"}),
    (u"create collection 1111--11111111111", "exception"),
    (u"create collection aaa", {"command" : ncl_create_collection,
                             "collection_name" : "aaa"}),
    (u"create collection aaa versioning=true", 
        {"command" : ncl_create_collection,
         "collection_name" : "aaa",
         "versioning" : True}),
    (u"create collection aaa versioning=true access_control=aaa/bbb", 
        {"command" : ncl_create_collection,
         "collection_name" : "aaa",
         "versioning" : True,
         "access_control" : "aaa/bbb"}),
    (u"set collection aaa versioning=true", 
        {"command" : ncl_set_collection,
         "collection_name" : "aaa",
         "versioning" : True}),
    (u"set collection aaa versioning=true access_control=aaa/bbb", 
        {"command" : ncl_set_collection,
         "collection_name" : "aaa",
         "versioning" : True,
         "access_control" : "aaa/bbb"}),
    (u"delete collection aaa", {"command" : ncl_delete_collection,
                                "collection_name" : "aaa"}),
    (u"xxx list keys", {"command" : ncl_list_keys,
                        "collection_name" : "xxx"}),
    (u"xxx list key versions aaa", {"command" : ncl_list_key_versions,
                                    "collection_name" : "xxx",
                                    "key" : "aaa"}),
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

