from marshmallow import fields
from flask_marshmallow.sqla import ModelSchema
from app.shared import ma
from app.shared import api
from app.models import *


class TeamSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteTeam'.lower(), team_id="<id>"),
         'collection': ma.URLFor('CreateListTeam'.lower(),),
         #'matches': ma.URLFor('AddRemoveListTeamMatch'.lower(), team_id="<id>"),
         #'players': ma.URLFor('AddRemoveListTeamPlayer'.lower(), team_id="<id>"),
         })

    class Meta:
        strict = True
        model = Team
        sqla_session = db.session


class TeamSchemaEx(TeamSchema):
    matches = fields.Nested('MatchSchema', many=True, dump_only=True)
    players = fields.Nested('PlayerSchema', many=True, dump_only=True)


class PlayerSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeletePlayer'.lower(), player_id="<id>"),
         'collection': ma.URLFor('CreateListPlayer'.lower()),
        })

    class Meta:
        strict = True
        model = Player
        sqla_session = db.session


class PlayerSchemaEx(PlayerSchema):
    player_matches = fields.Nested('PlayerMatchSchemaEx', many=True,
                                   dump_only=True)

    team = fields.Nested('TeamSchema', dump_only=True,
                         exclude=("matches", "players"))


class CompetitionSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteCompetition'.lower(),
                           competition_id="<id>"),
         'collection': ma.URLFor('CreateListCompetition'.lower())
        })

    num_match_won = fields.String(dump_only=True)
    num_match_tied = fields.String(dump_only=True)
    num_match_lost = fields.String(dump_only=True)
    match_results = fields.String(dump_only=True)

    class Meta:
        strict = True
        model = Competition
        sqla_session = db.session


class CompetitionSchemaEx(CompetitionSchema):

    matches = fields.Nested('MatchSchemaEx', many=True, dump_only=True,
                            exclude=("player_matches",))


class OpponentSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteOpponent'.lower(), opponent_id="<id>"),
         'collection': ma.URLFor('CreateListOpponent'.lower())
        })

    num_match_won = fields.String(dump_only=True)
    num_match_tied = fields.String(dump_only=True)
    num_match_lost = fields.String(dump_only=True)
    match_results = fields.String(dump_only=True)

    class Meta:
        strict = True
        model = Opponent
        sqla_session = db.session


#
class OpponentSchemaEx(OpponentSchema):
    matches = fields.Nested('MatchSchemaEx', many=True, dump_only=True,
                            exclude=("player_matches", "opponent", "team"))


class ShotSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteShot'.lower(), shot_id="<id>"),
         'collection': ma.URLFor('CreateListShot'.lower())
        })

    class Meta:
        strict = True
        model = Shot
        sqla_session = db.session

#
class ShotSchemaEx(ShotSchema):
    goal = fields.Nested('GoalSchema', dump_only=True)
    player_match = fields.Nested('PlayerMatchSchema', dump_only=True)


class AssistSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteAssist'.lower(), assist_id="<id>"),
         'collection': ma.URLFor('CreateListAssist'.lower())
        })

    class Meta:
        strict = True
        model = Assist
        sqla_session = db.session


#
class AssistSchemaEx(AssistSchema):
    player_match = fields.Nested('PlayerMatchSchema', dump_only=True)


class GoalSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteGoal'.lower(), goal_id="<id>"),
         'collection': ma.URLFor('CreateListGoal'.lower())
        })

    class Meta:
        strict = True
        model = Goal
        sqla_session = db.session

#
class GoalSchemaEx(GoalSchema):
    assist = fields.Nested('AssistSchema', dump_only=True)

    shot = fields.Nested('ShotSchema', dump_only=True)

    player_match = fields.Nested('PlayerMatchSchemaEx', dump_only=True, )



class PlayerMatchSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeletePlayerMatch'.lower(),
                           playermatch_id="<id>"),
         'collection': ma.URLFor('CreateListPlayerMatch'.lower()),
         })

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

#
class PlayerMatchSchemaEx(PlayerMatchSchema):
    player = fields.Nested(PlayerSchemaEx, dump_only=True,
                           exclude=("player_matches",))
    match = fields.Nested('MatchSchemaEx', dump_only=True,
                          exclude=("player_matches",))
    shots = fields.Nested(ShotSchema, dump_only=True, many=True)
    assists = fields.Nested(AssistSchema, dump_only=True, many=True)
    goals = fields.Nested(GoalSchema, dump_only=True, many=True)


class MatchSchema(ModelSchema):
    _links = ma.Hyperlinks(
        {'self': ma.URLFor('GetUpdateDeleteMatch'.lower(), match_id="<id>"),
         'collection': ma.URLFor('CreateListMatch'.lower()),
         })

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

#
class MatchSchemaEx(MatchSchema):
    competition = fields.Nested(CompetitionSchema, dump_only=True, exclude=("matches",))
    opponent = fields.Nested(OpponentSchema, dump_only=True, exclude=("matches",))
    team = fields.Nested(TeamSchema, dump_only=True, exclude=("players", "matches"))
    player_matches = fields.Nested(PlayerMatchSchemaEx, dump_only=True, many=True,
                                   exclude=("match", ))