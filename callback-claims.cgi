#!/usr/bin/python

import cgi
import Cookie
import os
import sys

from appLog import *

c = Cookie.SimpleCookie()
if 'HTTP_COOKIE' in os.environ:
    c.load(os.environ['HTTP_COOKIE'])

f = cgi.FieldStorage()
auth_state = f.getValue('authorization_state')

if auth_state != 'claims_submitted':
    logError("Received authorization state: %s" % auth_state)
    logError("Cannot get RPT.")
    print "Unsuitable Authorization State: %s" % auth_state
    print ""
    sys.exit(1)

log("Authorization completed. Requesting RPT.")
ticket = f.getvalue('ticket')
c['ticket'] = ticket
print c.output()
print "Content-Type: text/html\r\n"
print ""
print "<html><body><a href='/cgi-bin/get-rpt.cgi'>Get RPT</a></body></html>"


