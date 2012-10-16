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
_command_templates = [
    (ncl_list_collections, re.compile(u"^list collections$", re.UNICODE), ),
    (ncl_list_collection, 
     re.compile(u"^list collection (?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])$", re.UNICODE), ),
    (ncl_create_collection,
     re.compile(u"^create collection (?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9]).*$", re.UNICODE), ),
    (ncl_set_collection,
     re.compile(u"set collection (?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9]).*$", re.UNICODE), ),
    (ncl_delete_collection,
     re.compile(u"delete collection (?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])", re.UNICODE), ),
    (ncl_list_files, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9]) list files .*$", re.UNICODE), ),
    (ncl_list_file_versions, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9]) list file versions .*$", re.UNICODE), ),
    (ncl_list_file, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9]) list file .*$", re.UNICODE), ),
    (ncl_archive_file, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9]) archive file .*$", re.UNICODE), ),
    (ncl_retrieve_file, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9]) retrieve file .*$", re.UNICODE), ),
    (ncl_delete_file, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9]) delete file .*$", re.UNICODE), ), ]

_collection_name_re = re.compile(r'[a-z0-9][a-z0-9-]*[a-z0-9]$')
_max_collection_name_size = 63

def _valid_collection_name(collection_name):
    """
    return True if the username is valid
    copied from nimbus.io server library
    """
    return len(collection_name) <= _max_collection_name_size \
        and not '--' in collection_name \
        and _collection_name_re.match(collection_name) is not None

def _build_list_collections(match_object, ncl_dict):
    pass

def _build_list_collection(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise In_validNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

def _build_create_collection(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise In_validNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

def _build_set_collection(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise In_validNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

    pass
def _build_delete_collection(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise In_validNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

    pass
def _build_list_files(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise In_validNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

def _build_list_versions(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise In_validNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

def _build_list_file(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise In_validNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

def _build_archive_file(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise In_validNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

def _build_retrieve_file(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise In_validNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

def _build_delete_file(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

_dispatch_table = {
    ncl_list_collections   : _build_list_collections,
    ncl_list_collection    : _build_list_collection,
    ncl_create_collection  : _build_create_collection,
    ncl_set_collection     : _build_set_collection,
    ncl_delete_collection  : _build_delete_collection,
    ncl_list_files         : _build_list_files,
    ncl_list_file_versions : _build_list_versions,
    ncl_list_file          : _build_list_file,
    ncl_archive_file       : _build_archive_file,
    ncl_retrieve_file      : _build_retrieve_file,
    ncl_delete_file        : _build_delete_file,
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

    try:
        build_function = _dispatch_table[command]
    except KeyError:
        raise InvalidNCLString("Unknown command {0}".format(command))

    try:
        build_function(match_object, ncl_dict)
    except InvalidNCLString:
        raise
    except Exception, instance:
        raise InvalidNCLString("Exception during parsing {0}".format(instance))

    return ncl_dict

