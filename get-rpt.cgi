#!/usr/bin/python

import Cookie
import os
import oxdpython
import traceback
import sys

from oxdpython.exceptions import NeedInfoError

from constants import *
from appLog import *

client = oxdpython.Client(CONFIG_FILE)

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
title = "Getting RPT Access Token from the Authorization Server"

c = Cookie.SimpleCookie()
if 'HTTP_COOKIE' in os.environ:
    c.load(os.environ['HTTP_COOKIE'])

try:
    ticket = c['ticket'].value
    rpt = client.uma_rp_get_rpt(ticket=ticket)

    c['token_type'] = rpt['token_type']
    c['access_token'] = rpt['access_token']
    log("Writing cookie: \n%s" % str(c))
    print c.output()
    message = "Successfully received RPT. <a href='/cgi-bin/request-resource.cgi'>Get Resource using access token</a>"
except NeedInfoError as ne:
    if 'redirect_user' in ne.details:
        claims_url = client.uma_rp_get_claims_gathering_url(ne.details['ticket'])
        print "Location: %s\r\n" % claims_url
        print ""
        print "Redirecting"
    else:
        message = "Received NeedInfo Error, but no redirect flag present."
        logError(message)
        logException(traceback.format_exc())
except:
    message = "Failed to get RPT. Look at logs."
    logError(message)
    logException(traceback.format_exc())

d = {}
d['title'] = title
d['message'] = message
print "Content-Type: text/html"
print ""
print html % d




