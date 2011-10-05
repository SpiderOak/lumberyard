# -*- coding: utf-8 -*-
"""
HTTPConnection.py

nimbus.io wrapper for httplib.HTTPConnection
"""
import httplib
import logging

from lumberyard.http_util import current_timestamp, \
    compute_authentication_string

class LumberyardHTTPError(Exception):
    """
    a status of other than 200 OK has been retruned by the HTTP server
    """
    def __init__(self, status, reason):
        self.status = status
        self.reason = reason
        Exception.__init__(self, self.__str__())
    def __str__(self):
        return "(%s) %s" % (self.status, self.reason, )

class LumberyardRetryableHTTPError(LumberyardHTTPError):
    """
    a status of 503 Service unavailable was returned by the HTTP server
    but the request can b retried after an interval
    """
    def __init__(self, retry_after):
        LumberyardHTTPError.__init__(self, 503, "Service unavailable")
        self.retry_after = retry_after


class HTTPConnection(httplib.HTTPConnection):
    """
    nimbus.io wrapper for httplib.HTTPConnection
    """
    def __init__(
        self, base_address, user_name, auth_key, auth_id, debug_level=0
    ):
        httplib.HTTPConnection.__init__(self, base_address)
        self._log = logging.getLogger("HTTPConnection")
        self._user_name = user_name
        self._auth_key = auth_key
        self._auth_id = auth_id
        self.set_debuglevel(debug_level)
        self.connect()

    def request(self, method, uri, body=None, headers=dict()):
        timestamp = current_timestamp()
        authentication_string = compute_authentication_string(
            self._auth_id,
            self._auth_key,
            self._user_name, 
            method, 
            timestamp,
            uri
        )

        headers.update({
            "Authorization"         : authentication_string,
            "x-nimbus-io-timestamp" : str(timestamp),
            "agent"                 : 'lumberyard/1.0'
        })

        httplib.HTTPConnection.request(
            self, method, uri, body=body, headers=headers
        )

        response = self.getresponse()
        if response.status != httplib.OK:
            self._log.error("request failed %s %s" % (
                response.status, response.reason, 
            )) 
            self.close()
            self.connect()

            # if we got 503 service unavailable
            # and there is a retry_after header with an integer value 
            # give the caller a chance to retry
            if response.status == 503:
                retry_after = response.getheader("Retry-After", None)
                if retry_after is not None:
                    seconds = None
                    try:
                        seconds = int(retry_after)
                    except Exception:
                        pass
                    if seconds is not None and seconds > 0:
                        raise LumberyardRetryableHTTPError(seconds)

            raise LumberyardHTTPError(response.status, response.reason)

        return response

