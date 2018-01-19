#!/usr/bin/python

import cgi
import os
import oxdpython
from appLog import *
from constants import *

oxc = oxdpython.Client(CONFIG_FILE)

# get the authorization url from the gluu-server and redirect
auth_url = oxc.get_authorization_url()
log("Sent redirect to %s" % auth_url)

print "Location: ", auth_url, "\r\n"
print "Connection: close \r\n"
print ""
print "Redirecting"

