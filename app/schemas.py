from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema
from marshmallow import validate, ValidationError


# for schema objects
not_blank = validate.Length(min=1, error='Field cannot be blank')

# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class TeamSchema(Schema):
    id = fields.Integer() #dump_only=True
    name = fields.String(validate=must_not_be_blank)

    """
    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/teams/"
        else:
            self_link = "/teams/{}".format(data['id'])
        return {'self': self_link}
    """
    class Meta:
        strict = True
        type_ = "team"
        self_view = "main.GetUpdateDeleteTeam".lower()
        self_view_kwargs = {'team_id': "<id>"}
        self_view_many = 'main.CreateListTeam'.lower()


class CampaignSchema(Schema):
    id = fields.Integer() #dump_only=True
    name = fields.String(validate=must_not_be_blank)

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/campaigns/"
        else:
            self_link = "/campaigns/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        strict = True
        type_ = "campaign"
        self_view = "main.GetUpdateDeleteCampaign".lower()
        self_view_kwargs = {'campaign_id': "<id>"}
        self_view_many = 'main.CreateListCampaign'.lower()


class MatchSchema(Schema):
    id = fields.Integer() #dump_only=True
    '''
    date_time = fields.DateTime(format='iso8601')
    home_team = fields.Nested('TeamSchema')
    away_team = fields.Nested('TeamSchema')
    campaign = fields.Nested('CampaignSchema')
    '''
    date_time = fields.DateTime(format='iso8601', validate=must_not_be_blank)
    home_team = fields.Nested('TeamSchema', validate=must_not_be_blank)
    away_team = fields.Nested('TeamSchema', validate=must_not_be_blank)
    campaign = fields.Nested('CampaignSchema')

    #player_matches = fields.Nested('PlayerMatchSchema', many=True, exclude=('match',))
    #home_team = fields.Relationship(related_url='/api/v1/teams/{home_team_id}',
    #                                related_url_kwargs={'home_team_id': '<home_team.id>','_external': True},
    #                                include_data=True, type_='team')


    #away_team = fields.Relationship(related_url='/api/v1/teams/{away_team_id}',
    #                                related_url_kwargs={'away_team_id': '<away_team.id>'})

    #campaign = fields.Relationship(related_url='/api/v1/campaigns/{campaign_id}',
    #                                related_url_kwargs={'campaign_id': '<campaign.id>'})

    #player_matches = fields.Relationship(related_url='/api/v1/playermatches/{playermatch_id}',
    #                                related_url_kwargs={'playermatch_id': '<player_matches.id>'})


    '''
    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/matches/"
        else:
            self_link = "/matches/{}".format(data['match_id'])
        return {'self': self_link}
    '''
    class Meta:
        strict = True
        type_ = "match"
        self_view = "main.GetUpdateDeleteMatch".lower()
        self_view_kwargs = {'match_id': "<id>"}
        self_view_many = 'main.CreateListMatch'.lower()


class PlayerSchema(Schema):
    id = fields.Integer() #dump_only=True
    name = fields.String(validate=must_not_be_blank)
    number = fields.Integer()
    #player_matches = fields.Nested('PlayerMatchSchema', many=True, only=('id',))
    #player_matches = fields.Relationship(related_url='/api/v1/playermatches/{playermatches_id}',
    #                                     related_url_kwargs={'playermatches_id': '<id>'},
    #                                     many=True, include_resource_linkage=True,
    #                                     type_="playermatches")

    '''
    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/players/"
        else:
            self_link = "/players/{}".format(data['id'])
        return {'self': self_link}
    '''
    class Meta:
        strict = True
        type_ = "player"
        self_view = "main.GetUpdateDeletePlayer".lower()
        self_view_kwargs = {'player_id': "<id>"}
        self_view_many = 'main.CreateListPlayer'.lower()


class PlayerMatchSchema(Schema):
    id = fields.Integer() #dump_only=True
    started = fields.Boolean()
    minutes = fields.Integer(validate=must_not_be_blank)
    subbed_due_to_injury = fields.Boolean()
    yellow_card = fields.Integer()
    red_card = fields.Integer()
    corner = fields.Integer()
    player = fields.Nested(PlayerSchema, only=('id',), validate=must_not_be_blank)
    team = fields.Nested(TeamSchema, only=('id',), validate=must_not_be_blank)
    match = fields.Nested(MatchSchema, only=('id',), validate=must_not_be_blank)

    '''
    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/playermatches/"
        else:
            self_link = "/playermatches/{}".format(data['id'])
        return {'self': self_link}
    '''
    class Meta:
        strict = True
        type_ = "playermatch"
        self_view = "main.GetUpdateDeletePlayerMatch".lower()
        self_view_kwargs = {'playermatch_id': "<id>"}
        self_view_many = 'main.CreateListPlayerMatch'.lower()
