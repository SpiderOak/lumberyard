# -*- coding: utf-8 -*-
"""
ncl_main.py

main program for nimbusio command lnaguage
"""
from __future__ import print_function
import argparse
import json
import logging
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import sys


from lumberyard.http_connection import HTTPConnection, \
        UnAuthHTTPConnection, \
        LumberyardHTTPError

from lumberyard.http_util import compute_default_hostname, \
        compute_collection_hostname, \
        compute_default_collection_name, \
        compute_uri

from identity import load_identity_from_environment, \
    load_identity_from_file
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
    ncl_delete_key, \
    ncl_space_usage

class NCLError(Exception):
    pass
class InvalidIdentity(NCLError):
    pass
class NCLNotImplemented(NCLError):
    pass
class NCLErrorResult(NCLError):
    pass

_max_keys = 1000
_read_buffer_size = 64 * 1024

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
    parser.add_argument("residue", type=str, nargs="+", 
                        help="a ncl comman on the commandline")

    return parser.parse_args()

def _load_identity(args):
    log = logging
    if args.identity_file is not None:
        try:
            identity = load_identity_from_file(args.identity_file)
        except Exception:
            instance = sys.exc_info()[1]
            raise InvalidIdentity("unable to load {0}".format(
                args.identity_file))
        if identity is None:
            raise InvalidIdentity("unable to parse {0}".format(
                args.identity_file))
        return identity

    # TODO: we could get individual identity elements from the command line

    return load_identity_from_environment()

def _list_collections(args, identity, ncl_dict):
    method = "GET"

    if identity is None:
        raise InvalidIdentity("Must have identity to list collections")

    http_connection = HTTPConnection(compute_default_hostname(),
                                     identity.user_name,
                                     identity.auth_key,
                                     identity.auth_key_id)
    path = "/".join(["customers", identity.user_name, "collections"])
    uri = compute_uri(path)

    response = http_connection.request(method, uri, body=None)
        
    data = response.read()
    http_connection.close()
    collection_list = json.loads(data)
    # TODO: add an option for verbose list
    for entry in collection_list:
        print(entry["name"])

def _list_collection(args, identity, ncl_dict):
    method = "GET"

    http_connection = HTTPConnection(compute_default_hostname(),
                                     identity.user_name,
                                     identity.auth_key,
                                     identity.auth_key_id)
    path = "/".join(["customers", 
                     identity.user_name, 
                     "collections",
                     ncl_dict["collection_name"]])
    uri = compute_uri(path)

    response = http_connection.request(method, uri, body=None)
        
    data = response.read()
    http_connection.close()
    result = json.loads(data)
    print(str(result))

def _create_collection(args, identity, ncl_dict):
    raise NCLNotImplemented("_create_collection")

def _set_collection(args, identity, ncl_dict):
    raise NCLNotImplemented("_set_collection")

def _delete_collectio0n(args, identity, ncl_dict):
    raise NCLNotImplemented("_delete_collection")

def _list_keys(args, identity, ncl_dict):
    method = "GET"

    hostname = compute_collection_hostname(ncl_dict["collection_name"])
    if identity is None:
        http_connection = UnAuthHTTPConnection(hostname)
    else:
        http_connection = HTTPConnection(hostname,
                                         identity.user_name,
                                         identity.auth_key,
                                         identity.auth_key_id)

    kwargs = {
        "max_keys" : _max_keys,
    }
    if "prefix" in ncl_dict and ncl_dict["prefix"] != "" and \
        ncl_dict["prefix"] is not None: 
        kwargs["prefix"] = ncl_dict["prefix"]
    if "marker" in ncl_dict and ncl_dict["marker"] != "" and \
        ncl_dict["marker"] is not None: 
        kwargs["marker"] = ncl_dict["marker"]
    if "delimiter" in ncl_dict and ncl_dict["delimiter"] != "" and \
        ncl_dict["delimiter"] is not None: 
        kwargs["delimiter"] = ncl_dict["delimiter"]

    uri = compute_uri("data/", **kwargs)

    response = http_connection.request(method, uri)
    
    data = response.read()
    http_connection.close()
    data_dict = json.loads(data)

    if "key_data" in data_dict:
        for key_entry in data_dict["key_data"]:
            print(key_entry["key"])
    elif "prefixes" in data_dict:
        for prefix in data_dict["prefixes"]:
            print(prefix)
    else:
        raise ValueError("Unexpected return value %s" % (data_dict, ))

