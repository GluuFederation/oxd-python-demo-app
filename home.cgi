#!/usr/bin/python

import Cookie
import os
import shelve
import time
import traceback

from constants import *
from appLog import *
from common import *

html = """<HTML><HEAD><TITLE>%(title)s</TITLE></HEAD>
<BODY>
<H1>%(title)s</H1>
%(message)s
<hr>
</BODY>
</HTML>
"""

message = """<P><a href="%s">OpenID Connect Login</a></P>""" % GET_AUTH_URL
envs = os.environ
session = get_session(envs)

sub = None
if session:
    sub = session['sub']
    exp = int(session['exp'])
    os.environ['TZ'] = TZ
    time.tzset()
    expiration_time =  time.strftime('%x %X %Z', time.localtime(exp))
    message = """Subject: %s
Application Session Expires: %s
<P><a href="%s">OpenID Connect Logout</a> </P>""" % (sub, expiration_time, GET_LOGOUT_URL)
else:
    message = """<P><a href="%s">OpenID Connect Login</a></P>""" % GET_AUTH_URL
    message = "No session found. <BR>" + message
    log("Printing login link")

if sub:
    log("Printing homepage for sub %s" % sub)
else:
    log("Printing homepage with link to login.")

d = {}
d['title'] = TITLE
d['message'] = message

print "Content-type: text/html"
print
print html % d
