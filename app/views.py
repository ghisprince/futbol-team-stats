from flask_restful import Resource

from flask import jsonify, make_response, request
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs

from app.models import *
from app.schemas import *
from marshmallow import ValidationError
import webargs
from pprint import pprint

team_schema = TeamSchema()
team_schema_ex = TeamSchemaEx()

player_schema = PlayerSchema()
player_schema_ex = PlayerSchemaEx()

match_schema = MatchSchema()
match_schema_ex = MatchSchemaEx()

competition_schema = CompetitionSchema()
competition_schema_ex = CompetitionSchemaEx()

opponent_schema = OpponentSchema()
opponent_schema_ex = OpponentSchemaEx()

playermatch_schema = PlayerMatchSchema()
playermatch_schema_ex = PlayerMatchSchemaEx()

shot_schema = ShotSchema()
shot_schema_ex = ShotSchemaEx()

goal_schema = GoalSchema()
goal_schema_ex = GoalSchemaEx()

assist_schema = AssistSchema()
assist_schema_ex = AssistSchemaEx()

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


class CreateListResourceBase(Resource):
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
    mm_schema_ex = team_schema_ex

    @use_kwargs({'name': webargs.fields.Str(required=False),
                 'expand': webargs.fields.Bool(required=False)})
    def get(self, name, expand):
        query = self.ModelClass.query
        if name:
            query = query.filter_by(name=name)
        if expand:
            return self.mm_schema_ex.dump(query.all(), many=True).data
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        return self.ModelClass(**request_dict)



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
        if request_dict.get('team'):
            request_dict['team'] = Team.query.get_or_404(
                                        request_dict.get('team', None))
        return self.ModelClass(**request_dict)


class CreateListCompetition(CreateListResourceBase):
    ModelClass = Competition
    mm_schema = competition_schema
    mm_schema_ex = competition_schema_ex

    @use_kwargs({'name': webargs.fields.Str(required=False),
                 'expand': webargs.fields.Bool(required=False)})
    def get(self, name, expand):

        query = self.ModelClass.query
        if name:
            query = query.filter_by(name=name)
        if expand:
            return self.mm_schema_ex.dump(query.all(), many=True).data
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        return self.ModelClass(**request_dict)


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
        return self.ModelClass(**request_dict)


class CreateListMatch(CreateListResourceBase):
    ModelClass = Match
    mm_schema = match_schema
    mm_schema_ex = match_schema_ex

    @use_kwargs({'opponent_id': webargs.fields.Int(required=False),
                 'competition_id': webargs.fields.Int(required=False),
                 'expand': webargs.fields.Bool(required=False)
                 })
    def get(self, opponent_id, competition_id, expand=False):
        query = self.ModelClass.query

        if opponent_id:
            query = query.filter(self.ModelClass.opponent_id == opponent_id)

        if competition_id:
            query = query.join(Competition).filter(Competition.id == competition_id)

        if expand:
            return self.mm_schema_ex.dump(query.all(), many=True).data
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):

        request_dict['team'] = Team.query.get_or_404(request_dict['team']['id'])
        request_dict['opponent'] = Opponent.query.get_or_404(
            request_dict['opponent']['id'])

        if request_dict.get('competition', None):
            request_dict['competition'] = Competition.query.get_or_404(
                                            request_dict['competition']['id'])

        return self.ModelClass(**request_dict)


class CreateListPlayerMatch(CreateListResourceBase):
    ModelClass = PlayerMatch
    mm_schema = playermatch_schema
    mm_schema_ex = playermatch_schema_ex

    @use_kwargs({'player_id': webargs.fields.Int(required=False),
                 'match_id': webargs.fields.Int(required=False),
                 'competition_id': webargs.fields.Int(required=False),
                 'expand': webargs.fields.Bool(required=False)})
    def get(self, player_id, match_id, competition_id, expand=False):

        query = self.ModelClass.query
        if player_id:
            query = query.join(Player).filter(Player.id == player_id)

        if match_id:
            query = query.filter_by(match_id=match_id)

        if competition_id:
            query = query.join(Match).join(Competition).filter(
                        Competition.id == competition_id)

        if expand:
            return self.mm_schema_ex.dump(query.all(), many=True).data
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):

        request_dict['player'] = db.session.query(Player).filter_by(
                                      id=request_dict['player']['id']).one()

        request_dict['match'] = db.session.query(Match).filter_by(
                                    id=request_dict['match']['id']).one()

        return self.ModelClass(**request_dict)


