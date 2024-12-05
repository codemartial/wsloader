wsloader
========

WSGI Application and Protocol for exposing Python Modules as REST API

Webservice Loader (wsloader) is a WSGI application and protocol
to allow exposing native Python interfaces as REST-like webservices
without writing any HTTP/web-service specific code to expose a new
service.

Convert this:
```python
# greeter.py
def say_hello():
   return "Hello World!"
```

to this:
```sh
$ curl -D - 'http://localhost:8080/say_hello'
HTTP/1.1 200 OK
Content-Length: 13
Content-Type: text/plain; charset=utf-8
Last-Modified: Thu, 05 Dec 2009 09:30:01 GMT
Date: Thu, 05 Dec 2009 09:34:47 GMT

Hello World!
```
with *no additional code*! 

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
   * handling of service independent request and response marshalling via JSON
   * automatic URL creation based on the module path (can be overridden)
   * automatic enforcing of GET and POST methods for read and write endpoints
   * proper HTTP error responses for service invocation failures
   * high-performance application loading and state management
   * redirection of `sys.stderr` to apache error logs 

See the Quick-start Guide for more details, at [example/example.md](example/example.md)
