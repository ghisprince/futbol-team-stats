from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from app.extensions import cache
from app.forms import LoginForm
from app.models import *
from app.views import *  # should use ..
from flask_restful import Api

main = Blueprint('main', __name__)
api = Api(main)

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


api.add_resource(CreateListTeam, '/api/v1/teams/')
api.add_resource(GetUpdateDeleteTeam, '/api/v1/teams/<int:team_id>')

api.add_resource(CreateListPlayer, '/api/v1/players/')
api.add_resource(GetUpdateDeletePlayer, '/api/v1/players/<int:player_id>')

api.add_resource(CreateListMatch, '/api/v1/matches/')
api.add_resource(GetUpdateDeleteMatch, '/api/v1/matches/<int:match_id>')

#api.add_resource(CreateListTeamMatch, '/api/v1/teams/<int:team_id>/matches/')
#api.add_resource(GetUpdateDeleteTeamMatch, '/api/v1/teams/<int:team_id>/matches/<int:match_id>')

api.add_resource(CreateListCampaign, '/api/v1/campaigns/')
api.add_resource(GetUpdateDeleteCampaign, '/api/v1/campaigns/<int:campaign_id>')

api.add_resource(CreateListPlayerMatch, '/api/v1/playermatches/')
api.add_resource(GetUpdateDeletePlayerMatch, '/api/v1/playermatches/<int:playermatch_id>')
