from flask_restful import Resource

from flask import jsonify, make_response, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from webargs.flaskparser import use_kwargs

from app.models import *
from app.schemas import *
from marshmallow import ValidationError
import webargs

team_schema = TeamSchema(only=("_links", "id", "name"))
player_schema = PlayerSchema(only=("_links", "id", "name", "number", "team"))
match_schema = MatchSchema()
campaign_schema = CampaignSchema()
opponent_schema = OpponentSchema()
playermatch_schema = PlayerMatchSchema()
shot_schema = ShotSchema()
goal_schema = GoalSchema()
assist_schema = AssistSchema()
shotagainst_schema = ShotAgainstSchema()

"""http://jsonapi.org/format/#fetching
A server MUST respond to a successful request to fetch an individual 
resource or resource collection with a 200 OK response.
A server MUST respond with 404 Not Found when processing a request to 
fetch a single resource that does not exist, except when the request 
warrants a 200 OK response with null as the primary data 
(as described above) a self link as part of the top-level links object
"""

"""http://jsonapi.org/format/#crud
A resource can be created by sending a POST request to a URL that 
represents a collection of roles. The request MUST include a 
single resource object as primary data. The resource object 
MUST contain at least a type member.
If a POST request did not include a Client-Generated ID and the 
requested resource has been created successfully, the server MUST 
return a 201 Created status code"""


class GetResourceBase(Resource):
    pass


class CreateListResourceBase(GetResourceBase):

    def post(self):
        request_dict = request.get_json(force=True)
        try:
            self.mm_schema.validate(request_dict)
            modelInst = self.InstanceFromDict(request_dict)
            modelInst.add(modelInst)
            query = self.ModelClass.query.get(modelInst.id)
            results = self.mm_schema.dump(query).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


# basic collection of roles

class CreateListTeam(CreateListResourceBase):
    ModelClass = Team
    mm_schema = team_schema

    @use_kwargs({'name': webargs.fields.Str(required=False)})
    def get(self, name):
        query = self.ModelClass.query
        if name:
            query = query.filter_by(name=name)
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        return self.ModelClass(request_dict['name'], )


class CreateListPlayer(CreateListResourceBase):
    ModelClass = Player
    mm_schema = player_schema

    @use_kwargs({'name': webargs.fields.Str(required=False)})
    def get(self, name):
        query = self.ModelClass.query
        if name:
            query = query.filter_by(name=name)
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        team = None
        if request_dict.get('team', None):
            team = Team.query.get_or_404(request_dict.get('team', None))

        return self.ModelClass(name=request_dict['name'],
                               number=request_dict.get('number', None),
                               team=team)


class CreateListCampaign(CreateListResourceBase):
    ModelClass = Campaign
    mm_schema = campaign_schema

    @use_kwargs({'name': webargs.fields.Str(required=False)})
    def get(self, name):
        query = self.ModelClass.query
        if name:
            query = query.filter_by(name=name)
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        return self.ModelClass(request_dict['name'], )



class CreateListOpponent(CreateListResourceBase):
    ModelClass = Opponent
    mm_schema = opponent_schema

    @use_kwargs({'name': webargs.fields.Str(required=False)})
    def get(self, name):
        query = self.ModelClass.query
        if name:
            query = query.filter_by(name=name)
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        return self.ModelClass(request_dict['name'], )


class CreateListMatch(CreateListResourceBase):
    ModelClass = Match
    mm_schema = match_schema

    @use_kwargs({'opponent_id': webargs.fields.Int(required=False),
                 'team_id': webargs.fields.Int(required=False),
                 'campaign_id': webargs.fields.Int(required=False),
                 'at_home': webargs.fields.Bool(required=False),})
    def get(self, team_id, opponent_id, campaign_id, at_home):
        query = self.ModelClass.query

        if opponent_id:
            query = query.filter(self.ModelClass.opponent_id == opponent_id)

        if campaign_id:
            query = query.join(Campaign).filter(Campaign.id == campaign_id)

        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        campaign = None
        if request_dict['campaign']:
            campaign = Campaign.query.get_or_404(request_dict['campaign']['id'])

        modelInst = self.ModelClass(
            date_time=request_dict['date_time'].replace("+00:00", ""),
            team=Team.query.get_or_404(request_dict['team']['id']),
            opponent=Opponent.query.get_or_404(request_dict['opponent']['id']),
            campaign=campaign,
            at_home=request_dict['at_home']
            )
        return modelInst


