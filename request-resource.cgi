#!/usr/bin/python

import cgi
import os
import oxdpython
import traceback
import urllib2
import ssl
import Cookie
import sys

from constants import *
from appLog import *
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

api_url = RS_BASE_URL + "api/photos/"
TITLE = 'UMA RP Accessing %s' % api_url
envs = os.environ
session = get_session(envs)
client = oxdpython.Client(CONFIG_FILE)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

c = Cookie.SimpleCookie()
if 'HTTP_COOKIE' in envs:
    cookie_string = envs['HTTP_COOKIE']
    c.load(cookie_string)

try:
    log("Requesting resource from %s" % api_url)
    req = urllib2.Request(api_url)
    # Add the authorization RPT if present
    if 'token_type' in  c and 'access_token' in c:
        req.add_header('Authorization', '%s %s' % (
                       c['token_type'].value, c['access_token'].value))

    response = urllib2.urlopen(req, context=ctx)
    message = "Response from Resource Server: <pre>%s</pre>" % response.read()
except urllib2.HTTPError as error_response:
    message = str(error_response)
    # Expect a 401 response when the RPT is empty
    if 'www-authenticate' in error_response.headers:
        log("Received 401 with www-authenticate header. Redirecting to get RPT.")
        www_auth = error_response.headers['www-authenticate']
        auth_values = dict(x.split('=') for x in www_auth.split(','))
        ticket = auth_values['ticket'].strip("\"")
        c['ticket'] = ticket
        message = "Received 401 Unauthorized. <a href='/cgi-bin/get-rpt.cgi'>Get RPT Access Token</a>"
    else:
        message = 'Request for resource at %s failed. See logs.' % api_url
        logError(message)
        logException(traceback.format_exc())
except:
    message = 'Request for resource at %s failed. See logs.' % api_url
    logError(message)
    logException(traceback.format_exc())

# Clear the RPT after it is used
c['token_type'] = ''
c['token_type']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'
c['access_token'] = ''
c['access_token']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'

d = {}
d['title'] = TITLE
d['message'] = message

print c.output()
print "Content-type: text/html"
print
print html % d