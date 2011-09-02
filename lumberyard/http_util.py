# -*- coding: utf-8 -*-
"""
http_util.py

utility functions for connecting with nimbus.io via HTTP
"""
import hashlib
import hmac
import os
import time
import urllib

meta_prefix = "__nimbus_io__"
_host_port = 8088
_default_collection_prefix = "dd"
_reserved_collection_prefix = "rr"

def compute_default_collection_name(username):
    """
    return the name of this customer's default collection
    """
    return "-".join([_default_collection_prefix, username])

def compute_reserved_collection_name(username, collection_name):
    """
    return the decorated name of a reserved collection name
    """
    return "-".join([_reserved_collection_prefix, username, collection_name])

def compute_hostname(collection_name):
    """
    return the DNS hostname for this collection
    """
    hostname = ".".join([collection_name, "nimbus", "io"])
    hostname_with_port = ":".join([hostname, "%s" % _host_port])
    return hostname_with_port

def compute_default_hostname(username):
    """
    return the DNS hostname for this customer's default collection
    """
    return compute_hostname(compute_default_collection_name(username))

def compute_reserved_hostname(username, collection_name):
    """
    return the DNS hostname for one of this customer's reserved collection
    """
    return compute_hostname(
        compute_reserved_collection_name(username, collection_name)
    )

def compute_authentication_string(
    auth_key_id,  auth_key, user_name,  method, timestamp, uri
):
    """
    Compute the authentication hmac sent to the server
    """
    message = "\n".join([user_name, method, str(timestamp), uri])
    hmac_object = hmac.new(
        auth_key,
        message,
        hashlib.sha256
    )
    return "NIMBUS.IO %s:%s" % (auth_key_id, hmac_object.hexdigest(), )

def compute_uri(sub_dir, key=None, **kwargs):
    """
    Create the REST URI sent to the server
    """    
    work_key = (urllib.quote_plus(key) if key is not None else None)
    if work_key is not None:
        path = os.path.join(os.sep, sub_dir, work_key)
    else:
        path = os.path.join(os.sep, sub_dir)
    if len(kwargs) > 0:
        path = "?".join([path, urllib.urlencode(kwargs.items()), ])
    return path

def current_timestamp():
    """
    return the current time as an integer
    """
    return int(time.time())


