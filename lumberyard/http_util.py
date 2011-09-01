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


