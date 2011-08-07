# -*- coding: utf-8 -*-
"""
HTTPConnection.py

$NAME wrapper for httplib.HTTPConnection
"""
import hashlib
import hmac
import httplib
import logging

from lumberyard.http_util import current_timestamp

class HTTPRequestError(Exception):
    def __init__(self, status, reason):
        self.status = status
        self.reason = reason
        Exception.__init__(self, self.__str__())
    def __str__(self):
        return "(%s) %s" % (self.status, self.reason, )

def _compute_authentication_string(
    user_name, auth_key, auth_key_id, method, timestamp
):
    """
    Compute the authentication hmac sent to the server
    """
    message = "\n".join([user_name, method, str(timestamp)])
    hmac_object = hmac.new(
        auth_key,
        message,
        hashlib.sha256
    )
    return "DIYAPI %s:%s" % (auth_key_id, hmac_object.hexdigest(), )

class HTTPConnection(httplib.HTTPConnection):
    """
    DIY wrapper for httplib.HTTPConnection
    """
    def __init__(self, base_address, user_name, auth_key, auth_id):
        httplib.HTTPConnection.__init__(self, base_address)
        self._log = logging.getLogger("HTTPConnection")
        self._user_name = user_name
        self._auth_key = auth_key
        self._auth_id = auth_id

    def request(self, method, uri, body=None, headers=dict()):
        timestamp = current_timestamp()
        authentication_string = _compute_authentication_string(
            self._user_name, 
            self._auth_key,
            self._auth_id,
            method, 
            timestamp
        )

        headers.update({
            "Authorization"         : authentication_string,
            "X-DIYAPI-Timestamp"    : str(timestamp),
            "agent"                 : 'diy-tool/1.0'
        })

        httplib.HTTPConnection.request(
            self, method, uri, body=body, headers=headers
        )

        response = httplib.HTTPConnection.getresponse(self)
        if response.status != httplib.OK:
            self._log.error("request failed %s %s" % (
                response.status, response.reason, 
            )) 
            self.close()
            self.connect()
            raise HTTPRequestError(response.status, response.reason)

        return response

