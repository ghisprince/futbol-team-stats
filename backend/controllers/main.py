from flask import Blueprint, render_template, flash, redirect, url_for, send_file, session, request, jsonify
from flask_login import login_user, logout_user

#from .. extensions import cache
from .. models import *
from .. api import *

main = Blueprint('main', __name__)

"""
@main.route("/api/v1/login", methods=["POST"])
def login():
    data = json.loads(request.data)
    username = data["username"]
    password = data["password"]

    try:
        user = User.query.filter_by(username=username).one()
        if user.check_password(password):
            login_user(user, remember=True)
            token = user.generate_auth_token()
            return jsonify({ 'token': token.decode('ascii') })
        else:
            raise Exception
    except:
        import time;time.sleep(0.1)
        resp = jsonify({"error": "Login failed"})
        resp.status_code = 401
        return resp
"""