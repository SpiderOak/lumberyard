# -*- coding: utf-8 -*-
"""
ncl_main.py

main program for nimbusio command lnaguage
"""
import argparse
import logging
import sys

from lumberyard.http_connection import HTTPConnection, \
        UnAuthHTTPConnection, \
        LumberyardHTTPError

from identity import load_identity_from_environment, load_identity_from_file

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

class InvalidIdentity(Exception):
    pass

_log_format = '%(asctime)s %(name)-12s: %(levelname)-8s %(message)s'
def _initialize_logging():
    """
    Initialize logging to stderr
    Intended for reporting errors
    """
    log_level = logging.WARN
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(log_level)
    formatter = logging.Formatter(_log_format)
    formatter.datefmt = '%H:%M:%S'
    console.setFormatter(formatter)
    logging.root.addHandler(console)
    logging.root.setLevel(log_level)

def _parse_commandline():
    parser = argparse.ArgumentParser(description="Nimbus.io Command Language")
    parser.add_argument("-i", "--identity-file", type=str, default=None,
                        help="path to a nimbusio identity file")

    return parser.parse_args()

def _load_identity(args):
    log = logging
    if args.identity_file is not None:
        try:
            identity = load_identity_from_file(args.identity_file)
        except Exception, instance:
            raise InvalidIdentity("unable to load {0} {1}".format(
                args.identity_file, instance))
        if identity is None:
            raise InvalidIdentity("unable to parse {0}".format(
                args.identity_file))
        return identity

    # TODO: we could get individual identity elements from the command line

    return load_identity_from_environment()

def _list_collections(args, indentity, ncl_dict):
    pass

def _list_collection(args, indentity, ncl_dict):
    pass

def _create_collection(args, indentity, ncl_dict):
    pass

def _set_collection(args, indentity, ncl_dict):
    pass

def _delete_collectio0n(args, indentity, ncl_dict):
    pass

def _list_keys(args, indentity, ncl_dict):
    pass

def _list_key_versions(args, indentity, ncl_dict):
    pass

def _list_key(args, indentity, ncl_dict):
    pass

def _archive_key(args, indentity, ncl_dict):
    pass

def _retrieve_key(args, indentity, ncl_dict):
    pass

def _delete_key(args, identity, ncl_dict):
    pass

_dispatch_table = {
    ncl_list_collections    : _list_collections,
    ncl_list_collection     : _list_collection,
    ncl_create_collection   : _create_collection,
    ncl_set_collection      : _set_collection,
    ncl_delete_collection   : _delete_collectio0n,
    ncl_list_keys           : _list_keys,
    ncl_list_key_versions   : _list_key_versions,
    ncl_list_key            : _list_key,
    ncl_archive_key         : _archive_key,
    ncl_retrieve_key        : _retrieve_key,
    ncl_delete_key          : _delete_key}

def main():
    """
    main entry point
    returns 0 on normal termination
    """
    _initialize_logging()
    log = logging.getLogger("main")
    args = _parse_commandline()

    try:
        identity = _load_identity(args)
    except InvalidIdentity, instance:
        log.error("invalid identity: {0}".format(instance))
        return 1

    for line in sys.stdin:
        try:
            ncl_dict = parse_ncl_string(line)
            _dispatch_table[ncl_dict["command"]](args, identity, ncl_dict)
        except InvalidNCLString, instance:
            log.error(str(instance))
            return 1
        except Exception, instance:
            log.exception(line)
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())

