import logging
from constants import *

logger = logging.getLogger(TITLE)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOG_FN)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s|%(levelname)s::: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def log(s):
    logger.debug(s)

def logException(s):
    logger.exception(s)

def logError(s):
    logger.error(s)
