# Application Preferences
COOKIE_DOMAIN = 'www.example.com'
TITLE = "World's Simplest Web App"
EXPIRATION_IN_MINUTES = 30
TZ = 'EST+05EDT,M4.1.0,M10.5.0'

# Folders
CGI_BIN = '/usr/lib/cgi-bin'
DONT_INSTALL_LIST = ['setupDemo.py', 'cleanupDemo.py']

# Make sure these files are writable by the web server
APP_FOLDER = '/var/log/sampleapp'
DB_FILENAME = '%s/sessionDB' % APP_FOLDER
CONFIG_FILE_ORIGINAL = 'demosite.cfg'
CONFIG_FILE = '%s/demosite.cfg' % APP_FOLDER
LOG_FN = '%s/app.log' % APP_FOLDER

# Application URLs
HOME_URL = '/cgi-bin/home.cgi'
GET_AUTH_URL = '/cgi-bin/redirect-to-login.cgi'
GET_LOGOUT_URL = '/cgi-bin/redirect-to-logout.cgi'
LOGOUT_CONFIRM = '/cgi-bin/logout-confirmation.cgi'

# Resource Server URL
RS_BASE_URL = 'https://localhost:8085/'

DEMOSITE_CFG = """
[oxd]
host = localhost
port = 8099
id =

[client]
authorization_redirect_uri = https://%s/cgi-bin/callback-login.cgi
post_logout_redirect_uri = https://%s/cgi-bin/logout-confirmation.cgi
client_frontchannel_logout_uris = https://%s/cgi-bin/callback-logout.cgi
claims_redirect_uri = https://%s/cgi-bin/callback-claims.cgi
client_name = World's Simplest Web App
contacts = admin@example.com
scope = openid,email,profile
grant_types = client_credentials,authorization_code
"""
