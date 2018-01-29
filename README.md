# Demo CGI

The goal of this app is to show oxd-python at work with a minimal
amount of application overhead. A cookie is used to track a session id,
which is persisted using the simple python shelve database interface.

## Table of Contents

* [Scripts in cgi-bin folder](#scripts-in-cgi-bin-folder)
* [Deployment Instructions (Ubuntu 14/16)](#deployment-instructions-ubuntu-14-16)
    - [Install oxd](#install-oxd)
    - [Install Python Dependencies](#install-python-dependencies)
    - [Install and Configure Apache 2](#install-and-configure-apache-2)
    - [Install Demo](#install-demo)
    - [Setup demo UMA Resource Server](#setup-demo-uma-resource-server)
* [Demo](#demo)
    - [OpenID Connect](#openid-connect)
    - [UMA Requesting Party](#uma-requesting-party)
* [Troubleshooting](#troubleshooting)
* [Uninstall Demo](#uninstall-demo)


## Scripts in cgi-bin folder

*Properties*
* **constants.py** General Application properties: _Check paths, hostnames and ports_

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
* **uma_rs** Folder contains a Flask app that runs on port localhost:8085
* **uma-home.cgi** Script that lists the resource endpoints in the UMA Resource
Server
* **request-resource.cgi** Script that requests data from UMA Resource Server
* **get-rpt.cgi** Script that gets the RPT token from the Auth Server
* **callback-claims.cgi** The script parses the response from Authorization
Server if claims gathering was necessary.

*Helper modules*
* **appLog.py** Module to centralize logging code
* **common.py** Place to put some shared methods

## Deployment Instructions (Ubuntu 14/16)

###  Install oxd

1. Install [oxd-server](https://gluu.org/docs/oxd/install/)
2. Edit `/opt/oxd-server/conf/oxd-conf.json` and enter server name and your oxd license details.
Set `uma2_auto_register_claims_gathering_endpoint_as_redirect_uri_of_client` to false.
3. Edit `/opt/oxd-server/conf/oxd-default-site-conf.json` and for`op_host`,
specify the Gluu Server hostname.
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

1. `$ git clone https://github.com/GluuFederation/oxd-python-demo-app.git`
1. `$ cd oxd-python-demo-app/cgi-bin`
1.  Update the value for `COOKIE_DOMAIN` in `constants.py`, and any other system
properties to suit your preference.
1. `$ sudo python setupDemo.py`

### Setup demo UMA Resource Server

```
$ cd ../uma_rs
$ nohup python app.py > uma_rs.log 2>&1 &
```
**Note:**
1. This server will be accessible only via localhost and will be used by the CGI app to demonstrate UMA.
You can run `curl -k https://localhost:8085/api/` to know the API details provided by the RS app.
2. To stop the server, note down the PID returned by the *nohup* command and run `sudo kill <pid>`

## Demo

### OpenID Connect

The url for your application will be `https://your-hostname/cgi-bin/home.cgi`

![home](images/home.png)

![visiting authorization URL](images/login.png)

![authorizing app](images/authorize.png)

![session active](images/session-active.png)

![logout confirmation](images/logout-confirmation.png)

### UMA Requesting Party

To test UMA, visit `https://your-hostname/cgi-bin/uma-home.cgi`

![uma home](images/uma-home.png)

![request resource](images/uma-request-fail.png)

![get rpt](images/uma-get-rpt.png)

![home with rpt](images/uma-home-with-rpt.png)

![resource obtained](images/uma-request-success.png)


## Troubleshooting

* Make sure that the web server can be reached by your local browser. You should
also make sure that the server that is running the cgi scripts can reach the
hostname of the Gluu Server (i.e. use DNS or update your `/etc/hosts` file).

* To debug, check the application log, which defaults to
`/var/log/samleapp/app.log`, and the oxd log in `/var/log/oxd-server.log`

* You should be able to login using an existing account on your Gluu Server.


## Uninstall demo

```
$ cd oxd-python-demo-app/cgi-bin
$ sudo python cleanupDemo.py
```
