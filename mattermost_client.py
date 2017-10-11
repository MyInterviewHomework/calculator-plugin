#!/usr/bin/env python

import httplib, urllib
import sys
import re
import json


body= {'channel_id': 'cniah6qa73bjjjan6mzn11f4ie',
 'channel_name': 'town-square',
 'command': '',
 'response_url': 'not+supported+yet',
 'team_domain': 'someteam',
 'team_id': 'rdc9bgriktyx9p4kowh3dmgqyc',
 'text': '',
 'token': 'xr3j5x3p4pfk7kk6ck7b4e6ghh',
 'user_id': 'c3a4cqe3dfy6dgopqt8ai3hydh',
 'user_name': 'somenam'}

headers= {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "application/json",
	   "User-Agent": "Go 1.1 package http",
	   "Host": "127.0.0.1:5000", 
	   "Content-Length": 0}


#get http server ip
http_server = "127.0.0.1"

def do_post(conn, slash, expr):
    """"Client send post request to server"""
    body["text"] = expr
    body["command"] = slash
    params = urllib.urlencode(body)
    
    print "Sending HTTP POST Request for slash command '{0}'".format(slash)
    
    headers["Content-Length"] = len(params)
    conn.request("POST", "", params, headers)

def do_get(conn, expr):
    """"Client send post request to server"""
    body["text"] = expr
    params = urllib.urlencode(body)

    headers["Content-Length"] = len(params)

    conn.request("GET", "", params, headers)


def get_response(conn, expr):
    """Client query en print response"""
    response = conn.getresponse()
    res = response.read()
    # print response.status, response.reason," : ",
    res = json.loads(res)
    print "{0} = {1}".format(expr,res["text"])

def run():
    """Mattermost client framework """ 
    #get http server ip
    http_server = "127.0.0.1"
    
    #create a connection
    conn = httplib.HTTPConnection(http_server+":8000")
    
    while 1:
    	cmd = raw_input('>')
    	cmd = cmd.replace('"',"")
    	slash = re.findall("^/[a-zA-Z]+", cmd)

    	if len(slash) == 0: 
			pass
    	else:
			slash = slash[0]
			expr = re.sub("^/[a-zA-Z]+ *", "", cmd)
			do_post(conn, slash, expr)
			print "Query response"
			get_response(conn,expr)
    conn.close()

if __name__ == "__main__":
    run()
