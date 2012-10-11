# -*- coding: utf-8 -*-
"""
parser.py 

parse strings of ncl into command structures
"""
import re

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

class InvalidNCLString(Exception):
    pass

# detect the basic command skeleton
# TODO: we could allow abbreviations
_command_templates = {
    (ncl_list_collections, re.compile(u"^list collections$", re.UNICODE), ),
    (ncl_list_collection, 
     re.compile(u"^list collection (?P<collection_name>\w+)$", re.UNICODE), ),
    (ncl_create_collection,
     re.compile(u"^create collection (?P<collection_name>\w+).*$", re.UNICODE), ),
    (ncl_set_collection,
     re.compile(u"set collection (?P<collection_name>\w+).*$", re.UNICODE), ),
    (ncl_delete_collection,
     re.compile(u"delete collection (?P<collection_name>\w+)", re.UNICODE), ),
    (ncl_list_files, 
     re.compile(u"^(?P<collection_name>\w+) list files .*$", re.UNICODE), ),
    (ncl_list_file_versions, 
     re.compile(u"^(?P<collection_name>\w+) list file versions .*$", re.UNICODE), ),
    (ncl_list_file, 
     re.compile(u"^(?P<collection_name>\w+) list file .*$", re.UNICODE), ),
    (ncl_archive_file, 
     re.compile(u"^(?P<collection_name>\w+) archive file .*$", re.UNICODE), ),
    (ncl_retrieve_file, 
     re.compile(u"^(?P<collection_name>\w+) retrieve file .*$", re.UNICODE), ),
    (ncl_delete_file, 
     re.compile(u"^(?P<collection_name>\w+) delete file .*$", re.UNICODE), ),
}

def parse_ncl_string(ncl_string):
    """
    return a well-formed NCL object
    or raise InvalidNCLString
    """
    ncl_dict = {}
    ncl_string.decode("utf-8")
    tokens = ncl_string.split()

    # first identify the command
    ncl_dict["command"] = None
    match_object = None
    for command, command_template in _command_templates:
        match_object = command_template.match(ncl_string)
        if match_object is not None:
            ncl_dict["command"] = command
            break

    if match_object is None:
        raise InvalidNCLString("Unable to recognize a command")

    return ncl_dict
