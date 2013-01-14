# -*- coding: utf-8 -*-
"""
read_reporter.py

class ReadReporter

A class that wraps a python file object (or something like him)
and reports bytes read to a callback.

Intended to be passed as the 'body' parameter to HTTPConnection.request

Takes an open python file object and a callback functions as arguments
The callback should take a single integer as an argument: bytes_read.
"""
import collections
import logging

class ReadReporter(collections.Iterable):
    """
    A class that wraps a python file object (or something like him)
    and reports bytes read to a calback

    Intended to be passed as the 'body' parameter to HTTPConnection.request

    Takes an open pythong file object and a callback functions as arguments
    The callback should take a single integer as an argument: bytes_read.
    """
    def __init__(self, file_object, callback=None):
        self._log = logging.getLogger("ReadReporter")
        self._file_object = file_object
        self._callback = callback

    def __iter__(self):
        while True:
            data = self.read()
            if len(data) == 0:
                break
            yield data

    def set_callback(self, callback):
        self._callback = callback

    def close(self):
        self._log.debug("close")
        self._file_object.close()

    def fileno(self):
        self._log.debug("fileno = {0}".format(self._file_object.fileno()))
        return self._file_object.fileno()

    def read(self, size=None):
        self._log.debug("read({0})".format(size))
        data = None
        if size is None:
            data = self._file_object.read()
        else:
            data = self._file_object.read(size)

        self._log.debug("actual bytes read {0}".format(len(data)))
        self._callback(len(data))

        return data

    def seek(self, offset, whence=None):
        self._log.debug("seek({0}, {1})".format(offset, whence))
        self._file_object.seek(offset, whence)

    def tell(self):
        result = self._file_object.tell()
        self._log.debug("tell() = {0}".format(result))
        return result

