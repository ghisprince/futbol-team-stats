from flask import Blueprint, render_template, flash, redirect, url_for, send_file, session, request, jsonify
from flask_login import login_user, logout_user, login_required

#from .. extensions import cache
from .. forms import LoginForm
from .. models import *
from .. api import *

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    return render_template('index.html')


@main.route("/api/v1/login", methods=["POST"])
def login():
    data = json.loads(request.data)
    username = data["username"]
    password = data["password"]

    try:
        user = User.query.filter_by(username=username).one()
        if user.check_password(password):
            login_user(user, remember=True)
        else:
            raise Exception
    except:
        import time;time.sleep(1)
        resp = jsonify({"error": "Login failed"})
        resp.status_code = 401
        return resp





@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".login"))


@main.route("/stats")
@login_required
def stats():
    return render_template('stats.html')


@main.route("/restricted")
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200


api_v1_html = """
<p>
rest api version 1.0
    <ul>
    <li><a href="/api/v1/teams/">/api/v1/teams/</a></li>
    <li><a href="/api/v1/players/">/api/v1/players/</a></li>
    <li><a href="/api/v1/competitions/">/api/v1/competitions/</a></li>
    <li><a href="/api/v1/matches/">/api/v1/matches/</a></li>
    <li><a href="/api/v1/playermatches/">/api/v1/playermatches/</a></li>
    </ul>
</p>

"""


@main.route("/api/v1")
@login_required
def api_v1():
    return api_v1_html
