#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

"""
# -----------------------------------------------------------------------------------------
# calcaltor.py
#
# HTTP server for simple integer expressions including addition, subtraction and parenthesis
# The server receives HTTP POST or HTTP GET requests from Mattermost
## -----------------------------------------------------------------------------------------
"""

import json
import re
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib

import calcyacc

# Module that computes 
calc = calcyacc.CalcYacc()

class CalculatorHTTPRequestHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler with GET/POST commands.
    This get a post command from mattermost with a text defining and integer expression
    The GET/POST requests are identical except that the GET does not compute the expression (it provides the latest valid result)
    """
    def do_POST(self):
	    "Respond to POST request."
	    # Widraw the expression to compute from post body 
	    content_len = int(self.headers.getheader('content-length', 0))
	    post_body = self.rfile.read(content_len)
				
	    # Parse and Compute the expression
	    code = 200 
	    try:
    		# Decode
    		post_body = urllib.unquote(post_body)
    		body = self._get_form(post_body)
    		if body["command"] == "/calcul":
				data = body["text"]
				res = calc.calcul(data)
				print " {0} = {1}".format(data,res)
    		else:
				res = "Bad slash command '{0}'".format(body["command"])
				code = 400
	    except SyntaxError,e:
    	    	res = str(e)
    	    	code = 400 # Bad Request
	    except UnicodeDecodeError,e:
				res = str(e)
				code = 400 # Bad Request

	    self._set_header(code)
	    self._set_payload(res)
			
		
    def do_GET(self):
    	"""Respond to a GET request."""
    	# Send code OK (200) response
    	self._set_header(200)
    	# Send Latest result
    	res = calc.result
    	self._set_payload(res)

    def _set_header(self, code):
		"""Set abd send the header of response
		:param code : Code of the response status
		:param expr : The expression to parse
		:type expr: int
		"""
		self.send_response(code)
		# Send Header first 
		self.send_header("content-type", "application/json")
		self.end_headers() 

    def _set_payload(self, text):
		"""Set the payload response
		:param text : Payload text
		:param expr : string
		"""
		payload={"response_type": "in_channel", "text": text}
		self.wfile.write(json.dumps(payload))
		
    def _get_form(self, form_raw):
	    """Construct an application/x-www-form-urlencoded body as python dict.
		:param form_raw : Raw resquest application/x-www-form-urlencoded
		:param expr : string
		:return: a python dict of the application/x-www-form-urlencoded
		:rtype: dict
		"""
	    form = dict()
	    form_raw = form_raw.split("&")
	    for var_val in form_raw:
    		var,val = var_val.split("=")
    		form[var] = val
	    return form
		
def run():
    print('Http server is starting...')
    #ip and port of servr
    #by default http server port is 8000
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, CalculatorHTTPRequestHandler)
    print('Http server is running... on 127.0.0.1 port 8000')
    httpd.serve_forever()
  
if __name__ == '__main__':
    run()

