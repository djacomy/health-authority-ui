from datetime import datetime, timedelta
from random import randint
from time import sleep
from uuid import uuid4
from flask import Blueprint, jsonify, current_app, json, make_response, session, redirect, request

import config

common_blueprint = Blueprint('common', __name__)


@common_blueprint.route('/routes')
def list_routes():
    output = []
    for rule in current_app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = "{:50s} {:20s}".format(str(rule), methods)
        output.append(line)
    return jsonify(routes=output)


@common_blueprint.after_request
def after_request(response):
    # Fake network delay.
    sleep(0.5)
    # Add CORS.
    header = response.headers
    header["Access-Control-Allow-Origin"] = config.FRONT_URL
    header["Access-Control-Allow-Credentials"] = "true"
    header["Access-Control-Allow-Headers"] = "content-type"
    return response


@common_blueprint.route("/")
def home():
    return "Hello world"


@common_blueprint.route("/user-info/")
def user_info():
    if "username" in session:
        return json.jsonify({"user": "Dr. Nemo"})
    return make_response("", 401)


@common_blueprint.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = "Dr. Nemo"
        return redirect(config.FRONT_URL)
    return """
        <form method="post">
            <input type="submit" value="login">
        </form>
    """


@common_blueprint.route("/logout/")
def logout():
    session.pop("username", None)
    return redirect(config.FRONT_URL)


@common_blueprint.route("/create-code/", methods=["POST"])
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
