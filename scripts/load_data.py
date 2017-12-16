"""
Load tests\data.json (toy data) into database for dev work.
"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

from app import create_app
from app.models import *

app = create_app('app.settings.DevConfig')
db.app = app
#db.session.remove()
#db.drop_all()
db.create_all()


def get_player_by_name(name):
    return db.session.query(Player).filter_by(name=name).first()


def get_player_match_by_name(match, name):
    for i in match.player_matches:
        if i.player.name == name:
            return i

def load_users(team):
    # create some roles
    admin_role = get_or_create(db.session, Role, name='admin')
    edit_role = get_or_create(db.session, Role, name='editor')

    # create some users
    parent = db.session.query(User).filter_by(username="gp")
    if not parent.first():
        parent = User("gp", "gp")
        parent.teams.append(team)
        parent.roles.append(edit_role)
        parent.roles.append(admin_role)
        db.session.add(parent)

    historian = db.session.query(User).filter_by(username="historian")
    if not historian.first():
        historian = User("historian", "historian")
        historian.teams.append(team)
        historian.roles.append(edit_role)
        db.session.add(historian)

    stranger = db.session.query(User).filter_by(username="stranger")
    if not stranger.first():
        stranger = User("stranger", "stranger")
        db.session.add(stranger)

    db.session.commit()


def load_match(match_data):
    match_data_date_time = datetime.datetime.strptime(match_data["date_time"],
                                                      "%Y-%m-%dT%H:%M:%S")

    team = get_or_create(db.session, Team, name=match_data['team'])

    load_users(team)
    if db.session.query(Match).filter_by(date_time=match_data_date_time).first():
        print("Already loaded {} vs '{}' on {}".format(match_data["team"],
                                                       match_data["opponent"],
                                                       match_data["date_time"]))
        return

    if match_data["competition"]:
        competition = get_or_create(db.session, Competition,
                                    name=match_data["competition"],
                                    team=team)
    else:
        competition = None

    print("Load Match ({} on {})".format(match_data["opponent"],
                                         match_data["date_time"]))

    if "duration" not in match_data:
        match_data["duration"] = 70

    match = Match(date_time=match_data["date_time"],
                  duration=match_data["duration"],
                  team=get_or_create(db.session, Team, name=match_data["team"]),
                  opponent=get_or_create(db.session, Opponent,
                                         name=match_data["opponent"],
                                         team=team),
                  competition=competition)

    if "match_stats" in match_data:
        print("Load Additional Stats")
        add_stats_data = match_data["match_stats"]
        add_stats_data['match'] = match
        add_stats = MatchStats(**add_stats_data)
        db.session.add(add_stats)


    db.session.add(match)


    # collect all playermatch shot data into a list and defer until all
    #  playermatch have been created to deal with assist (between 2 playermatch)
    pm_shot_data = []

    print("Load PlayerMatch")
    for pm_data in match_data["player_match"]:
        print(" - player match : {}".format(pm_data["name"]))
        team = get_or_create(db.session, Team, name=match_data["team"])
        playerMatch = PlayerMatch(player=get_or_create(db.session, Player,
                                                       name=pm_data["name"],
                                                       team=team),
                                  match=match,
                                  starter=pm_data["starter"],
                                  minutes=pm_data["minutes"],
                                  subbed_due_to_injury=pm_data["subbed_due_to_injury"],
                                  yellow_cards=pm_data["yellow_cards"],
                                  red_cards=pm_data["red_cards"],
                                  corners=pm_data["corners"],
                                  )
        for shot in pm_data['shots']:
            shot['player'] = pm_data["name"]
            pm_shot_data.append(shot)

        db.session.add(playerMatch)

    print("Load Shots")
    for shot_data in pm_shot_data:
        playerMatch = get_player_match_by_name(match, shot_data['player'])
        shot = Shot(playerMatch,
                    x=shot_data.get('x', None),
                    y=shot_data.get('y', None),
                    on_target=shot_data.get('on_target', False),
                    pk=shot_data.get('pk', False),
                    by_opponent=shot_data.get('by_opponent', False), )

        if shot_data.get('scored', False):
            goal = Goal(shot, shot_data.get('time', None))

            goal.player_match = playerMatch
            goal.shot = shot
            if shot_data.get('assist', None):
                assistPlayerMatch = get_player_match_by_name(match,
                                                             shot_data['assist'])
                assist = Assist(assistPlayerMatch, goal)
                db.session.add(assist)
            db.session.add(goal)
        db.session.add(shot)

    db.session.commit()


f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
d = json.load(open(f, "r"))
for i in d:
    load_match(i)

print("FIN")
