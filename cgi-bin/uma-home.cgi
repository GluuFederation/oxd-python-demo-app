#!/usr/bin/python

import urllib2
import ssl
import json
import traceback
import Cookie
import os
import cgi
import oxdpython
import sys
import urlparse

from constants import *
from common import *
from oxdpython.exceptions import NeedInfoError

client = oxdpython.Client(CONFIG_FILE)

html = """<HTML><HEAD><TITLE>%(title)s</TITLE></HEAD>
<BODY>
<H1>%(title)s</H1>

<h3>Available Resource Endpoints</h3>
<table>
    <tr>
        <th>API Endpoint</th>
        <th>UMA Protection Status</th>
        <th>Action</th>
    </tr>
    
    %(endpoints)s
        
</table>
<hr>

<h3>UMA RPT Access Token Token</h3>
<pre><code>
%(rpt_token)s
</code></pre>
<hr>

<h3>PCT</h3>
<pre><code>
%(pct)s
</code></pre>
<hr>

%(message)s
<hr>
<h6>POWERED BY</h6>
<IMG SRC="https://www.gluu.org/wp-content/themes/gluu/images/logo.png" alt="Powered by Gluu"
 width="100" />
</BODY>
</HTML>
"""
TITLE = "UMA RP Home Page"

if hasattr(ssl, 'create_default_context'):
    ctx = ssl.create_default_context()
else:
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

c = Cookie.SimpleCookie()
if 'HTTP_COOKIE' in os.environ:
    cookie_string = os.environ['HTTP_COOKIE']
    c.load(cookie_string)

# Get and list API endpoints
try:
    response = urllib2.urlopen(RS_BASE_URL, context=ctx)
    resources = json.loads(response.read())['resources']
    # Generate html links
    link_template = """
    <tr>
        <td>
            {endpoint}
        </td>
        <td>{uma_protected}</td>
        <td> 
            <a href="/cgi-bin/uma-home.cgi?api={endpoint}">Get Resource</a>
        </td>
    </tr>
    """
    links = [link_template.format(**r)
             for r in resources]
    endpoints = "\n".join(links)
    message = "Click on <strong>Get Resource</strong> to fetch the resource"
except urllib2.HTTPError:
    endpoints = ""
    message = "Failed to get resources from the UMA RS"
    logError(message)
    logException(traceback.format_exc())
except TypeError:
    endpoints = ""
    message = "The data received from the UMA RS doesn't meet expectation."
    logError(message)
    logException(traceback.format_exc())


def get_resource(url, token_type, access_token):
    """Makes a request to the given URL using the token type and access token
    available in the cookie as the Authorization header. It clears the
    access_token from the cookie after using it

    :param url: url of the resource to access
    :param token_type: token type from RPT
    :param access_token: access token from RPT
    :return: response message or an error message as string
    """
    try:
        log("Requesting resource with RPT: %s" % url)
        req = urllib2.Request(url)
        req.add_header('Authorization', '%s %s' % (token_type, access_token))
        reply = urllib2.urlopen(req, context=ctx)
        msg = "Response from Resource Server: <pre>%s</pre>" % reply.read()
    except:
        msg = 'Request for resource at %s failed. See logs.' % api_url
        logError(msg)
        logException(traceback.format_exc())

    return msg


def get_ticket(url):
    """Makes a plain HTTP GET request to the url expecting a 401 Unauthorized,
    then parses the ticket from the response and returns it.

    :param url: url to call
    :return: ticket if 'www-authenticate' is available in headers, None otherwise
    """
    try:
        log("Requesting ticket from RS for url: %s" % url)
        urllib2.urlopen(url, context=ctx)
        # the request is expected to fail, if it succeeds, then no ticket
        ticket = None
    except urllib2.HTTPError as error_response:
        # Expect a 401 response when the RPT is empty
        if 'www-authenticate' in error_response.headers:
            log("Received 401 with www-authenticate header. Redirecting to get RPT.")
            www_auth = error_response.headers['www-authenticate']
            auth_values = dict(x.split('=') for x in www_auth.split(','))
            ticket = auth_values['ticket'].strip("\"")
        else:
            ticket = None
    except:
        ticket = None
        logError("Request for ticket failed.")
        logException(traceback.format_exc())
    return ticket


def fetch_rpt(ticket, cookie):
    """Fetches RPT using the ticket and stores the obtained values in the cookie

    :param ticket: ticket to be passed to the oxd server to get RPT
    :param cookie: cookie to store the received values
    :return: message if any
    """
    try:
        rpt = client.uma_rp_get_rpt(ticket)
        cookie['access_token'] = rpt['access_token']
        cookie['token_type'] = rpt['token_type']
        cookie['pct'] = rpt['pct']
        fail_message = None
    except NeedInfoError as ne:
        if 'redirect_user' in ne.details:
            log("Redirecting user to the Authorization server")
            claims_url = client.uma_rp_get_claims_gathering_url(ne.details['ticket'])
            print "Location: %s\r\n" % claims_url
            print ""
            print "Redirecting"
            sys.exit()
        else:
            fail_message = "Received NeedInfo Error, but no redirect flag present."
            logError(fail_message)
            logException(traceback.format_exc())
    except:
        fail_message = "Failed to get RPT. Look at logs."
        logError(fail_message)
        logException(traceback.format_exc())
    return fail_message

# Request the resources if requested by the user
fs = cgi.FieldStorage()
if 'api' in fs:
    api_url = urlparse.urljoin(RS_BASE_URL, fs.getfirst('api'))
    if 'token_type' in c and 'access_token' in c:
        token_type = c.get('token_type').value
        access_token = c.get('access_token').value
        message = get_resource(api_url, token_type, access_token)
    else:
        ticket = get_ticket(api_url)
        fail_msg = fetch_rpt(ticket, c)
        if fail_msg:
            message = fail_msg
        else:
            message = get_resource(api_url, c)

    c['access_token'] = ''
    c['access_token']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    c['token_type'] = ''
    c['token_type']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'

# When the page is called after claims gathering by the Auth Server
if 'ticket' in fs:
    ticket = fs.getfirst('ticket')
    state = fs.getfirst('state')
    fail_msg = fetch_rpt(ticket, c)
    if not fail_msg:
        message = "RPT has been obtained. Click <strong>Get Resource</strong>"

d = {}
d['title'] = TITLE
d['message'] = message
d['rpt_token'] = c.get('access_token').value if 'access_token' in c else "No RPT present"
d['pct'] = c.get('pct').value if 'pct' in c else "No PCT present"
d['endpoints'] = endpoints

print "Content-type: text/html\r\n"
print ""
print html % d

