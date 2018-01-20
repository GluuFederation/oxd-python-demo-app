import os
import oxdpython
import random

from app_config import SCOPE_MAP, RESOURCES

from flask import Flask, render_template, request, jsonify, abort, make_response

app = Flask(__name__)
this_dir = os.path.dirname(os.path.realpath(__file__))
config = os.path.join(this_dir, 'rs-oxd.cfg')
oxc = oxdpython.Client(config)

app.config['FIRST_RUN'] = True


@app.route('/')
def index():
    if app.config.get('FIRST_RUN'):
        return render_template('setup.html')
    return render_template('index.html')

@app.route('/setup/')
def setup_resource_server():
    resource_list = RESOURCES.keys()
    oxc.register_site()
    conditions = [{"httpMethods": [method], "scopes": scopes}
                  for method, scopes in SCOPE_MAP.iteritems()]
    resources = [
        {
            "path": "/api/{0}/".format(resource_list[0]),
            "conditions": conditions
        }
    ]
    protected = oxc.uma_rs_protect(resources)
    response_dict = {
        'protected_resources': resources,
        'unprotected_resources': ["/api/{0}/".format(r) for r in resource_list[1:]]
    }
    app.config['FIRST_RUN'] = False
    return jsonify(response_dict)


@app.route('/api/<rtype>/', methods=['GET', 'POST'])
def api(rtype):
    """Function that fetches or adds a particular resource.

    :param rtype: resource type either photos or docs
    :return: json
    """
    resources = RESOURCES.keys()
    status = {'access': 'granted'}
    try:
        rpt = request.headers.get('Authorization')
        if rpt:
            rpt = rpt.split()[1]
        status = oxc.uma_rs_check_access(rpt=rpt, path=request.path,
                                         http_method=request.method)
    except:
        print request.path, " seems unprotected"

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

