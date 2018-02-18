# Welcome to the uma_rs Demo!

The goal of uma_rs is to demonstrate how an API programmer can use UMA to
protect API's by making the right calls to oxd.

In UMA, the RS is the thing that has the API's. The RS knows which scopes are required to call it's API's. It is the policy enforcement point--it must decide whether to give access to a client, based on a bearer token issued by the Authorization Server.

## Prerequisites

* Gluu Server 3.1.2
* oxd 3.1.2
* oxd-python 3.1.2

## Configuration

Review the config files for flask `app_config.py` and oxd `rs-oxd.cfg`

### app_config.py

The file contains the standard flask variables like
`SERVER_NAME` and `SECRET_KEY` and `DEBUG`.

uma_rs defines a new flask variable called `RESOURCES`, which enables you
to manage the API's of your uma_rs. Each `RESOURCES` key is an API.
So for example, the default `app_config.py` in this project defines
two API's: `/docs` and `/photos`.

The resource entry itself is a dictionary with three possible keys:

* `content` - The static JSON data returned by the API
* `protected` - are UMA access tokens required to call this API?  
* `scope_map` - Maps which HTTP methods require which UMA scopes.

### rs-oxd.cfg

oxd-python configuration file provides information used for
client registration. Make sure the `oxd` parameters for
host and port are correct. You can use the default `client`
parameters. For more information on how to make a configuration
file for oxd-python, see the [oxd-python docs](https://github.com/GluuFederation/oxd-python)

## Running uma_rs

```
$ cd ../uma_rs
$ nohup python app.py > uma_rs.log 2>&1 &
$ curl -k https://localhost:8085/api/
```

The `curl` command above should return a JSON document listing the api's
defined as `RESOURCES` in `app_config.py`.

### Endpoints and responses

1. Home `curl -k https://localhost:8085/`

```json
{
  "resources": [
    {
      "endpoint": "/api/photos",
      "uma_protected": true
    },
    {
      "endpoint": "/api/docs",
      "uma_protected": false
    }
  ]
}
```

2. API `curl -k https://localhost:8085/api/`

```json
{
  "resources": [
    {
      "endpoint": "/api/photos",
      "uma_protected": true
    },
    {
      "endpoint": "/api/docs",
      "uma_protected": false
    }
  ]
}
```

3. Protected resource (/photos/) `curl -ki https://localhost:8085/api/photos/`
```http request
HTTP/1.0 401 UNAUTHORIZED
Content-Type: text/plain
Content-Length: 6
WWW-Authenticate: UMA realm="rs",as_uri="https://gluu.example.com",error="insufficient_scope",ticket="55268b6e-1590-4718-99c8-d99b24c079d4"
Server: Werkzeug/0.12.2 Python/2.7.14
Date: Fri, 26 Jan 2018 10:39:05 GMT

denied
```

4. Unprotected Resource (/docs/) `curl -ki https://localhost:8085/api/docs/`
```http request
HTTP/1.0 401 UNAUTHORIZED
Content-Type: text/plain
Content-Length: 6
Server: Werkzeug/0.12.2 Python/2.7.14
Date: Fri, 26 Jan 2018 10:41:03 GMT

denied
```

### Typical Resource Access Cycle

**Note:** Ideally all this should be done by a separate UMA Requesting Party App. We are using `curl` here.

1. Access the URL `https://localhost:8085/api/photos/` from a REST client.
```bash
$ curl -k -i https://localhost:8085/api/photos/
HTTP/1.0 401 UNAUTHORIZED
Content-Type: text/html; charset=utf-8
Content-Length: 6
WWW-Authenticate: UMA realm="rs",as_uri="https://gluu.example.com",error="insufficient_scope",ticket="6cbfe25d-c504-40c8-9326-17be6c07bfb2"
Server: Werkzeug/0.12.2 Python/2.7.14
Date: Wed, 24 Jan 2018 13:50:26 GMT

denied
```
2. Use the **ticket** from the response's `WWW-Authenticate` header in the Requesting Party to generate RPT Token.
This step is beyond the scope of this application and you should refer to the CGI app in this repository on how
to get a RPT token as the Requesting Party.
```json
{
  "access_token": "ebe71635-1c24-470c-830c-7bc961e33457_140A.BA5B.556E.9842.0E8F.EFF7.F0AF.12E9",
  "pct": "ed0ce518-ebfd-41ae-b3a6-c6a6a9d8f440_5F41.AB57.0892.31D3.D786.CFB4.CF9D.D32C",
  "token_type": "Bearer",
  "updated": false
}
```
3. Now access the resource with the RPT access token
```bash
$ curl -k -H 'Authorization: Bearer ebe71635-1c24-470c-830c-7bc961e33457_140A.BA5B.556E.9842.0E8F.EFF7.F0AF.12E9' https://localhost:8085/apt/photos/
{
    "photos": {
        "contents": [
            {
                "filename": "https://example.com/photo1.jpg",
                "id": 1
            }
        ],
        "protected": true
    }
}
```
Voila here is our resource.

Happy building UMA apps with oxd-python.