class CreateListPlayerMatch(CreateListResourceBase):
    ModelClass = PlayerMatch
    mm_schema = playermatch_schema

    @use_kwargs({'player_id': webargs.fields.Int(required=False)})
    def get(self, player_id):
        query = self.ModelClass.query
        if player_id:
            query = query.join(Player).filter(Player.id == player_id)
        return self.mm_schema.dump(query.all(), many=True).data


    def InstanceFromDict(self, request_dict):
        player = db.session.query(Player).filter_by(id=request_dict['player']['id']).one()
        match = db.session.query(Match).filter_by(id=request_dict['match']['id']).one()
        modelInst = self.ModelClass(
                        player=player,
                        match=match,
                        started=request_dict['started'],
                        minutes=request_dict['minutes'],
                        subbed_due_to_injury=request_dict['subbed_due_to_injury'],
                        yellow_card=request_dict['yellow_card'],
                        red_card=request_dict['red_card'],
                        corners=request_dict['corners'],
                        )

        return modelInst

#
class CreateListShot(CreateListResourceBase):
    ModelClass = Shot
    mm_schema = shot_schema

    @use_kwargs({'playermatch_id': webargs.fields.Int(required=False)})
    def get(self, playermatch_id):
        query = self.ModelClass.query
        if playermatch_id:
            query = query.join(Player).filter(Player.id == playermatch_id)
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        player_match = db.session.query(PlayerMatch).filter_by(
                        id=request_dict['player_match']['id']).one()

        modelInst = self.ModelClass(
                        player_match=player_match,
                        x=request_dict['x'],
                        y=request_dict['y'],
                        on_goal=request_dict['on_goal'],
                        pk=request_dict['pk'],
                    )

        return modelInst

#
class CreateListShotAgainst(CreateListResourceBase):
    ModelClass = ShotAgainst
    mm_schema = shotagainst_schema

    @use_kwargs({'playermatch_id': webargs.fields.Int(required=False)})
    def get(self, playermatch_id):
        query = self.ModelClass.query
        if playermatch_id:
            query = query.join(Player).filter(Player.id == playermatch_id)
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        player_match = db.session.query(PlayerMatch).filter_by(
                        id=request_dict['player_match']['id']).one()
        modelInst = self.ModelClass(
                        player_match=player_match,
                        x=request_dict['x'],
                        y=request_dict['y'],
                        on_goal=request_dict['on_goal'],
                        pk=request_dict['pk'],
        )

        return modelInst

#
class CreateListGoal(CreateListResourceBase):
    ModelClass = Goal
    mm_schema = goal_schema

    @use_kwargs({'goal_id': webargs.fields.Int(required=False)})
    def get(self, goal_id):
        query = self.ModelClass.query
        if goal_id:
            query = query.join(Player).filter(Player.id == goal_id)
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        shot = db.session.query(Shot).filter_by(
                        id=request_dict['shot']['id']).one()
        modelInst = self.ModelClass(
                        shot=shot,
                        time=request_dict['time'],
        )

        return modelInst

#
class CreateListAssist(CreateListResourceBase):
    ModelClass = Assist
    mm_schema = assist_schema

    def get(self):
        query = self.ModelClass.query
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        goal = db.session.query(Goal).filter_by(
                        id=request_dict['goal']['id']).one()
        player_match = db.session.query(PlayerMatch).filter_by(
                        id=request_dict['player_match']['id']).one()
        modelInst = self.ModelClass(goal=goal, player_match=player_match, )

        return modelInst


# collections within relationships
class AddRemoveListTeamPlayer(GetResourceBase):
    ModelClass = Player
    mm_schema = player_schema

    def get(self, team_id=None):
        query = self.ModelClass.query.join(Team).filter(Team.id == team_id)
        return self.mm_schema.dump(query.all(), many=True).data


class AddRemoveListTeamMatch(GetResourceBase):
    ModelClass = Match
    mm_schema = match_schema

    def get(self, team_id):
        query = self.ModelClass.query.filter(Match.team_id == team_id)
        return self.mm_schema.dump(query.all(), many=True).data


class AddRemoveListPlayerPlayerMatch(GetResourceBase):
    ModelClass = PlayerMatch
    mm_schema = playermatch_schema

    def get(self, player_id):
        query = self.ModelClass.query.join(Player).filter(Player.id == player_id)
        return self.mm_schema.dump(query.all(), many=True).data


class AddRemoveListMatchPlayerMatch(GetResourceBase):
    ModelClass = PlayerMatch
    mm_schema = playermatch_schema

    def get(self, match_id=None):
        query = self.ModelClass.query.join(Match).filter(Match.id == match_id)
        return self.mm_schema.dump(query.all(), many=True).data


