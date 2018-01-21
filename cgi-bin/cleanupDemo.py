#!/usr/bin/python

# For DEMO purposes ONLY!
# Not for production usage!

import os
from constants import *

def ls(exclude=[]):
    f_list = []
    for subdir, dirs, files in os.walk('./'):
        for fn in files:
            if fn not in exclude: f_list.append(fn)
    f_list.sort()
    return f_list

# Remove app data folder
os.system('/bin/rm -rf %s' % APP_FOLDER)

# Remove files from cgi-bin
cgi_files = ls(DONT_INSTALL_LIST)
for fn in cgi_files:
    os.system("/bin/rm -f %s/%s" % (CGI_BIN, fn))
    if fn[-3:] == '.py':
        os.system("/bin/rm -f %s/%sc" % (CGI_BIN, fn))