class CreateListShot(CreateListResourceBase):
    ModelClass = Shot
    mm_schema = shot_schema
    mm_schema_ex = shot_schema_ex

    @use_kwargs({'player_id': webargs.fields.Int(required=False),
                 'match_id': webargs.fields.Int(required=False),
                 'expand': webargs.fields.Bool(required=False)})
    def get(self, player_id, match_id, expand):
        query = self.ModelClass.query
        if player_id:
            query = query.join(PlayerMatch).join(Player).filter(
                                                Player.id == player_id)

        if match_id:
            query = query.join(PlayerMatch).join(Match).filter(
                                                Match.id == match_id)

        if expand:
            return self.mm_schema_ex.dump(query.all(), many=True).data

        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        request_dict['player_match'] = db.session.query(
            PlayerMatch).filter_by(id=request_dict['player_match']['id']).one()

        return self.ModelClass(**request_dict)


class CreateListGoal(CreateListResourceBase):
    ModelClass = Goal
    mm_schema = goal_schema

    @use_kwargs({'player_id': webargs.fields.Int(required=False),
                 'match_id': webargs.fields.Int(required=False), })
    def get(self, player_id, match_id):
        query = self.ModelClass.query
        if player_id:
            query = query.join(Shot).join(PlayerMatch).join(Player).filter(
                                                Player.id == player_id)

        if match_id:
            query = query.join(Shot).filter(Match.id == match_id)
        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        request_dict['shot'] = db.session.query(Shot).filter_by(
                                    id=request_dict['shot']['id']).one()

        return self.ModelClass(**request_dict)


class CreateListAssist(CreateListResourceBase):
    ModelClass = Assist
    mm_schema = assist_schema

    @use_kwargs({'player_id': webargs.fields.Int(required=False),
                 'match_id': webargs.fields.Int(required=False), })
    def get(self, player_id, match_id):
        query = self.ModelClass.query
        if player_id:
            query = query.join(PlayerMatch).join(Player).filter(
                                                Player.id == player_id)

        if match_id:
            query = query.filter(Match.id == match_id)

        return self.mm_schema.dump(query.all(), many=True).data

    def InstanceFromDict(self, request_dict):
        request_dict['goal'] = db.session.query(
                        Goal).filter_by(id=request_dict['goal']['id']).one()

        request_dict['player_match'] = db.session.query(
                        PlayerMatch).filter_by(
                            id=request_dict['player_match']['id']).one()

        return self.ModelClass(**request_dict)


"""
# collections within relationships
class AddRemoveListTeamPlayer(Resource):
    ModelClass = Player
    mm_schema = player_schema

    def get(self, team_id=None):
        query = self.ModelClass.query.join(Team).filter(Team.id == team_id)
        return self.mm_schema.dump(query.all(), many=True).data


class AddRemoveListTeamMatch(Resource):
    ModelClass = Match
    mm_schema = match_schema

    def get(self, team_id):
        query = self.ModelClass.query.filter(Match.team_id == team_id)
        return self.mm_schema.dump(query.all(), many=True).data
"""

#
class GetUpdateDeleteResourceBase(Resource):
    """ base class that adds
        - get(id)
        - patch(id)
        - delete(id)
      """

    def get(self, id, expand=False):
        query = self.ModelClass.query.get_or_404(id)
        if expand:
            return self.mm_schema_ex.dump(query).data
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
        for att in ['matches', 'playermatches', ]:
            if getattr(modelInst, att, None):
                resp = jsonify({"error": "Delete failed, object has associated " + att})
                resp.status_code = 401
                return resp

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
    mm_schema_ex = team_schema_ex

    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, team_id, expand=False):
        return super().get(team_id, expand)

    def patch(self, team_id):
        return super().delete(team_id)

    def delete(self, team_id):
        resp = jsonify({"error": "Deleting of team not allowed!"})
        resp.status_code = 403
        return resp


