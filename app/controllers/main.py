from flask import Blueprint, render_template, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required


from app.extensions import cache
from app.forms import LoginForm
from app.models import *



main = Blueprint('main', __name__)

@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for(".home"))

    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".home"))


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
    <li><a href="/api/v1/campaigns/">/api/v1/campaigns/</a></li>
    <li><a href="/api/v1/matches/">/api/v1/matches/</a></li>
    <li><a href="/api/v1/playermatches/">/api/v1/playermatches/</a></li>    
    </ul>
</p>

"""

@main.route("/api/v1")
def api_v1():
    return api_v1_html


from app.api import *