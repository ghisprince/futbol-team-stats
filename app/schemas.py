from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
from marshmallow import validate, ValidationError


# for schema objects
not_blank = validate.Length(min=1, error='Field cannot be blank')

# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class TeamSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(validate=must_not_be_blank)

    class Meta:
        strict = True
        type_ = "team"
        self_view = "main.GetUpdateDeleteTeam".lower()
        self_view_kwargs = {'team_id': "<id>"}
        self_view_many = 'main.CreateListTeam'.lower()


class CampaignSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(validate=must_not_be_blank)

    class Meta:
        strict = True
        type_ = "campaign"
        self_view = "main.GetUpdateDeleteCampaign".lower()
        self_view_kwargs = {'campaign_id': "<id>"}
        self_view_many = 'main.CreateListCampaign'.lower()


class MatchSchema(Schema):
    id = fields.String(dump_only=True)
    date_time = fields.DateTime(format='iso8601', validate=must_not_be_blank)
    home_team = fields.Nested('TeamSchema', validate=must_not_be_blank)
    away_team = fields.Nested('TeamSchema', validate=must_not_be_blank)
    campaign = fields.Nested('CampaignSchema')

    class Meta:
        strict = True
        type_ = "match"
        self_view = "main.GetUpdateDeleteMatch".lower()
        self_view_kwargs = {'match_id': "<id>"}
        self_view_many = 'main.CreateListMatch'.lower()


class PlayerSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(validate=must_not_be_blank)
    number = fields.Integer()
    team = fields.Nested('TeamSchema',)

    class Meta:
        strict = True
        type_ = "player"
        self_view = "main.GetUpdateDeletePlayer".lower()
        self_view_kwargs = {'player_id': "<id>"}
        self_view_many = 'main.CreateListPlayer'.lower()


class PlayerMatchSchema(Schema):
    id = fields.String(dump_only=True)
    started = fields.Boolean()
    minutes = fields.Integer(validate=must_not_be_blank)
    subbed_due_to_injury = fields.Boolean()
    yellow_card = fields.Integer()
    red_card = fields.Integer()
    corner = fields.Integer()
    player = fields.Nested(PlayerSchema, only=('id',), validate=must_not_be_blank)
    team = fields.Nested(TeamSchema, only=('id',), validate=must_not_be_blank)
    match = fields.Nested(MatchSchema, only=('id',), validate=must_not_be_blank)

    class Meta:
        strict = True
        type_ = "playermatch"
        self_view = "main.GetUpdateDeletePlayerMatch".lower()
        self_view_kwargs = {'playermatch_id': "<id>"}
        self_view_many = 'main.CreateListPlayerMatch'.lower()
