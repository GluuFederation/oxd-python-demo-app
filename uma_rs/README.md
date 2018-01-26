# UMA RS App

This is a sample application to demonstrate a UMA Resource Server
and requesting party using oxd.

## Files

* `app.py` - A simple flask application
* `app_config.py` - The configuration for the Flask application
* `rs-oxd.cfg` - oxd-python config file

## Demo Application

### What does the app do?

* The app acts as a UMA Resource server.
* When either of the endpoints `/api/photos/` or `/api/docs` is accessed, it checks the Auth Server for access and returns a response based on the Auth Server's answer.

### Prerequisites

* A Gluu Server to act as the Authorization Server
* oxd-server or oxd-https-extension configured with the Gluu server as its `op_host`.

### Running the app

```commandline
# apt install python-pip
# pip install oxdpython
# cd ~
# git clone https://github.com/GluuFederation/oxd-python-demo-app.git
# cd oxd-python-demo-app/uma_rs
# python app.py
```

Run `curl -k https://localhost:8085/` for API details.

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
