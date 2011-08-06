# -*- coding: utf-8 -*-
"""
http_util.py

utility functions for connecting with $NAME via HTTP
"""
import os
import time
import urllib

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


