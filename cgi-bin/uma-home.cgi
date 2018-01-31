#!/usr/bin/python

import urllib2
import ssl
import json
import traceback
import Cookie
import os
import cgi
import oxdpython

from constants import *
from common import *
from oxdpython.exceptions import NeedInfoError

client = oxdpython.Client(CONFIG_FILE)

html = """<HTML><HEAD><TITLE>%(title)s</TITLE></HEAD>
<BODY>
<H1>%(title)s</H1>

<p>Available Resource Endpoints</p>
<table>
    <tr>
        <th>API Endpoint</th>
        <th>UMA Protection Status</th>
        <th>Action</th>
    </tr>
    
    %(endpoints)s
        
</table>

<p>UMA RPT Access Token Token</p>
<pre><code>
%(rpt_token)s
</code></pre>

<p>PCT</p>
<pre><code>
%(pct)
</code></pre>

%(message)s
<hr>
<h6>POWERED BY</h6>
<IMG SRC="https://www.gluu.org/wp-content/themes/gluu/images/logo.png" alt="Powered by Gluu"
 width="100" />
</BODY>
</HTML>
"""
TITLE = "UMA RP Home Page"

ctx = ssl.create_default_context()
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
            <a href="/cgi-bin/uma-home.cgi?api={endpoint}">Request Resource</a>
        </td>
    </tr>
    """
    links = [link_template.format(**r)
             for r in resources]
    endpoints = "\n".join(links)
    message = "Click on <strong>Request Resource</strong> to fetch the resource"
except urllib2.HTTPError:
    message = "Failed to get resources from the UMA RS"
    logError(message)
    logException(traceback.format_exc())
except TypeError:
    message = "The data received from the UMA RS doesn't meet expectation."
    logError(message)
    logException(traceback.format_exc())

# Check if there is any RPT token stored and set it up
if 'token_type' in c and 'access_token' in c:
    rpt_token = "{0} {1}".format(c.get('token_type'), c.get('access_token'))
else:
    rpt_token = "No RPT Token present"

# Check if there is PCT
if 'pct' in c:
    pct = c.get("pct")
else:
    pct = "No PCT present"

# Request the resources if requested by the user
fs = cgi.FieldStorage()
api_url = fs.getfirst('api', '')

def get_resource(url, token_type, access_token):
    """Makes a request to the given URL using the token type and access token
    as the Authorization header

    :param url: url of the resource to access
    :param token_type: token type specified in the RPT
    :param access_token: access token provided by the RPT
    :return: response message or an error message as string
    """
    try:
        log("Requesting resource with RPT: %s" % url)
        req = urllib2.Request(url)
        req.add_header('Authorization', '%s %s' % (token_type, access_token))
        response = urllib2.urlopen(req, context=ctx)
        message = "Response from Resource Server: <pre>%s</pre>" % response.read()
    except:
        message = 'Request for resource at %s failed. See logs.' % api_url
        logError(message)
        logException(traceback.format_exc())
    return message

def get_ticket(url):
    """Makes a plain HTTP GET request to the url expecting a 401 Unauthorized,
    then parses the ticket from the response and returns it.

    :param url: url to call
    :return: ticket if 'www-authenticate' is available in headers, None otherwise
    """
    try:
        log("Requesting ticket from RS")
        urllib2.urlopen(api_url, context=ctx)
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


if api_url:
    api_url = RS_BASE_URL + api_url
    # After claims-gathering the callback redirects with the ticket
    if fs.getfirst('authorization_state') == 'claims_submitted':
        ticket = fs.getfirst('ticket')
    elif fs.getfirst('authorization_state') != 'claims_submitted':
        ticket = fs.getfirst('ticket')
        logError("Received authorization state: %s" % fs.getfirst('authorization_state'))
        message = "Unsuitable Authorization State: %s" % fs.getfirst('authorization_state')
    else:
        # In case of the resource request, new ticket is generated
        ticket = get_ticket(api_url)

    try:
       rpt = client.uma_rp_get_rpt(ticket)
       message = get_resource(api_url, rpt['token_type'], rpt['access_token'])
    except NeedInfoError as ne:
        if 'redirect_user' in ne.details:
            message = "Redirecting user to the Authorization server"
            log(message)
            claims_url = client.uma_rp_get_claims_gathering_url(ne.details['ticket'])
            print "Location: %s\r\n" % claims_url
            print ""
            print "Redirecting"
        else:
            message = "Received NeedInfo Error, but no redirect flag present."
            logError(message)
            logException(traceback.format_exc())
    except:
        message = "Failed to get RPT. Look at logs."
        logError(message)
        logException(traceback.format_exc())


d = {}
d['title'] = TITLE
d['message'] = message
d['rpt_token'] = rpt_token
d['pct'] = pct

print "Content-type: text/html\r\n"
print ""
print html % d

