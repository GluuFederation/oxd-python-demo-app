#!/usr/bin/python

# For DEMO purposes ONLY!
# Not for production usage!

import shelve
import os
import os.path
from constants import *

def ls(exclude=[]):
    import os
    f_list = []
    for subdir, dirs, files in os.walk('./'):
        for fn in files:
            if (fn[-4:] != '.pyc') and (fn not in exclude):
                f_list.append(fn)
    f_list.sort()
    return f_list

# Create the application folder
if not os.path.isdir(APP_FOLDER):
     os.mkdir(APP_FOLDER)

from appLog import *

# Create the database
db = shelve.open(DB_FILENAME, "n")
db.close()
log("Database created: %s " % DB_FILENAME)

# Copy the default config file to the live location
demosite_cfg = DEMOSITE_CFG % tuple(4 * [COOKIE_DOMAIN])
f = open(CONFIG_FILE, 'w')
f.write(demosite_cfg)
f.close()
log("Wrote config file to %s" % CONFIG_FILE)

# Copy files to cgi-bin
cgi_files = ls(DONT_INSTALL_LIST)
for fn in cgi_files:
    isCGI = ('.cgi' == fn[-4:])
    os.system("/bin/cp %s %s" % (fn, CGI_BIN))
    if isCGI:
        os.system("/bin/chmod 555 %s/%s" % (CGI_BIN, fn))
    log("Copied %s to %s" % (fn, CGI_BIN))

# Make sure the web user can write these files.
# Even the config file needs to be writable, because
# the oxid returned from oxd will be written there.
# Note: 777 allows ANY USER to read / write. Bad for
# security, but this is only a demo.
os.system("/bin/chmod 777 %s" % APP_FOLDER)
os.system("/bin/chmod 777 %s" % DB_FILENAME)
os.system("/bin/chmod 777 %s" % LOG_FN)
os.system("/bin/chmod 777 %s" % CONFIG_FILE)
