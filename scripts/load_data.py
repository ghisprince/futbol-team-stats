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
        print("Already loaded {} vs '{}' on {}".format(match_data["home_team"],
                                                       match_data["away_team"],
                                                       match_data["date_time"]))
        return

    if match_data["campaign"]:
        campaign = get_or_create(db.session, Campaign, name=match_data["campaign"])
    else:
        campaign = None

    print("Load Match")
    match = Match(date_time=match_data["date_time"],
                  home_team=get_or_create(db.session, Team, name=match_data["home_team"]),
                  away_team=get_or_create(db.session, Team, name=match_data["away_team"]),
                  campaign=campaign)

    db.session.add(match)

    print("Load PlayerMatch")
    for pm_data in match_data["player_match"]:
        print(" - player match : {}".format(pm_data["name"]))
        team = get_or_create(db.session, Team, name=pm_data["team"])
        playerMatch = PlayerMatch(player=get_or_create(db.session, Player, name=pm_data["name"], team=team),
                                  match=match,
                                  team=team,
                                  started=pm_data["started"],
                                  minutes=pm_data["minutes"],
                                  subbed_due_to_injury=pm_data["subbed_due_to_injury"],
                                  yellow_card=pm_data["yellow_card"],
                                  red_card=pm_data["red_card"],
                                  corner=pm_data["corner"],
                                  )

        db.session.add(playerMatch)
    #db.session.commit()

    print("Load Shots")
    for shot_data in match_data.get("shot", []):
        playerMatch = get_player_match_by_name(match, shot_data['player'])
        shot = Shot(playerMatch,
                    x=shot_data['x'], y=shot_data['y'],
                    on_goal=shot_data['on_goal'], pk=shot_data['pk'])

        #shot.player_match = playerMatch
        if shot_data['goal']:
            goal = Goal(playerMatch, shot_data.get('time', None))

            goal.player_match = playerMatch
            goal.shot = shot
            if shot_data['assist']:
                assistPlayerMatch = get_player_match_by_name(match, shot_data['assist'])
                assist = Assist(assistPlayerMatch, goal)
                db.session.add(assist)
            db.session.add(goal)
        db.session.add(shot)

    for shot_ag_data in match_data.get("shot_against", []):
        shotAgainst = ShotAgainst(x=shot_ag_data["x"], y=shot_ag_data["y"],
                                  on_goal=shot_ag_data["on_goal"],
                                  saved=shot_ag_data["saved"],
                                  pk=shot_ag_data["pk"],
                                  )
        keeper = get_player_match_by_name(match, shot_ag_data['keeper'])
        shotAgainst.player_match = keeper
        db.session.add(shotAgainst)

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


#validate_player_match(milan_2017_04_22_match)




d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "data.json"), "r"))
for i in d:
    load_match(i)
print("FIN")
