from appLog import *
from constants import *

def get_session(envs):
    import Cookie, shelve
    session = None
    if 'HTTP_COOKIE' in envs:
        cookie_string=envs['HTTP_COOKIE']
        c=Cookie.SimpleCookie()
        c.load(cookie_string)
        try:
            session_id = c['session'].value
            db = shelve.open(DB_FILENAME)
            session = db[session_id]
        except KeyError:
            log("Session not found")
    return session

def update_session(session, key, value):
    if not key or not session or not value:
        logError("Missing parameters for update session method")
        return None
    try:
        db = shelve.open(DB_FILENAME, 'w')
        session = {}
        try:
            session = db[session_id]
        except:
            log("Creating session_id %s" % session)
        session[key] = value
        db[session_id] = session
        log("Updated session %s: %s = %s" % (session, key, value))
    except:
        logError("session not found for update session method")
        return None