class GetUpdateDeletePlayer(GetUpdateDeleteResourceBase):
    ModelClass = Player
    mm_schema = player_schema
    mm_schema_ex = player_schema_ex

    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, player_id, expand=False):
        return super().get(player_id, expand)

    def patch(self, player_id):
        return super().patch(player_id)

    def delete(self, player_id):
        resp = jsonify({"error": "Deleting of player not allowed!"})
        resp.status_code = 403
        return resp


class GetUpdateDeleteMatch(GetUpdateDeleteResourceBase):
    ModelClass = Match
    mm_schema = match_schema
    mm_schema_ex = match_schema_ex

    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, match_id, expand=False):
        return super().get(match_id, expand)

    def delete(self, match_id):
        return super().delete(match_id)


class GetUpdateDeleteCompetition(GetUpdateDeleteResourceBase):
    ModelClass = Competition
    mm_schema = competition_schema
    mm_schema_ex = competition_schema_ex

    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, competition_id, expand=False):
        return super().get(competition_id, expand)

    def patch(self, competition_id):
        return super().patch(competition_id)

    def delete(self, competition_id):
        return super().delete(competition_id)


class GetUpdateDeleteOpponent(GetUpdateDeleteResourceBase):
    ModelClass = Opponent
    mm_schema = opponent_schema
    mm_schema_ex = opponent_schema_ex

    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, opponent_id, expand=False):
        return super().get(opponent_id, expand)

    def patch(self, opponent_id):
        return super().patch(opponent_id)

    def delete(self, opponent_id):
        return super().delete(opponent_id)


class GetUpdateDeletePlayerMatch(GetUpdateDeleteResourceBase):
    ModelClass = PlayerMatch
    mm_schema = playermatch_schema
    mm_schema_ex = playermatch_schema_ex

    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, playermatch_id, expand=False):
        return super().get(playermatch_id, expand)

    def patch(self, playermatch_id):
        return super().patch(playermatch_id)

    def delete(self, playermatch_id):
        return super().delete(playermatch_id)


class GetUpdateDeleteMatch(GetUpdateDeleteResourceBase):
    ModelClass = Match
    mm_schema = match_schema
    mm_schema_ex = match_schema_ex

    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, match_id, expand=False):
        from pprint import pprint
        return super().get(match_id, expand)

    def patcho(self, match_id):
        return super().patch(match_id)

    def patch(self, match_id):

        modelInst = self.ModelClass.query.get_or_404(match_id)

        request_dict = request.get_json(force=True)

        request_dict['team'] = db.session.query(
            Team).filter_by(id=request_dict['team']['id']).one()

        print("#"*40)
        pprint(request_dict)
        print("#"*40)
        request_dict['opponent'] = db.session.query(
            Opponent).filter_by(id=request_dict['opponent']['id']).one()

        request_dict['competition'] = db.session.query(
            Competition).filter_by(id=request_dict['competition']['id']).one()

        request_dict['date_time'] = datetime.datetime.strptime(
                                        request_dict['date_time'][:-6],
                                                        "%Y-%m-%dT%H:%M:%S")
        try:
            #self.mm_schema.validate(request_dict, partial=True)
            for key, value in request_dict.items():
                setattr(modelInst, key, value)
            modelInst.update()
            return self.get(match_id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

    def delete(self, match_id):
        return super().delete(match_id)


class GetUpdateDeleteShot(GetUpdateDeleteResourceBase):
    ModelClass = Shot
    mm_schema = shot_schema
    mm_schema_ex = shot_schema_ex

    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, shot_id, expand=False):
        return super().get(shot_id, expand)

    def patch(self, shot_id):
        return super().patch(shot_id)

    def delete(self, shot_id):
        return super().delete(shot_id)


class GetUpdateDeleteGoal(GetUpdateDeleteResourceBase):
    ModelClass = Goal
    mm_schema = goal_schema
    mm_schema_ex = goal_schema_ex

    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, goal_id, expand=False):
        return super().get(goal_id, expand)

    def patch(self, goal_id):
        return super().patch(goal_id)

    def delete(self, goal_id):
        return super().delete(goal_id)


class GetUpdateDeleteAssist(GetUpdateDeleteResourceBase):
    ModelClass = Assist
    mm_schema = assist_schema
    mm_schema_ex = assist_schema_ex

    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, assist_id, expand=False):
        return super().get(assist_id, expand)

    def patch(self, assist_id):
        return super().patch(assist_id)

    def delete(self, assist_id):
        return super().delete(assist_id)
