from marshmallow import fields
from flask_marshmallow.sqla import ModelSchema
from .shared import ma
from .shared import api
from .models import *


class UserSchema(ModelSchema):
    is_editor = fields.Boolean(dump_only=True)

    class Meta:
        strict = True
        model = User
        fields = ('username', 'is_editor', 'teams')  # token here?
        sqla_session = db.session


class TeamSchema(ModelSchema):
    class Meta:
        strict = True
        model = Team
        sqla_session = db.session


class TeamSchemaEx(TeamSchema):
    matches = fields.Nested('MatchSchema', many=True, dump_only=True)
    players = fields.Nested('PlayerSchema', many=True, dump_only=True)


class PlayerSchema(ModelSchema):
    label = fields.String(dump_only=True)
    num_apps =  fields.Integer(dump_only=True)

    class Meta:
        strict = True
        model = Player
        sqla_session = db.session
        exclude = ["player_matches",]


class PlayerSchemaEx(PlayerSchema):
    player_matches = fields.Nested('PlayerMatchSchemaEx',
                                   many=True,
                                   dump_only=True)

    team = fields.Nested('TeamSchema', dump_only=True,
                         exclude=("matches", "players"))


class CompetitionSchema(ModelSchema):

    start_date = fields.String(dump_only=True)
    num_match_won = fields.Integer(dump_only=True)
    num_match_tied = fields.Integer(dump_only=True)
    num_match_lost = fields.Integer(dump_only=True)
    num_match = fields.Integer(dump_only=True)
    match_results = fields.String(dump_only=True)
    goal_differential = fields.Integer(dump_only=True)
    clean_sheets = fields.Integer(dump_only=True)

    class Meta:
        strict = True
        model = Competition
        sqla_session = db.session
        exclude = ["matches",]


class CompetitionSchemaEx(CompetitionSchema):
    matches = fields.Nested('MatchSchemaEx', many=True,
                            dump_only=True,
                            exclude=("player_matches",))


class OpponentSchema(ModelSchema):

    num_match_won = fields.Integer(dump_only=True)
    num_match_tied = fields.Integer(dump_only=True)
    num_match_lost = fields.Integer(dump_only=True)
    num_match = fields.Integer(dump_only=True)
    match_results = fields.String(dump_only=True)
    goal_differential = fields.Integer(dump_only=True)

    class Meta:
        strict = True
        model = Opponent
        sqla_session = db.session
        exclude = ["matches",]


class OpponentSchemaEx(OpponentSchema):
    matches = fields.Nested('MatchSchemaEx', many=True,
                            dump_only=True,
                            exclude=("player_matches",
                                     "opponent",
                                     "team"))


class ShotSchema(ModelSchema):

    scored = fields.Boolean(dump_only=True)
    player_number = fields.Integer(dump_only=True)

    # hybrid properties on model
    player_label = fields.String(dump_only=True)

    goal = fields.Nested('GoalSchemaEx', dump_only=True,
                         exclude=["shot", "player_match"])

    #player_match = fields.Nested('PlayerMatchSchemaEx',
    #                             dump_only=True,
    #                             exclude=["shots"])

    class Meta:
        strict = True
        model = Shot
        sqla_session = db.session


class ShotSchemaEx(ShotSchema):
    # todo: if don't do "all player shots, then no need for this for graphing"
    pass

class AssistSchema(ModelSchema):
    class Meta:
        strict = True
        model = Assist
        sqla_session = db.session


class AssistSchemaEx(AssistSchema):
    player_label = fields.String(dump_only=True)
    goal = fields.Nested('GoalSchemaEx', dump_only=True,
                         exclude=["assist", "player_match"])


class GoalSchema(ModelSchema):
    assisted = fields.Boolean(dump_only=True)
    assist = fields.Nested('AssistSchemaEx', dump_only=True, exclude=["goal", ])

    class Meta:
        strict = True
        model = Goal
        sqla_session = db.session


class GoalSchemaEx(GoalSchema):
    assist = fields.Nested('AssistSchemaEx', dump_only=True, exclude=["goal", ])
    shot = fields.Nested('ShotSchemaEx', dump_only=True, exclude=["goal", ])


class PlayerMatchSchema(ModelSchema):
    # hybrid properties on model
    player_label = fields.String(dump_only=True)
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
        exclude = ("assists", "shots")


class PlayerMatchSchemaEx(PlayerMatchSchema):
    match = fields.Nested('MatchSchemaEx', dump_only=True,
                          only=("id",
                                "date_time",
                                "competition_name",
                                "competition_id",
                                "opponent_name",
                                "opponent_id",
                                "result",
                                "score"))


class MatchStatsSchema(ModelSchema):

    class Meta:
        strict = True
        model = MatchStats
        sqla_session = db.session


class MatchSchema(ModelSchema):

    # add hybrid properties on model
    result = fields.String(dump_only=True)
    score = fields.String(dump_only=True)
    result_long = fields.String(dump_only=True)
    num_goals = fields.Integer(dump_only=True)
    num_goals_against = fields.Integer(dump_only=True)
    goal_differential = fields.Integer(dump_only=True)

    # add hybrid properties from MatchStats for convenient access
    opponent_name = fields.String(dump_only=True)
    competition_name = fields.String(dump_only=True)
    goals_timeline = fields.List(fields.String, dump_only=True, )
    goals_against_timeline = fields.List(fields.String, dump_only=True, )
    num_shots = fields.Integer(dump_only=True)
    num_shots_against = fields.Integer(dump_only=True)
    shot_on_target_pct = fields.String(dump_only=True)
    opponent_shot_on_target_pct = fields.String(dump_only=True)
    num_corners = fields.Integer(dump_only=True)
    num_opponent_corners = fields.Integer(dump_only=True)
    num_yellow_cards = fields.Integer(dump_only=True)
    num_opponent_yellow_cards = fields.Integer(dump_only=True)
    num_red_cards = fields.Integer(dump_only=True)
    num_opponent_red_cards = fields.Integer(dump_only=True)
    num_passes = fields.Integer(dump_only=True)
    num_opponent_passes = fields.Integer(dump_only=True)
    num_pass_strings = fields.Integer(dump_only=True)
    num_opponent_pass_strings = fields.Integer(dump_only=True)
    pass_pct = fields.Integer(dump_only=True)
    opponent_pass_pct = fields.Integer(dump_only=True)

    class Meta:
        strict = True
        model = Match
        sqla_session = db.session


class MatchSchemaEx(MatchSchema):
    competition = fields.Nested(CompetitionSchema,
                                dump_only=True,
                                exclude=("matches",))

    opponent = fields.Nested(OpponentSchema, dump_only=True,
                             exclude=("matches",))

    team = fields.Nested(TeamSchema, dump_only=True,
                         exclude=("players",
                                  "matches",
                                  "opponents",
                                  "competitions",
                                  "teams"))

    match_stats = fields.Nested(MatchStatsSchema,
                                dump_only=True)

    player_matches = fields.Nested(PlayerMatchSchemaEx,
                                   dump_only=True,
                                   many=True,
                                   exclude=("match",))
