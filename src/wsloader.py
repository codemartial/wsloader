"""
Webservice Loader (wsloader)
See README.txt accompanying this module for details

"""

__licence__ = """
Copyright 2009-2010 Lulu, Inc.  

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this file except in compliance with the License. You may
obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.
"""

__version__ = 1.2

import sys, os, time
import simplejson as json

from werkzeug import responder
from werkzeug.wrappers import Request, Response, EnvironHeaders
from werkzeug.exceptions import MethodNotAllowed, BadRequest, InternalServerError
from werkzeug.routing import Map, Rule, NotFound
from ConfigParser import SafeConfigParser, ParsingError

URL_MAP = Map([Rule('/<path:service>/<endpoint>')])

class WSLoader(object):
    """ WSGI Application Definition
    This class defines the "WSLoader" WSGI application that is
    used to expose Python modules as web services on apache2 via
    mod_wsgi
    
    """
    def __init__(self, confdir = '/etc/wsloader-wsgi/'):
        """ Initialise the service loader        
        Scans confdir directory for service configurations and loads them
        
        """
        # default endpoint prefixes indicating a write operation
        # used for ensuring POST requests to these endpoints
        self.writeops = ("add", "post", "submit", "set", "update", "delete")
        
        self.services = {}
        config = SafeConfigParser()
        conf_files = [os.path.join(confdir + x) for x in os.listdir(confdir)]
        try:
            config.read(conf_files)
        except ParsingError, e:
            raise e
        
        for module in config.sections():
            self.services[module] = dict(config.items(module))

        # Deserialise csv stuff to list
        for module, config in self.services.items():
            for key, value in config.items():
                if key not in ['unencoded_params', 'drop_keys']:
                    continue
                vlist = [x.strip() for x in value.split(',')]
                config[key] = vlist

    def __get_module(self, modname):
        """Load a module by name or find it in already loaded modules"""
        if modname not in sys.modules:
            try:
                __import__(modname)
            except ImportError:
                raise NotFound(description = "%s implementation could not be loaded" % modname)

        return sys.modules[modname]
        
    def __get_endpoint(self, resources):
        """Get a service callable matching the given URI"""
        service = resources['service'].replace('/', '.')
        if service not in self.services:
            raise NotFound(description = "Service %s was not found " % service)
        
        endpoint = None
        srv_conf = self.services[service] # Service configuration
        
        # Check if the service maps to a different installed module
        if srv_conf.get('alias_to', None):
            service = srv_conf['alias_to']
        
        if srv_conf.get('type', None) == 'class':
            modname, _, classname = service.rpartition(".")
            module = self.__get_module(modname)
            classdef = getattr(module, classname)
            method = getattr(classdef, resources['endpoint'])
            
            if srv_conf.get('init_param', None):
                endpoint = (classdef, method, srv_conf['init_param'])
            else:
                endpoint = getattr(classdef(), resources['endpoint'])
        else:
            module = self.__get_module(service)
            endpoint = getattr(module, resources['endpoint'])

        return endpoint

    def __get_response(self, environ, args, kwargs, endpoint):
        if endpoint.__name__ == "service_check":
            result = endpoint(*args, **kwargs)
            response = Response(result['body'])
            response.status_code = result['status']
            return response

        response = {
            'server_info': {
                'http_headers': dict(EnvironHeaders(environ)),
                'response_id': 0,
                'arguments': repr(args) if args else repr(kwargs),
                'processing_time': 0.0
                },
            'response': {}
            }
        
        start_time = time.time()
        # Make the call
        result = endpoint(*args, **kwargs)
        
        # Send the API call response
        response['response'] = result
        response['server_info']['processing_time'] = 1000*(time.time() - start_time)
        try:
            response = json.dumps(response)
        except (TypeError, UnicodeError):
            return InternalServerError(description = "Could not encode service response")
                                    
        response = Response(response)
        response.headers['content-type'] = 'application/json'        
        return response
    
    @responder
    def __call__(self, environ, start_response):
        """ WSGI Callable"""
        
        request = Request(environ)
        
        # Get the callable endpoint
        url = URL_MAP.bind_to_environ(environ)
        _, resources = url.match()
        try:
            endpoint = self.__get_endpoint(resources)
        except NotFound, e:
            return e
        except AttributeError, e:
            return NotFound(description =
                            "Endpoint \'%s\' not found in service \'%s\' "
                            % (resources['endpoint'], resources['service']))
        
        service = resources['service'].replace('/', '.')
        srv_conf = self.services[service]
        
        if resources['endpoint'].startswith(self.writeops):
            if request.method != 'POST': return MethodNotAllowed(['POST'])
            if srv_conf.get("merge_req_params", False):
                reqdata = request.args.copy()
                reqdata.update(request.form)
            else:
                reqdata = request.form
        else:
            if request.method != 'GET': return MethodNotAllowed(['GET'])
            reqdata = request.args
        
        #JSON Decode all values
        kwargs = {}
        try:
            for key, value in reqdata.iteritems():
                if key in srv_conf.get('drop_keys', []):
                    continue
                if key in srv_conf.get('unencoded_params', []):
                    kwargs[key] = value.encode('utf-8')
                else:
                    kwargs[key] = json.loads(value.encode("utf-8"))
        except (TypeError, ValueError, UnicodeError):
            return BadRequest("Could not decode a parameter value %s for key %s" % (value, key))
        
        # Use "args" as a list of positional params
        args = kwargs.pop("args", [])
        
        if type(endpoint) == type(()): # Instance Method
            (classdef, method, init_arg) = endpoint
            
            if init_arg not in kwargs:
                return BadRequest("Required parameter %s is missing" % init_arg)
            
            endpoint = getattr(classdef(kwargs.pop(init_arg)), method.__name__)
            
        if not callable(endpoint):
            return NotFound(description = "%s is not a service method" % resources['endpoint'])
        
        response = self.__get_response(environ, args, kwargs, endpoint)
        return response

application = WSLoader()
