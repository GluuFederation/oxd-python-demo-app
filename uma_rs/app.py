import os
import oxdpython
import random
import socket

from flask import Flask, request, jsonify, abort, make_response
from oxdpython.exceptions import InvalidRequestError, OxdServerError
from oxdpython.utils import ResourceSet

app = Flask(__name__)
app.config.from_object('app_config')
app.config['FIRST_RUN'] = True

this_dir = os.path.dirname(os.path.realpath(__file__))
config = os.path.join(this_dir, 'rs-oxd.cfg')
oxc = oxdpython.Client(config)


@app.route('/')
def index():
    if app.config.get('FIRST_RUN'):
        return setup_resource_server()
    return api()


@app.route('/setup/')
def setup_resource_server():
    rset = ResourceSet()

    for k, resource in app.config["RESOURCES"].iteritems():
        path = "/api/{0}/".format(k)
        if resource['protected']:
            r = rset.add(path)
            for method, scope in resource['scope_map'].iteritems():
                r.set_scope(method, scope)

    try:
        oxc.register_site()
        if not oxc.uma_rs_protect(rset.dump()):
            return jsonify({"error": "UMA protection failed. Check oxd-server logs."})
    except socket.error:
        return jsonify({"error": "Unable to connect to oxd-server."})
    except OxdServerError:
        return jsonify({"error": "Unknown internal oxd-server error."})

    app.config['FIRST_RUN'] = False
    return api()


@app.route('/api/')
def api():
    if app.config.get('FIRST_RUN'):
        return setup_resource_server()

    response = {
        "resources": [{
            "endpoint": "/api/{0}/".format(k),
            "uma_protected": app.config["RESOURCES"][k]["protected"]
        } for k in app.config["RESOURCES"].keys()],
    }
    return jsonify(response)


@app.route('/api/<rtype>/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def api_resource(rtype):
    """Function that fetches or adds a particular resource.

    :param rtype: resource type either photos or docs
    :return: json
    """
    if app.config.get('FIRST_RUN'):
        setup_resource_server()

    resources = app.config["RESOURCES"].keys()
    status = {'access': 'denied'}
    try:
        rpt = request.headers.get('Authorization')
        if rpt:
            rpt = rpt.split()[1]
        status = oxc.uma_rs_check_access(rpt=rpt, path=request.path,
                                         http_method=request.method)
    except socket.error as e:
        app.logger.error("Unable to connect to oxd-server.")
        status["error"] = "internal_error"
    except OxdServerError as e:
        app.logger.error(str(e))
        status["error"] = "internal_error"
    except InvalidRequestError as e:
        app.logger.error(str(e))
        status["error"] = "invalid_request"

    if "error" in status:
        # conform to https://docs.kantarainitiative.org/uma/wg/oauth-uma-grant-2.0-05.html#rfc.section.3.2.2
        response = make_response(
            status['access'],
            403,
            {"Content-Type": "text/plain", "Warning": '199 - "UMA Authorization Server Unreachable"'},
        )
        return response

    if not status['access'] == 'granted':
        response = make_response(status['access'], 401, {"Content-Type": "text/plain"})
        if 'www-authenticate_header' in status:
            response.headers['WWW-Authenticate'] = status['www-authenticate_header']
        return response

    if rtype not in resources:
        abort(404)

    resource = app.config["RESOURCES"][rtype]['content']

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
    app.run(ssl_context='adhoc')
