# Use the hostname of your web server here.
# Also used as hostname of redirect uri's
COOKIE_DOMAIN = 'www.example.com'

# Folders
CGI_BIN = '/usr/lib/cgi-bin'      # check apache2 conf for cgi-bin path
APP_FOLDER = '/var/log/sampleapp' # Writable by the web server :-(

# Files
DB_FILENAME = '%s/sessionDB' % APP_FOLDER
CONFIG_FILE_ORIGINAL = 'demosite.cfg'
CONFIG_FILE = '%s/demosite.cfg' % APP_FOLDER
LOG_FN = '%s/app.log' % APP_FOLDER

# Application URLs
HOME_URL = '/cgi-bin/home.cgi'
GET_AUTH_URL = '/cgi-bin/redirect-to-login.cgi'
GET_LOGOUT_URL = '/cgi-bin/redirect-to-logout.cgi'
LOGOUT_CONFIRM = '/cgi-bin/logout-confirmation.cgi'

<<<<<<< HEAD
# Other stuff
DONT_INSTALL_LIST = ['setupDemo.py', 'cleanupDemo.py']
RS_BASE_URL = 'https://localhost:8085/'
TITLE = "World's Simplest Web App"
EXPIRATION_IN_MINUTES = 30
TZ = 'EST+05EDT,M4.1.0,M10.5.0'
=======
# Resource Server URL
RS_BASE_URL = 'https://localhost:8085'
>>>>>>> origin/master

# oxd config file template
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
