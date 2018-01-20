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
* Once endpoints are protected with required *Scopes* and *Http Methods*, they can be accessed to verify the protection.
* When either of the endpoints `/resource/photos/` or `/resource/docs` is accessed, it asks the AS for validity and returns a response based on the Auth Server's answer.

### Prerequisites

* A Gluu Server to act as the Authorization Server. Use this server's URL
as `op_host` in the configuration `rs-oxd.cfg`
* oxd-server or oxd-https-extension

### Running the app

```
# apt install python-pip
# pip install oxdpython
# cd /usr/local
# git clone https://github.com/GluuFederation/oxd-python.git
# cd oxd-python/examples/uma_rs/

# Edit the rs-oxd.cfg to suit your op_host
# remove the line with oxd_id if present

# run the application
python app.py
```

Now the RS site should be available at `https://localhost:8085`

### Endpoints

-----------------------------------------------------
|  Endpoint  | Methods           | Description      |
|------------|-------------------|------------------|
| `/`        | GET               | Home page of the application |
| `/protect` | POST              | URL where the form is submitted from the homepage for resource protection. |
| `/api/<resource>/` | GET, POST | API for accessing and the resource. `resource`s are *docs* and *photos* |
-------------------------------------------------------------


### Typical Resource Protection & Access Cycle

#### Resource Protection

When the first run the app, a "Setup" link is provided. Clicking it sets up the app with necessary protections.


#### Resource Access

**Note:** Ideally all this should be done by a separate UMA Requesting Party App. For the RS example, lets just use `cURL`

1. Access the URL `https://localhost:8085/api/photos/` from a REST client.
```
$ curl -k https://localhost:8085/api/photos/
{
  "access": "denied",
  "ticket": "030db88e-f07f-4558-bd17-3ac2a7400be3",
  "www-authenticate_header": "UMA realm=\"rs\",as_uri=\"https://gluu.example.com\",error=\"insufficient_scope\",ticket=\"030db88e-f07f-4558-bd17-3ac2a7400be3\""
}
```
2. Use the Requesting Party to generate RPT Token.
```
{
  "access_token": "ebe71635-1c24-470c-830c-7bc961e33457_140A.BA5B.556E.9842.0E8F.EFF7.F0AF.12E9",
  "pct": "ed0ce518-ebfd-41ae-b3a6-c6a6a9d8f440_5F41.AB57.0892.31D3.D786.CFB4.CF9D.D32C",
  "token_type": "Bearer",
  "updated": false
}
```
3. Now access the resource with the RPT access token
```
curl -k -H 'Authorization: Bearer ebe71635-1c24-470c-830c-7bc961e33457_140A.BA5B.556E.9842.0E8F.EFF7.F0AF.12E9' https://localhost:8085/apt/photos/
{
    "photos": [
        {
            "filename": "https://example.com/photo1.jpg",
            "id": 1
        }
    ]
}
```
Voila here is our resource.

Happy building UMA apps with oxd-python.
