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


class CompetitionSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteCompetition'.lower(), competition_id="<id>"),
         'collection': ma.URLFor('CreateListCompetition'.lower())
        })

    matches = fields.Nested('MatchSchema',
                            many=True,
                            dump_only=True,
                            only=("_links", "id", "date_time", "team",
                                  "at_home", "result", "result_long"))

    match_results = fields.String()

    class Meta:
        strict = True
        model = Competition
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
                            only=("_links", "id", "date_time", "team_id",
                                  "opponent_id", "result"))

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

    player_match = fields.Nested('PlayerMatchSchema', dump_only=True,
                                 only=("_links", "id"))

    class Meta:
        strict = True
        model = Shot
        sqla_session = db.session


class AssistSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteAssist'.lower(), assist_id="<id>"),
         'collection': ma.URLFor('CreateListAssist'.lower())
        })

    player_match = fields.Nested('PlayerMatchSchema', dump_only=True,
                                 only=("_links", "id"))

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

    shot = fields.Nested('ShotSchema',
                            dump_only=True,
                            only=("_links", "id", ))

    player_match = fields.Nested('PlayerMatchSchema', dump_only=True,
                                 only=("_links", "id"))

    class Meta:
        strict = True
        model = Goal
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

    # hybrid properties on model
    num_shots = fields.Integer(dump_only=True)
    num_shots_against = fields.Integer(dump_only=True)
    num_goals = fields.Integer(dump_only=True)
    num_goals_against = fields.Integer(dump_only=True)
    num_assists = fields.Integer(dump_only=True)
    num_saves = fields.Integer(dump_only=True)

    class Meta:
        strict = True
        model = PlayerMatch
        sqla_session = db.session


class MatchSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteMatch'.lower(), match_id="<id>"),
         'collection': ma.URLFor('CreateListMatch'.lower()),
         })

    competition = fields.Nested(CompetitionSchema,
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
                                         "player", "minutes", "starter",
                                         "subbed_due_to_injury",
                                         "yellow_card", "red_card",
                                         "num_shots", "num_goals",
                                         "num_assists",
                                         "num_shots_against",
                                         "num_goals_against",
                                         )
                                   )

    # add hybrid properties on model
    result = fields.String(dump_only=True)
    result_long = fields.String(dump_only=True)
    num_shots = fields.Integer(dump_only=True)
    num_shots_against = fields.Integer(dump_only=True)
    num_goals = fields.Integer(dump_only=True)
    num_goals_against = fields.Integer(dump_only=True)

    class Meta:
        strict = True
        model = Match
        sqla_session = db.session