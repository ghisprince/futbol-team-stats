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
db.session.remove()
db.drop_all()
db.create_all()


def get_player_by_name(name):
    return db.session.query(Player).filter_by(name=name).first()


def get_player_match_by_name(match, name):
    for i in match.player_matches:
        if i.player.name == name:
            return i


def load_match(match_data):
    match_data_date_time = datetime.datetime.strptime(match_data["date_time"],
                                                      "%Y-%m-%dT%H:%M:%S")

    if db.session.query(Match).filter_by(date_time=match_data_date_time).first():
        print("Already loaded {} vs '{}' on {}".format(match_data["team"],
                                                       match_data["opponent"],
                                                       match_data["date_time"]))
        return

    if match_data["campaign"]:
        campaign = get_or_create(db.session, Campaign, name=match_data["campaign"])
    else:
        campaign = None

    print("Load Match")
    match = Match(date_time=match_data["date_time"],
                  team=get_or_create(db.session, Team,
                                     name=match_data["team"]),
                  opponent=get_or_create(db.session, Opponent,
                                         name=match_data["opponent"]),
                  campaign=campaign)

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
                                  yellow_card=pm_data["yellow_card"],
                                  red_card=pm_data["red_card"],
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
                    x=shot_data['x'],
                    y=shot_data['y'],
                    on_goal=shot_data['on_goal'],
                    pk=shot_data['pk'],
                    scored=shot_data['scored'],
                    by_opponent=shot_data.get('by_opponent', False), )

        if shot_data['scored']:
            goal = Goal(shot_data.get('time', None))

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


def pprint():
    print("PLAYER")
    for p in db.session.query(Player).all():
        print(p)

    print("MATCH")
    for m in db.session.query(Match).all():
        print(m)

    print("PM")
    for pm in db.session.query(PlayerMatch).all():
        print(pm)



d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "data.json"), "r"))
for i in d:
    load_match(i)
print("FIN")
