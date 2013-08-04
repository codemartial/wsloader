#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.append("../src")

import unittest
import wsloader
import simplejson as json
from werkzeug import Client, BaseResponse
from werkzeug.debug import DebuggedApplication


class TestWSLoader(unittest.TestCase):
    def setUp(self):
        app = wsloader.WSLoader(confdir = os.getcwd() + '/conf/')
        self.client = Client(app, BaseResponse)

    def test_service_check(self):
        response = self.client.get("/greeter/service_check")
        print response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "OK")

    def test_defaults(self):
        response = self.client.get("/greeter/say_hello")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        self.assertEqual(body['response'], "Hello World!")

    def test_aliased_class(self):
        response = self.client.get('/helloworld/say_hello?greeting="Hola"&to_whom="Amigos!"')
        try:
            body = json.loads(response.data)
        except Exception, e:
            print e
            print response.data
            return
        self.assertEqual(body['response'], "Hola Amigos!")

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestWSLoader)
  unittest.TextTestRunner(verbosity=2).run(suite)
    
