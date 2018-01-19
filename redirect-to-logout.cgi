#!/usr/bin/python

import cgi
import os
import oxdpython
from constants import *
from appLog import *

oxc = oxdpython.Client(CONFIG_FILE)
logout_url = oxc.get_logout_uri()
log("Redirect to logout url: %s" % logout_url)

print "Location: ", logout_url, "\r\n"
print "Connection: close \r\n"
print ""
print "Redirecting"

