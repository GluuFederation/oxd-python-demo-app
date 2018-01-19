#!/usr/bin/python

import Cookie
import os
import shelve
from constants import *
from appLog import *

envs = os.environ
c=Cookie.SimpleCookie()
if 'HTTP_COOKIE' in envs:
    cookie_string=envs['HTTP_COOKIE']
    c.load(cookie_string)
    try:
        session_id = c['session'].value
        db = shelve.open(DB_FILENAME)
        sub = db[session_id]['sub']
        del db[session_id]
        db.close()
        message = "Removed session from DB for %s" % sub
        log(message)
    except:
        message = "Error removing session from DB"
        logException(message)
else:
    log("No Cookie found")

c['session'] = ''
c['session']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'
c['session']['domain'] = ".%s" % COOKIE_DOMAIN

print c.output()
print "Content-type: text/html"
print
print '<HTML><HEAD><meta http-equiv="Refresh" content="0; url=%s"></HEAD></HTML>' % LOGOUT_CONFIRM 

