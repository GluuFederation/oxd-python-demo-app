# Folders
CGI_BIN = "/usr/lib/cgi-bin"

# Make sure these files are writable by the web server
DB_FILENAME = "/var/log/sampleapp/sessionDB"
CONFIG_FILE_ORIGINAL = 'demosite.cfg'
CONFIG_FILE = '/var/log/sampleapp/demosite.cfg'
LOG_FN = '/var/log/sampleapp/app.log'

# Application Preferences
TITLE = "World's Simplest Web App"
COOKIE_DOMAIN = "squid.gluu.info"
EXPIRATION_IN_MINUTES = 30
TZ = "EST+05EDT,M4.1.0,M10.5.0"

# Application URLs
HOME_URL = "/cgi-bin/home.cgi"
GET_AUTH_URL = "/cgi-bin/redirect-to-login.cgi"
GET_LOGOUT_URL = "/cgi-bin/redirect-to-logout.cgi"
LOGOUT_CONFIRM = "/cgi-bin/logout-confirmation.cgi"

# Resource Server URL
RS_BASE_URL = "https://localhost:8085/"
