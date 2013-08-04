wsloader
========

WSGI Application and Protocol for exposing Python Modules as REST API

Webservice Loader (wsloader) is a WSGI application and protocol
to allow exposing native Python interfaces as REST-like webservices
without writing any HTTP/web-service specific code to expose a new
service.

Objectives
----------

The objectives of wsloader are:

   1. Minimal/Zero extra code and configuration to expose Python
   interfaces as a webservice
   2. Clean separation of webservice delivery mechanism and service
   implementation
   3. Full encapsulation of webservice protocols and mechanisms for
   authentication, authorisation, serialisation, end-point discovery
   and loading, logging and load balancing 

Features
--------

Currently wsloader supports the following features:

   * loading any Python module/class as a service
   * handling of service independent request and response marshalling
   * via JSON
   * automatic URL creation based on the module path (can be
   * overridden)
   * automatic enforcing of GET and POST methods for read and write
   * endpoints
   * proper HTTP error responses for service invocation failures
   * high-performance application loading and state management
   * apache error log access to module code via sys.stderr 

See the Quick-start Guide for more details, at
http://code.google.com/p/wsloader/wiki/QuickStart