def _list_key_versions(args, identity, ncl_dict):
    raise NCLNotImplemented("_list_key_versions")

def _list_key(args, identity, ncl_dict):
    raise NCLNotImplemented("_list_key")

def _archive_key(args, identity, ncl_dict):
    raise NCLNotImplemented("_archive_key")

def _retrieve_key(args, identity, ncl_dict):
    method = "GET"

    hostname = compute_collection_hostname(ncl_dict["collection_name"])
    if identity is None:
        http_connection = UnAuthHTTPConnection(hostname)
    else:
        http_connection = HTTPConnection(hostname,
                                         identity.user_name,
                                         identity.auth_key,
                                         identity.auth_key_id)

    kwargs = {
    }

    uri = compute_uri("data", ncl_dict["key"], **kwargs)

    response = http_connection.request(method, 
                                       uri, 
                                       body=None)

    while True:
        data = response.read(_read_buffer_size)
        if len(data) == 0:
            break
        sys.stdout.write(data)

    http_connection.close()

def _delete_key(args, identity, ncl_dict):
    raise NCLNotImplemented("_delete_key")

def _space_usage(args, identity, ncl_dict):
    method = "GET"

    if identity is None:
        raise InvalidIdentity("Must have identity to retrieve space usage")

    http_connection = HTTPConnection(compute_default_hostname(),
                                     identity.user_name,
                                     identity.auth_key,
                                     identity.auth_key_id)

    kwargs = {"action" : "space_usage"}
    if "days" in ncl_dict:
        kwargs["days_of_history"] = ncl_dict["days"]

    path = "/".join(["customers", 
                     identity.user_name, 
                     "collections",
                     ncl_dict["collection_name"]])
    uri = compute_uri(path, **kwargs)

    response = http_connection.request(method, uri, body=None)
        
    data = response.read()
    http_connection.close()
    result = json.loads(data)

    if not result["success"]:
        raise NCLErrorResult(result["error_message"])

    print()
    for day_entry in result["operational_stats"]:
        print(day_entry["day"])
        if day_entry["archive_success"] != 0:
            print("{0:8} archive success".format(day_entry["archive_success"]))
            print("{0:8} archive bytes".format(day_entry["success_bytes_in"]))
        if day_entry["retrieve_success"] != 0:
            print("{0:8} retrieve success".format(day_entry["retrieve_success"]))
            print("{0:8} retrieve bytes".format(day_entry["success_bytes_out"]))
        if day_entry["delete_success"] != 0:
            print("{0:8} delete success".format(day_entry["delete_success"]))
        if day_entry["listmatch_success"] != 0:
            print("{0:8} listmatch success".format(day_entry["listmatch_success"]))

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
    ncl_delete_key          : _delete_key,
    ncl_space_usage         : _space_usage}

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
    except InvalidIdentity:
        instance = sys.exc_info()[1]
        log.error("invalid identity: {0}".format(instance))
        return 1

    if len(args.residue) > 0:
        input_file = StringIO(" ".join(args.residue))
    else:
        input_file = sys.stdin

    for line in input_file:
        try:
            ncl_dict = parse_ncl_string(line)
            _dispatch_table[ncl_dict["command"]](args, identity, ncl_dict)
        except InvalidNCLString:
            instance = sys.exc_info()[1]
            log.error(str(instance))
            return 1
        except NCLErrorResult:
            instance = sys.exc_info()[1]
            log.error(str(instance))
            return 1
        except InvalidIdentity:
            instance = sys.exc_info()[1]
            log.error(str(instance))
            return 1 
        except LumberyardHTTPError:
            instance = sys.exc_info()[1]
            log.error(str(instance))
            return 1 
        except Exception:
            instance = sys.exc_info()[1]
            log.exception(line)
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())

