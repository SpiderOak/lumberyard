# -*- coding: utf-8 -*-
"""
HTTPConnection.py

nimbus.io wrapper for HTTPSConnection
"""
try:
    from httplib import HTTPConnection
    from httplib import HTTPSConnection
    from httplib import BadStatusLine
    from httplib import OK
    from httplib import SERVICE_UNAVAILABLE
    from httplib import INTERNAL_SERVER_ERROR
except ImportError:
    from http.client import HTTPConnection
    from http.client import HTTPSConnection
    from http.client import BadStatusLine
    from http.client import OK
    from http.client import SERVICE_UNAVAILABLE
    from http.client import INTERNAL_SERVER_ERROR
import logging
import os
try:
    from urllib import unquote_plus
except ImportError:
    from urllib.parse import unquote_plus
import socket
import sys

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
        return "({0}) {1}".format(self.status, self.reason)

class LumberyardRetryableHTTPError(LumberyardHTTPError):
    """
    a status of 503 Service unavailable was returned by the HTTP server
    but the request can be retried after an interval
    """
    def __init__(self, retry_after):
        LumberyardHTTPError.__init__(self, 
                                     SERVICE_UNAVAILABLE, 
                                     "Service unavailable")
        self.retry_after = retry_after

_timeout_str = os.environ.get("NIMBUSIO_CONNECTION_TIMEOUT")
_timeout = (None if _timeout_str is None else float(_timeout_str))
_connection_retries = int(os.environ.get("NIMUSIO_CONNECTION_RETRIES", "5"))
_connection_retry_seconds = 15

# For testing on a local machines, we will not use SSL
if os.environ.get("NIMBUS_IO_SERVICE_SSL", "1") == "0":
    _base_class = HTTPConnection
else:
    _base_class = HTTPSConnection

class HTTPConnection(_base_class):
    """
    base_address
        A hostname or address that should resolve to a socket connection on a 
        server.

        For example ``nimbus.io`` or ``127.0.0.1:8088``

    user_name
        name of a valid nimbus.io user

    auth_key
        an authentication key valid for the user

    auth_id
        the id number of the authentication key

    debug level
        debug level of HTTPConnection base class 

    nimbus.io wrapper for HTTPSConnection. This constructor performs
    the initial connection but does not send a request.
    """
    def __init__(
        self, 
        base_address, 
        user_name, 
        auth_key, 
        auth_id, 
        debug_level=0
    ):
        _base_class.__init__(self, base_address, timeout=_timeout)
        self._log = logging.getLogger("HTTPConnection")
        self._user_name = user_name
        self._auth_key = auth_key
        self._auth_id = auth_id
        self.set_debuglevel(debug_level)
        self._connected = False

    def close(self):
        self._log.debug("close()")
        if self._connected:
            _base_class.close(self)
            self._connected = False

    def request(self, 
                method, 
                uri, 
                body=None, 
                headers=None, 
                expected_status=OK):
        """
        method
            one of GET, PUT, POST, DELETE, HEAD

        uri
            the REST command for this request

        body
            if present, must be a string or an open file object

        headers
            a dictionary of key/value pairs to be added to the HTTP headers

        expected_status
            status indicating a successful result, for example 201 CREATED

        send an HTTP request over the connection
        return a HTTPResponse object, or raise an exception
        """
        retry_count = 0
        while not self._connected:
            try:
                self.connect()
            except Exception:
                instance = sys.exc_info()[1]
                # this could be an error from a real socket or a gevent 
                # monkeypatched socket. So we check the string
                if "DNSError".lower() in str(instance).lower():
                    retry_count += 1
                    if retry_count > _connection_retries:
                        self._log("DNSError: too many retries".format(
                            retry_count))
                        raise
                    self._log("DNSError retry {0} in {1} seconds".format(
                        retry_count, _connection_retry_seconds))
                    continue                       
                self._log.exception("Unhandled connection error {0}".format(
                    str(instance)))
                raise
            self._connected = True

        if headers is None:
            headers = dict()

        timestamp = current_timestamp()
        authentication_string = compute_authentication_string(
            self._auth_id,
            self._auth_key,
            self._user_name, 
            method, 
            timestamp,
            unquote_plus(uri)
        )

        headers.update({
            "Authorization"         : authentication_string,
            "x-nimbus-io-timestamp" : str(timestamp),
            "agent"                 : 'lumberyard/1.0'
        })

        # nginx will (rightly) reject with HTTP status 411 Length Required if
        # we send a PUT without a Content-Length header, even if the body size
        # is 0.  and our httplib base class won't add this header if body is
        # None.
        if method == "PUT":
            try:
                headers.setdefault("Content-Length", str(len(body)))
            except TypeError:
                if body is None:
                    headers.setdefault("Content-Length", str(0))

        # the body maybe beyond 7 bit ascii, so a unicode URL can't be combined
        # with it into a single string to form the request.

        try:
            _base_class.request(self, 
                                method, 
                                uri, 
                                body=body, 
                                headers=headers)
        except Exception:
            instance = sys.exc_info()[1]
            # 2012-02-14 dougfort -- we are getting timeouts here
            # on heavily loaded benchmark tests
            self._log.exception(str(instance))
            self.close()
            # 2012-10-12 dougfort -- if we get an exception here, it's not
            # an internal server error. So pass it on and let the caller deal
            # with it
            raise

        try:
            response = self.getresponse()
        except BadStatusLine:
            instance = sys.exc_info()[1]
            self._log.exception("BadStatusLine: '{0}'".format(instance))
            self.close()
            raise LumberyardHTTPError(INTERNAL_SERVER_ERROR, 
                                      "BadStatusLine")

        if response.status != expected_status:
            self._log.error("request failed {0} {1}".format(response.status, 
                                                            response.reason)) 

            # the server may have closed the connection already if this is an
            # error response
            try:
                response.read()
            except socket.error:
                pass

            self.close()

            # if we got 503 service unavailable
            # and there is a retry_after header with an integer value 
            # give the caller a chance to retry
            if response.status == SERVICE_UNAVAILABLE:
                retry_after = response.getheader("RETRY-AFTER", None)
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

