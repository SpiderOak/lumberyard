# -*- coding: utf-8 -*-
"""
You must give nimbus.io 3 items to identify yourself as a valid user:
 * user name
 * authorization key id
 * authorization key

You can have multiple authorization keys, so you must supply the key id to
identify which one you are using.

"""
from collections import namedtuple
import os
import os.path

#: You can create an identity with::
#:   
#:    identity_template(username=<your name>,
#:                      auth_key_id=<your auth key id>,
#:                      auth_key=<your auth key>)
#:
identity_template = namedtuple(
    "Identity", ["user_name", "auth_key_id", "auth_key"]
)

#TODO: locate the identity in the proper place for the platform
_identity_path = os.environ.get('NIMBUSIO_IDENTITY', 
    os.path.expandvars("$HOME/.nimbus.io"))
_user_name_env = "NIMBUSIO_USER_NAME"
_auth_key_id_env = "NIMBUSIO_AUTH_KEY_ID"
_auth_key_env = "NIMBUSIO_AUTH_KEY"

def load_identity_from_environment():
    """
    Identity can come from environment variables:
     * MOTOBOTO_USER_NAME
     * MOTOBOTO_AUTH_KEY_ID
     * MOTOBOTO_AUTH_KEY
    """
    if not _user_name_env in os.environ:
        return None
    if not _auth_key_id_env in os.environ:
        return None
    if not _auth_key_env in os.environ:
        return None

    return identity_template(
        user_name=os.environ[_user_name_env],
        auth_key_id=os.environ[_auth_key_id_env],
        auth_key=os.environ[_auth_key_env]
    )

def load_identity_from_file(path=_identity_path):
    """
    Identity can come from an identity file::

        Username motoboto-test-01
        AuthKeyId 43
        AuthKey oMDMm54A4F5+ukVSSoZTOlDVAIhlywJI+x4lsLjLWfA
    """
    user_name = None
    auth_key_id = None
    auth_key = None

    for line in open(path):
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == "#":
            continue
        key, value = line.split()
        if key.lower() in ["user_name", "username"]:
            user_name = value
        elif key.lower() in ["auth_key_id", "authkeyid"]:
            auth_key_id = value
        elif key.lower() in ["auth_key", "authkey"]:
            auth_key = value

    if user_name == None:
        return None
    if auth_key_id == None:
        return None
    if auth_key == None:
        return None

    return identity_template(
        user_name=user_name,
        auth_key_id=auth_key_id,
        auth_key=auth_key
    )

