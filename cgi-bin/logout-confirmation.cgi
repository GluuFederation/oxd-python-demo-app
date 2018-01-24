#!/usr/bin/python

import Cookie
import os
import shelve
from constants import *
from appLog import *

messages = []

def makeList(l):
    s = ""
    for item in l:
        s = "<LI>%s</LI>\n" % item
    return s

html = """<HTML><HEAD><TITLE>%(title)s</TITLE></HEAD>
<BODY>
<UL>
    %(message)s
</UL>
<hr>
</BODY>
</HTML>
"""

envs = os.environ
c=Cookie.SimpleCookie()
if 'HTTP_COOKIE' in envs:
    cookie_string=envs['HTTP_COOKIE']
    c.load(cookie_string)
    try:
        session_id = c['session'].value
        messages.append("Session cookie not deleted")
        try:
            db = shelve.open(DB_FILENAME)
            db_session = db[session_id]
            messages.append("DB session not deleted")
        except:
            messages.append("DB session deleted")
    except:
        messages.append("Cookie found but not session")
        messages.append(c.keys())
else:
    messages.append("Session cleared successfully")

log("Logout Confirmation: \n  * %s" % "\n  *".join(messages))
d = {'title': TITLE, 'message': makeList(messages)}

print "Content-type: text/html"
print
print html % d 

