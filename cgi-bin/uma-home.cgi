#!/usr/bin/python

import urllib2
import ssl
import json
import traceback
import Cookie
import os

from constants import *
from common import *

html = """<HTML><HEAD><TITLE>%(title)s</TITLE></HEAD>
<BODY>
<H1>%(title)s</H1>
%(message)s
<hr>
<h6>POWERED BY</h6>
<IMG SRC="https://www.gluu.org/wp-content/themes/gluu/images/logo.png" alt="Powered by Gluu"
 width="100" />
</BODY>
</HTML>
"""
TITLE = "UMA RP Home Page"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

c = Cookie.SimpleCookie()
if 'HTTP_COOKIE' in os.environ:
    cookie_string = os.environ['HTTP_COOKIE']
    c.load(cookie_string)

if c.get('access_token'):
    message = "<p>Access protected resources using RPT</p>"
else:
    message = "<p>Available resources from the resource server:</p>"

log("Showing a list of available resource endpoints from the RS")
try:
    response = urllib2.urlopen(RS_BASE_URL, context=ctx)
    resources = json.loads(response.read())['resources']
    # Generate html links
    links = ['<li><a href="/cgi-bin/request-resource.cgi?api={endpoint}">{endpoint}</a> - Protected Status: {uma_protected}</li>'.format(**r)
             for r in resources]
    message += "<ul>" + "\n".join(links) + "</ul>"
except urllib2.HTTPError:
    message = "Failed to get resources from the UMA RS"
    logError(message)
    logException(traceback.format_exc())
except TypeError:
    message = "The data received from the UMA RS doesn't meet expectation."
    logError(message)
    logException(traceback.format_exc())


d = {}
d['title'] = TITLE
d['message'] = message

print "Content-type: text/html\r\n"
print ""
print html % d