class UnAuthHTTPConnection(_base_class):
    """
    base_address
        A hostname or address that should resolve to a socket connection on a 
        server.

        For example ``nimbus.io`` or ``127.0.0.1:8088``

    debug level
        debug level of HTTPConnection base class 

    nimbus.io wrapper for HTTPSConnection. This constructor performs
    the initial connection but does not send a request.
    """
    def __init__(
        self, 
        base_address, 
        debug_level=0
    ):
        _base_class.__init__(self, base_address, timeout=_timeout)
        self._log = logging.getLogger("UnAuthHTTPConnection")
        self.set_debuglevel(debug_level)
        self.connect()

    def request(self, 
                method, 
                uri, 
                body=None, 
                headers=None, 
                expected_status=OK):
        """
        method
            one of GET, POST, DELETE, HEAD

        uri
            the REST command for this request

        body
            if present, must be a string or an open file object

        headers
            a dictionary of key/value pairs to be added to the HTTP headers

        expected_status
            status indicating a successful result, for example 201 CREATED

        send an HTTP request over the connection
        return a HTTPResponse object, or raise an exception
        """
        if headers is None:
            headers = dict()

        headers.update({
            "agent"                 : 'lumberyard/1.0'
        })

        # nginx will (rightly) reject with HTTP status 411 Length Required if
        # we send a PUT without a Content-Length header, even if the body size
        # is 0.  and our httplib base class won't add this header if body is
        # None.
        if method == "PUT":
            try:
                headers.setdefault("Content-Length", str(len(body)))
            except TypeError:
                if body is None:
                    headers.setdefault("Content-Length", str(0))

        # the body maybe beyond 7 bit ascii, so a unicode URL can't be combined
        # with it into a single string to form the request.

        try:
            _base_class.request(self, 
                                method, 
                                uri, 
                                body=body, 
                                headers=headers)
        except Exception:
            instance = sys.exc_info()[1]
            # 2012-02-14 dougfort -- we are getting timeouts here
            # on heavily loaded benchmark tests
            self._log.exception(str(instance))
            self.close()
            raise LumberyardHTTPError(INTERNAL_SERVER_ERROR, 
                                      str(instance))

        try:
            response = self.getresponse()
        except BadStatusLine:
            instance = sys.exc_info()[1]
            self._log.exception("BadStatusLine: '{0}'".format(instance))
            self.close()
            raise LumberyardHTTPError(INTERNAL_SERVER_ERROR, 
                                      "BadStatusLine")

        if response.status != expected_status:
            self._log.error("request failed {0} {1}".format(response.status, 
                                                            response.reason)) 

            # the server may have closed the connection already if this is an
            # error response
            try:
                response.read()
            except socket.error:
                pass

            self.close()

            # if we got 503 service unavailable
            # and there is a retry_after header with an integer value 
            # give the caller a chance to retry
            if response.status == SERVICE_UNAVAILABLE:
                retry_after = response.getheader("RETRY-AFTER", None)
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

