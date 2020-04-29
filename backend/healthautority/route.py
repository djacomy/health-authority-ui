import os
from datetime import datetime, timedelta
from random import randint
from uuid import uuid4
from flask import (Blueprint, jsonify, render_template, current_app,
                   json, make_response, session, redirect, request)

from healthautority.auth import AuthMachineClient
import config

blueprint = Blueprint('auth', __name__,
                      template_folder='templates',
                      root_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@blueprint.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = config.FRONT_URL
    header["Access-Control-Allow-Credentials"] = "true"
    header["Access-Control-Allow-Headers"] = "content-type"
    return response


@blueprint.route('/routes')
def list_routes():
    output = []
    for rule in current_app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = "{:50s} {:20s}".format(str(rule), methods)
        output.append(line)
    return jsonify(routes=output)


@blueprint.route("/")
def index():
    return render_template('index.jinja', user_info=session.get('user_info'))


@blueprint.route("/user-info/")
def user_info():
    if "user_info" in session:
        return json.jsonify(session['user_info'])
    return make_response("", 401)


@blueprint.route("/login/", methods=["GET", "POST"])
def login():
    client = AuthMachineClient()
    return redirect(client.get_authorization_url())


@blueprint.route('/oidc-callback')
def auth_callback():
    client = AuthMachineClient()
    aresp = client.get_authorization_response()
    session['user_info'] = client.get_userinfo(aresp)
    return redirect(config.FRONT_URL)


@blueprint.route("/logout/")
def logout():
    if 'user_info' in session:
        del session['user_info']
    return redirect(config.FRONT_URL)


@blueprint.route("/create-code/", methods=["POST"])
def create_code():
    code_type = request.json["type"]
    now = datetime.now()
    code = ""
    ttl = 0

    if code_type == "pincode":
        # A random number of 9 digits.
        code = str(randint(0, 999999999)).rjust(9, "0")
        ttl = 120
    else:
        code = str(uuid4())
        ttl = 3600

    delta = timedelta(seconds=ttl)
    expireAt = (now + delta).isoformat()
    return json.jsonify(
        {"type": "qrcode", "code": code, "expireAt": expireAt, "ttl": ttl,}
    )
