# Demo CGI

## Overview

The goal of these scripts is to show oxd-python at work with a minimal
amount of application overhead. A cookie is used to track a session id,
which is persisted using the simple python shelve database interface.

*Properties*
* **constants.py** General Application properties: _Check paths, hostnames and ports_
* **demosite.cfg** oxd properties: _Update with your web URL_

*Helper scripts to install / uninstall*
* **setupDemo.py** Helper script used to create app folder and install cgi scripts.
* **cleanupDemo.py** Removes app folder and cgi-bin scripts.

*OpenID Connect demo*
* **home.cgi** This is the main page of the app. Navigate to this page
first.
* **redirect-to-login.cgi** This script gets the right authorization url from
oxd, and redirects the user's browser there for authentication / authorization.
* **callback-login.cgi** Script that runs post-authorization. The script
gets the `code` and `state` and requests tokens and user_info from oxd.
* **redirect-to-logout.cgi** Script that gets the right logout url from oxd,
and redirects the user's browser there for OpenID Connect front channel logout.
* **callback-logout.cgi** This page is called by OpenID Connect
front channel logout. It clears the session and cookie, and redirects
to the logout confirmation page
* **logout-confirmation.cgi** This pages checks to make sure that the
cookie and DB session are removed.
file permissions.

*UMA demo*
* **request-resource.cgi** Script that requests data from UMA Resource Server
* **get-rpt.cgi** Script that gets the RPT token from the Auth Server
* **callback-claims.cgi** The script parses the response from Authorization
server and send the ticket to re-fetch RPT on successful authorization

*helper modules*
* **appLog.py** Module to centralize logging code
* **common.py** Place to put some shared methods

## Deployment instructions (Ubuntu 14)

###  Install oxd

If you haven't installed oxd, as root you will need to do the following.

1. Install [oxd-server](https://gluu.org/docs/oxd/install/)
2. Edit `/opt/oxd-server/conf/oxd-conf.json` and enter your oxd license details.
Set `uma2_auto_register_claims_gathering_endpoint_as_redirect_uri_of_client` to false.
3. Edit `/opt/oxd-server/conf/oxd-default-site-conf.json` and enter the value for
`op_host` pointing to your Gluu Server installation.
4. Start oxd-server `/etc/init.d/oxd-server start`

### Install python dependencies

```
# apt install python-pip
# pip install oxdpython flask pyOpenSSL
```
    
### Install and configure Apache 2

As root, install the following commands to enable ssl and cgi.

```
# apt install apache2
# a2enmod cgi
# a2enmod ssl
# a2dissite 000-default
# a2ensite default-ssl
# service apache2 restart
```

### Install demo

Do the following as a local user. 

```
 $ git clone https://github.com/GluuFederation/oxd-python-demo-app.git
 $ cd oxd-python-demo-app/cgi-bin
```

* Update the value for `COOKIE_DOMAIN` in `constants.py`
* Change the domain in `demosite.cfg` for your environment.
* Setup demo
```
 $ sudo python setupDemo.py
```

### Set up demo UMA Resource Server

1. Open a new terminal window and navigate to the `uma_rs` directory
```
$ cd /usr/lib/cgi-bin/oxd-python/examples/cgi_app/uma_rs
```
2. Run `$ nohup python app.py > uma_rs.log 2>&1 &` to start the demo RS server. This server will be accessible only at `https://localhos:8085/`
3. Run `curl -k https://localhost:8085/api/` for the details about the available API.

### Testing

The url for your application will be `https://your-hostname/cgi-bin/home.cgi`

Make sure that the web server can be reached by your local browser. You should
also make sure that the server that is running the cgi scripts can reach the
hostname of the Gluu Server (i.e. use DNS or update your `/etc/hosts` file).

To debug, check the application log, which defaults to
`/var/log/samleapp/app.log`, and the oxd log in `/var/log/oxd-server.log`

You should be able to login using an existing account on your Gluu Server.

To test UMA, visit `https://your-hostname/cgi-bin/request-resource.cgi`

### Uninstall demo

```
$ cd oxd-python-demo-app/cgi-bin
$ sudo python cleanupDemo.py
```
