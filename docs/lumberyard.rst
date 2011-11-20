.. lumberyard documentation master file, created by
   sphinx-quickstart on Sun Nov 20 08:24:16 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to lumberyard's documentation!
======================================

Contents:

.. toctree::
   :maxdepth: 2

An introduction to the nimbus.io **lumberyard** library.
--------------------------------------------------------

This library is a small set of low level tools for accessing the nimbus.io
REST API. We mainly use it to support the motoboto S3 emulation library,
but you can use it directly if you want to access nimbus.io without simulating
S3.

HTTP Connection
---------------
.. autoclass:: lumberyard.http_connection.HTTPConnection
    :members:

Utility Functions
-----------------
.. automodule:: lumberyard.http_util
    :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

