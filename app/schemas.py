from marshmallow import fields
from flask_marshmallow.sqla import ModelSchema
from app.shared import ma
from app.shared import api
from app.models import *


class TeamSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteTeam'.lower(), team_id="<id>"),
         'collection': ma.URLFor('CreateListTeam'.lower(),),
         'matches': ma.URLFor('AddRemoveListTeamMatch'.lower(), team_id="<id>"),
         'players': ma.URLFor('AddRemoveListTeamPlayer'.lower(), team_id="<id>"),
         })

    class Meta:
        strict = True
        model = Team
        sqla_session = db.session


class PlayerSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeletePlayer'.lower(), player_id="<id>"),
         'collection': ma.URLFor('CreateListPlayer'.lower()),
         'playermatches': ma.URLFor('AddRemoveListPlayerPlayerMatch'.lower(),
                                player_id="<id>")
        })

    player_matches = fields.Nested('PlayerMatchSchema',
                                   many=True,
                                   dump_only=True,
                                   only=("_links", "id",))

    team = fields.Nested('TeamSchema',
                         dump_only=True,
                         only=("_links", "id", "name"))

    class Meta:
        strict = True
        model = Player
        sqla_session = db.session


class CampaignSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteCampaign'.lower(), campaign_id="<id>"),
         'collection': ma.URLFor('CreateListCampaign'.lower())
        })

    matches = fields.Nested('MatchSchema',
                            many=True,
                            dump_only=True,
                            only=("_links", "id", "date_time", "away_team",
                                  "home_team"))

    class Meta:
        strict = True
        model = Campaign
        sqla_session = db.session


#
class OpponentSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteOpponent'.lower(), opponent_id="<id>"),
         'collection': ma.URLFor('CreateListOpponent'.lower())
        })

    matches = fields.Nested('MatchSchema',
                            many=True,
                            dump_only=True,
                            only=("_links", "id", "date_time", "away_team",
                                  "home_team"))

    class Meta:
        strict = True
        model = Opponent
        sqla_session = db.session


class ShotSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteShot'.lower(), shot_id="<id>"),
         'collection': ma.URLFor('CreateListShot'.lower())
        })
    goal = fields.Nested('GoalSchema',
                          dump_only=True,
                          only=("_links", "id", "time", ))

    class Meta:
        strict = True
        model = Shot
        sqla_session = db.session


class AssistSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteAssist'.lower(), assist_id="<id>"),
         'collection': ma.URLFor('CreateListAssist'.lower())
        })

    class Meta:
        strict = True
        model = Assist
        sqla_session = db.session


class GoalSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteGoal'.lower(), goal_id="<id>"),
         'collection': ma.URLFor('CreateListGoal'.lower())
        })

    assist = fields.Nested('AssistSchema',
                            dump_only=True,
                            only=("_links", "id"))
    class Meta:
        strict = True
        model = Goal
        sqla_session = db.session


class ShotAgainstSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteShotAgainst'.lower(),
                           shotagainst_id="<id>"),
         'collection': ma.URLFor('CreateListShotAgainst'.lower())
        })

    class Meta:
        strict = True
        model = ShotAgainst
        sqla_session = db.session


class PlayerMatchSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeletePlayerMatch'.lower(),
                           playermatch_id="<id>"),
         'collection': ma.URLFor('CreateListPlayerMatch'.lower()),
         })


    player = fields.Nested(PlayerSchema,
                             dump_only=True,
                             only=("_links", "id", "name", "number"))

    match = fields.Nested('MatchSchema', dump_only=True,
                          only=("_links", "id", ))

    shots = fields.Nested(ShotSchema, dump_only=True, many=True)
    assists = fields.Nested(AssistSchema, dump_only=True, many=True)
    goals = fields.Nested(GoalSchema, dump_only=True, many=True)
    shots_against = fields.Nested(ShotAgainstSchema, dump_only=True, many=True)

    class Meta:
        strict = True
        model = PlayerMatch
        sqla_session = db.session


class MatchSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteMatch'.lower(), match_id="<id>"),
         'collection': ma.URLFor('CreateListMatch'.lower()),
         'playermatches': ma.URLFor('AddRemoveListMatchPlayerMatch'.lower(),
                                    match_id="<id>"),
         })

    campaign = fields.Nested(CampaignSchema,
                             dump_only=True,
                             only=("_links", "id", "name"))

    opponent = fields.Nested(OpponentSchema, dump_only=True,
                             only=("_links", "id", "name"))

    team = fields.Nested(TeamSchema, dump_only=True,
                         only=("_links", "id", "name"))


    player_matches = fields.Nested(PlayerMatchSchema,
                                   dump_only=True,
                                   many=True,
                                   only=("_links", "id",
                                         "player", "minutes", "started",)
                                         #"subbed_due_to_injury",
                                         #"goals", "assists", "shots", "corner",
                                         #"shots_against",
                                         #"yellow_card", "red_card"
                                         #)
                                   )
    class Meta:
        strict = True
        model = Match
        sqla_session = db.session