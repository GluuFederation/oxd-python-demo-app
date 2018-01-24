#!/usr/bin/python

import cgi
import Cookie
import os
import oxdpython
import shelve
import time
import uuid

from constants import *
from appLog import *

oxc = oxdpython.Client(CONFIG_FILE)
c=Cookie.SimpleCookie()
try:
    # get the token after authorization
    f = cgi.FieldStorage()
    state = f.getvalue('state')
    code = f.getvalue('code')
    log("Login callback received code: %s and state: %s" % (code, state))
    tokens = oxc.get_tokens_by_code(code, state)
    
    # get user information
    at = tokens['access_token']
    log("Trying to get user_info with access token ending in %s" % at[-5:])
    user = oxc.get_user_info(at)

    sub = user['sub'][0]
    expiration_in_seconds = EXPIRATION_IN_MINUTES * 60
    session_id = str(uuid.uuid4())
    log("Writing session id: %s" % session_id)
    db = shelve.open(DB_FILENAME, "w")
    db[session_id] = {'sub': sub, 'exp': time.time() + expiration_in_seconds}
    db.close()
    log("Created session %s for user %s in DB" % (session_id, sub))
    c['session'] = session_id
    c['session']['expires'] = expiration_in_seconds
    c['session']['domain'] = ".%s" % COOKIE_DOMAIN
    log("Writing cookie: \n%s" % str(c))
    print c.output()
except:
    logException("Error processing login callback...")

print "Content-Type: text/html"
print
print '<HTML><HEAD><meta http-equiv="Refresh" content="0; url=%s"></HEAD></HTML>' % HOME_URL

