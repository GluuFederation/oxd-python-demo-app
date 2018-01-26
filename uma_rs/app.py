import os
import oxdpython
import random

from app_config import RESOURCES

from flask import Flask, request, jsonify, abort, make_response
from oxdpython.exceptions import InvalidRequestError

app = Flask(__name__)
this_dir = os.path.dirname(os.path.realpath(__file__))
config = os.path.join(this_dir, 'rs-oxd.cfg')
oxc = oxdpython.Client(config)

app.config['FIRST_RUN'] = True

@app.route('/')
def index():
    if app.config.get('FIRST_RUN'):
        return setup_resource_server()
    return api()

@app.route('/setup/')
def setup_resource_server():
    oxc.register_site()
    resources = []
    protected = []
    unprotected = []
    for k, resource in RESOURCES.iteritems():
        path = "/api/{0}/".format(k)
        if resource['protected']:
            scope_map = resource['scope_map']
            conditions = [{"httpMethods": [method], "scopes": scopes}
                          for method, scopes in scope_map.iteritems()]
            resources.append({
                "path": path,
                "conditions": conditions
            })
            protected.append(path)
        else:
            unprotected.append(path)

    if not oxc.uma_rs_protect(resources):
        return jsonify({"error": "UMA protection failed. Check oxd-server logs."})

    response_dict = {
        'protected_resources': protected,
        'unprotected_resources': unprotected
    }

    app.config['FIRST_RUN'] = False
    return jsonify(response_dict)

@app.route('/api/')
def api():
    if app.config.get('FIRST_RUN'):
        return setup_resource_server()

    response = {
        "resource_endpoints": ["/api/{0}".format(k) for k in RESOURCES.keys()],
        "resources": RESOURCES
    }
    return jsonify(response)

@app.route('/api/<rtype>/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def api_resource(rtype):
    """Function that fetches or adds a particular resource.

    :param rtype: resource type either photos or docs
    :return: json
    """
    if app.config.get('FIRST_RUN'):
        return setup_resource_server()

    resources = RESOURCES.keys()
    status = {'access': 'denied'}
    try:
        rpt = request.headers.get('Authorization')
        if rpt:
            rpt = rpt.split()[1]
        status = oxc.uma_rs_check_access(rpt=rpt, path=request.path,
                                         http_method=request.method)
    except InvalidRequestError as e:
        print str(e)
        print request.path, " is unprotected. Denying access."

    if not status['access'] == 'granted':
        response =  make_response(status['access'], 401)
        if 'www-authenticate_header' in status:
            response.headers['WWW-Authenticate'] = status['www-authenticate_header']
        return response

    if rtype not in resources:
        abort(404)

    resource = RESOURCES[rtype]

    if request.method == 'GET':
        return jsonify({rtype: resource})

    if request.method == 'POST':
        data = request.get_json()
        if 'filename' in data:
            item = {'id': random.randint(0, 1000), 'filename': data['filename']}
            resource.append(item)
            return make_response(jsonify(item), 201)
        else:
            abort(400)


if __name__ == '__main__':
    app.config.from_object('app_config')
    app.run(ssl_context='adhoc')