#
class GetUpdateDeleteResourceBase(Resource):
    """ base class that adds
        - get(id)
        - patch(id)
        - delete(id)
      """
    def get(self, id):
        query = self.ModelClass.query.get_or_404(id)
        return self.mm_schema.dump(query).data

    def patch(self, id):
        modelInst = self.ModelClass.query.get_or_404(id)
        request_dict = request.get_json(force=True)
        try:
            self.mm_schema.validate(request_dict, partial=True)
            for key, value in request_dict.items():
                setattr(modelInst, key, value)
            modelInst.update()
            return self.get(id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

    def delete(self, id):
        modelInst = self.ModelClass.query.get_or_404(id)
        try:
            modelInst.delete(modelInst)
            resp = make_response()
            resp.status_code = 204
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class GetUpdateDeleteTeam(GetUpdateDeleteResourceBase):
    ModelClass = Team
    mm_schema = team_schema

    def get(self, team_id):
        return super().get(team_id)

    def patch(self, team_id):
        return super().delete(team_id)

    def delete(self, team_id):
        resp = jsonify({"error": "Deleting of team not allowed!"})
        resp.status_code = 403
        return resp


class GetUpdateDeletePlayer(GetUpdateDeleteResourceBase):
    ModelClass = Player
    mm_schema = player_schema

    def get(self, player_id):
        query = Player.query.get_or_404(player_id)
        return player_schema.dump(query).data

    def patch(self, player_id):
        return super().patch(player_id)

    def delete(self, player_id):
        resp = jsonify({"error": "Deleting of player not allowed!"})
        resp.status_code = 403
        return resp


class GetUpdateDeleteMatch(GetUpdateDeleteResourceBase):
    ModelClass = Match
    mm_schema = match_schema

    def get(self, match_id):
        query = Match.query.get_or_404(match_id)
        return match_schema.dump(query).data

    def patch(self, match_id):
        return super().patch(match_id)

    def delete(self, match_id):
        return super().delete(match_id)


class GetUpdateDeleteCampaign(GetUpdateDeleteResourceBase):
    ModelClass = Campaign
    mm_schema = campaign_schema

    def get(self, campaign_id):
        query = Campaign.query.get_or_404(campaign_id)
        return campaign_schema.dump(query).data

    def patch(self, campaign_id):
        return super().patch(campaign_id)

    def delete(self, campaign_id):
        return super().delete(campaign_id)


class GetUpdateDeleteOpponent(GetUpdateDeleteResourceBase):
    ModelClass = Opponent
    mm_schema = opponent_schema

    def get(self, opponent_id):
        query = Opponent.query.get_or_404(opponent_id)
        return opponent_schema.dump(query).data

    def patch(self, opponent_id):
        return super().patch(opponent_id)

    def delete(self, opponent_id):
        return super().delete(opponent_id)


class GetUpdateDeletePlayerMatch(GetUpdateDeleteResourceBase):
    ModelClass = PlayerMatch
    mm_schema = playermatch_schema

    def get(self, playermatch_id):
        query = PlayerMatch.query.get_or_404(playermatch_id)
        return playermatch_schema.dump(query).data

    def patch(self, playermatch_id):
        return super().patch(playermatch_id)

    def delete(self, playermatch_id):
        return super().delete(playermatch_id)


#
class GetUpdateDeleteMatch(GetUpdateDeleteResourceBase):
    ModelClass = Match
    mm_schema = match_schema

    def get(self, match_id):
        query = Match.query.get_or_404(match_id)
        return match_schema.dump(query).data

    def patch(self, match_id):
        return super().patch(match_id)

    def delete(self, match_id):
        return super().delete(match_id)


#
class GetUpdateDeleteShot(GetUpdateDeleteResourceBase):
    ModelClass = Shot
    mm_schema = shot_schema

    def get(self, shot_id):
        query = Shot.query.get_or_404(shot_id)
        return match_schema.dump(query).data

    def patch(self, shot_id):
        return super().patch(shot_id)

    def delete(self, shot_id):
        return super().delete(shot_id)

#
class GetUpdateDeleteShotAgainst(GetUpdateDeleteResourceBase):
    ModelClass = ShotAgainst
    mm_schema = shotagainst_schema

    def get(self, shotagainst_id):
        query = Shot.query.get_or_404(shotagainst_id)
        return match_schema.dump(query).data

    def patch(self, shotagainst_id):
        return super().patch(shotagainst_id)

    def delete(self, shotagainst_id):
        return super().delete(shotagainst_id)


class GetUpdateDeleteGoal(GetUpdateDeleteResourceBase):
    ModelClass = Goal
    mm_schema = goal_schema

    def get(self, goal_id):
        query = Goal.query.get_or_404(goal_id)
        return match_schema.dump(query).data

    def patch(self, goal_id):
        return super().patch(goal_id)

    def delete(self, goal_id):
        return super().delete(goal_id)

#
class GetUpdateDeleteAssist(GetUpdateDeleteResourceBase):
    ModelClass = Assist
    mm_schema = assist_schema

    def get(self, assist_id):
        query = Assist.query.get_or_404(assist_id)
        return match_schema.dump(query).data

    def patch(self, assist_id):
        return super().patch(assist_id)

    def delete(self, assist_id):
        return super().delete(assist_id)
