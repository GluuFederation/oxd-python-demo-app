#!/usr/bin/python

import shelve
import os
from constants import *
from appLog import *

db = shelve.open(DB_FILENAME, "n")
db.close()

log("Database %s created" % DB_FILENAME)

# Not for production usage  :-)
os.system("/bin/cp %s %s" % (CONFIG_FILE_ORIGINAL, CONFIG_FILE))
os.system("/bin/chmod 777 %s" % DB_FILENAME)
os.system("/bin/chmod 777 %s" % LOG_FN) 
os.system("/bin/chmod 777 %s" % CONFIG_FILE) 

