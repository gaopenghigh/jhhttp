#!/usr/bin/python
# -*- coding: utf-8 -*-
import simplejson
import urllib2
import traceback

class RequestWithMethod(urllib2.Request):
    def __init__(self, url, method, data=None, headers={},\
        origin_req_host=None, unverifiable=False):
        self._method = method
        urllib2.Request.__init__(self, url, data, headers, origin_req_host,
                unverifiable)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self)


class JhhttpError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def _prepare_data(data=None):
    if type(data) is not str:
        data = simplejson.dumps(data)
    return data

def _restful_headers(headers=None):
    if headers is None:
        headers = {}
        headers['Content-Type'] = 'application/json'
    else:
        headers['Content-Type'] = 'application/json'
    return headers

def _open(url, method, data=None, headers=None):
    try:
        req = RequestWithMethod(url, method, data, headers)
        response = urllib2.urlopen(req)
    except Exception, e:
        traceback.print_exc()
        raise JhhttpError(e)
    return response

def _return(response, response_type):
    if response_type is 'json':
        try:
            content = response.read()
            ret = simplejson.loads(content)
        except Exception, e:
            traceback.print_exc()
            raise JhhttpError(e)
    else:
        ret = repr(content)
    return ret

def _check(url, data, headers):
    if type(headers) is not dict:
        raise JhhttpError('headers is not a dict')

def _do_http(url, data=None, headers=None, method='GET', response_type='text'):
    _check()
    data = _prepare_data(data)
    f = _open(url, method, data, headers)
    return _return(f, response_type)

def rest_put(url, data=None, headers=None):
    headers = _restful_headers(headers)
    return _do_http(url, data, headers, 'PUT', 'json')

def put(url, data=None, headers=None):
    return _do_http(url, data, headers, 'PUT', 'text')

def rest_delete(url, data=None, headers=None):
    headers = _restful_headers(headers)
    return _do_http(url, data, headers, 'DELETE', 'json')

def delete(url, data=None, headers=None):
    return _do_http(url, data, headers, 'DELETE', 'text')

def rest_post(url, data=None, headers=None):
    headers = _restful_headers(headers)
    return _do_http(url, data, headers, 'POST', 'json')

def post(url, data=None, headers=None):
    return _do_http(url, data, headers, 'POST', 'text')

def rest_get(url, headers=None):
    headers = _restful_headers(headers)
    data = None
    return _do_http(url, data, headers, 'GET', 'json')

def get(url, headers=None):
    data = None
    return _do_http(url, data, headers, 'GET', 'text')
