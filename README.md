## Demo CGI

CGI scripts are the simplest possible Web applications. The goal of
these scripts is to show oxd-python at work with a minimal amount of
application overhead. A cookie is used to track a session id, which
is persisted using the simple python shelve database interface.

This sample consists of the following files

* **home.cgi** This is the main page of the app. Navigate to this page
first.
* **constants.py** Module to centralize demo app properties
* **demosite.cfg** This file contains the oxd configuration properties
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
* **setupDemo.py** Helper script used to create the DB and set
file permissions.
* **appLog.py** Module to centralize logging code
* **request-resource.cgi** Script that requests data from UMA Resource Server
* **get-rpt.cgi** Script that gets the RPT token from the Auth Server
* **callback-claims.cgi** The script parses the response from Authorization
server and send the ticket to re-fetch RPT on successful authorization

## Deployment of demosite in Ubuntu

1. Install [oxd-server](https://gluu.org/docs/oxd/install/)
2. Edit `/opt/oxd-server/conf/oxd-conf.json` and enter your oxd license details.
Set `uma2_auto_register_claims_gathering_endpoint_as_redirect_uri_of_client` to false.
3. Edit `/opt/oxd-server/conf/oxd-default-site-conf.json` and enter the value for
`op_host` pointing to your Gluu Server installation. Run `service gluu-oxd-server start`.
4. Install oxd-python
    ```
    # apt install python-pip
    # pip install oxdpython
    ```
5. Install and configure Apache 2
    ```
    # apt install apache2
    # a2enmod cgi
    # a2enmod ssl
    # a2dissite 000-default
    # a2ensite default-ssl
    # service apache2 reload
    ```
6. Edit the properties in `constants.py` and `demosite.cfg` as appropriate for
your environment.
7. Setup logging and initialize the app
    ```
    # mkdir -p /var/log/sampleapp/
    # python setupDemo.py
    ```
10. Visit `https://your-hostname/cgi-bin/home.cgi`
11. To debug check the logs are `/var/log/sampleapp/app.log` and `/var/log/oxd-server.log`

## UMA Demo

Let us set up the three components required for UMA:
* Authorization Server (AS)  - The Gluu server set as OP host - Already Setup
* Requesting Party (RP) - `request-resource.cgi` - Already present as a part of this demo app
* Resource Server (RS) - The Flask app inside the `uma_rs` directory - Follow instructions below

### Set up demo UMA Resource Server

1. Open a new terminal window and navigate to the `uma_rs` directory
    ```
    # cd /usr/lib/cgi-bin/oxd-python/examples/cgi_app/uma_rs
    ```
2. Install requirements for the app
    ```
    # pip install flask pyOpenSSL
    ```
3. Edit the config file `rs-oxd.cfg` and input the `op_host` you are using. The `authorization_redirect_uri`
   is a part of the of the OAuth Spec requirement. You DON'T have to have a resolving URL, you can leave the dummy value
   in place.
4. Run `python app.py` to start the server.
5. From the old terminal window run `curl https://localhost:8085/setup/`. This will register the demo resources in
   the Authorization Server and give you a response containing the details of the resources and their endpoints.

### Seeing UMA RP in action

1. Visit `https://<your-hostname>/cgi-bin/request-resource.cgi`, based on the requirements and configured policies,
the links should get you the resource from the resource server.
