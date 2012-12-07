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
    ncl_list_keys, \
    ncl_list_key_versions, \
    ncl_list_key, \
    ncl_archive_key, \
    ncl_retrieve_key, \
    ncl_delete_key, \
    ncl_space_usage

class InvalidNCLString(Exception):
    pass

# detect the basic command skeleton
# TODO: we could allow abbreviations
_command_templates = [
    (ncl_list_collections, re.compile(u"^list collections$", re.UNICODE), ),
    (ncl_list_collection, 
     re.compile(u"^list collection\s(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])$", re.UNICODE), ),
    (ncl_create_collection,
     re.compile(u"^create collection\s(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])\s*(?P<options>.*)$", re.UNICODE), ),
    (ncl_set_collection,
     re.compile(u"set collection\s(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])\s*(?P<options>.*)$", re.UNICODE), ),
    (ncl_delete_collection,
     re.compile(u"delete collection\s(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])", re.UNICODE), ),
    (ncl_list_keys, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])\slist keys\s*(?P<options>.*)$", re.UNICODE), ),
    (ncl_list_key_versions, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])\slist key versions\s(?P<key>\S+)\s*(?P<options>.*)$", re.UNICODE), ),
    (ncl_list_key, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])\slist key\s(?P<key>\S+)\s*(?P<options>.*)$", re.UNICODE), ),
    (ncl_archive_key, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])\sarchive key\s(?P<key>\S+)\s*(?P<paths>.*)$", re.UNICODE), ),
    (ncl_retrieve_key, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])\sretrieve key\s(?P<key>\S+)\s*(?P<options>.*)$", re.UNICODE), ),
    (ncl_delete_key, 
     re.compile(u"^(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])\sdelete key\s(?P<key>\S+)\s*(?P<options>.*)$", re.UNICODE), ),
    (ncl_space_usage, 
     re.compile(u"^space usage\s(?P<collection_name>[a-z0-9][a-z0-9-]*[a-z0-9])\s*(?P<options>.*)$", re.UNICODE), ), ]

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

def _parse_options(option_string):
    option_dict = dict()
    for item in option_string.split():
        option_pair = item.split(u"=")
        if len(option_pair) != 2:
            raise InvalidNCLString("Unparseable option {0}".format(item))
        option_dict[option_pair[0].lower()] = option_pair[1]
    return option_dict

def _build_list_collections(_match_object, _ncl_dict):
    pass

def _build_list_collection(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

def _collection_options(option_string, ncl_dict):
    option_dict = _parse_options(option_string)

    if u"versioning" in option_dict:
        if option_dict["versioning"].lower() == u"true":
            ncl_dict["versioning"] = True
        elif option_dict != u"false":
            raise InvalidNCLString("Unknown versioning {0}".format(ncl_dict))

    if u"access_control" in option_dict:
        ncl_dict["access_control"] = option_dict["access_control"]

def _build_create_collection(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

    _collection_options(match_object.group("options"), ncl_dict)

def _build_set_collection(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

    _collection_options(match_object.group("options"), ncl_dict)
    
def _build_delete_collection(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

def _build_list_keys(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

def _build_list_versions(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

    ncl_dict["key"] = match_object.group("key")

def _build_list_key(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

    ncl_dict["key"] = match_object.group("key")
    
    option_dict = _parse_options(match_object.group("options"))
    if "version" in option_dict:
        ncl_dict["version"] = option_dict["version"]

def _build_archive_key(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

    ncl_dict["key"] = match_object.group("key")
    paths = match_object.group("paths").split()
    if len(paths) > 0:
        ncl_dict["paths"] = paths

def _build_retrieve_key(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

    ncl_dict["key"] = match_object.group("key")
    option_dict = _parse_options(match_object.group("options"))
    if "dest" in option_dict:
        ncl_dict["dest"] = option_dict["dest"]

def _build_delete_key(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

    ncl_dict["key"] = match_object.group("key")

def _build_space_usage(match_object, ncl_dict):
    ncl_dict["collection_name"] = match_object.group("collection_name")
    if not _valid_collection_name(ncl_dict["collection_name"]):
        raise InvalidNCLString("Invalid collection name {0}".format(
            ncl_dict["collection_name"]))

    option_dict = _parse_options(match_object.group("options"))
    if "days" in option_dict:
        ncl_dict["days"] = int(option_dict["days"])

_dispatch_table = {
    ncl_list_collections   : _build_list_collections,
    ncl_list_collection    : _build_list_collection,
    ncl_create_collection  : _build_create_collection,
    ncl_set_collection     : _build_set_collection,
    ncl_delete_collection  : _build_delete_collection,
    ncl_list_keys          : _build_list_keys,
    ncl_list_key_versions  : _build_list_versions,
    ncl_list_key           : _build_list_key,
    ncl_archive_key        : _build_archive_key,
    ncl_retrieve_key       : _build_retrieve_key,
    ncl_delete_key         : _build_delete_key,
    ncl_space_usage        : _build_space_usage,
}

def parse_ncl_string(ncl_string):
    """
    return a well-formed NCL object
    or raise InvalidNCLString
    """
    ncl_dict = {}
    ncl_string.decode("utf-8")

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

