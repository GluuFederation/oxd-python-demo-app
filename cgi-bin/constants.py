# Folders
CGI_BIN = "/usr/lib/cgi-bin"

# Make sure these files are writable by the web server
APP_FOLDER = "/var/log/sampleapp"
DB_FILENAME = "%s/sessionDB" % APP_FOLDER
CONFIG_FILE_ORIGINAL = 'demosite.cfg'
CONFIG_FILE = '%s/demosite.cfg' % APP_FOLDER
LOG_FN = '%s/app.log' % APP_FOLDER

# Application Preferences
TITLE = "World's Simplest Web App"
COOKIE_DOMAIN = "www.example.com"
EXPIRATION_IN_MINUTES = 30
TZ = "EST+05EDT,M4.1.0,M10.5.0"

# Application URLs
HOME_URL = "/cgi-bin/home.cgi"
GET_AUTH_URL = "/cgi-bin/redirect-to-login.cgi"
GET_LOGOUT_URL = "/cgi-bin/redirect-to-logout.cgi"
LOGOUT_CONFIRM = "/cgi-bin/logout-confirmation.cgi"

# Resource Server URL
RS_BASE_URL = "https://localhost:8085/"
