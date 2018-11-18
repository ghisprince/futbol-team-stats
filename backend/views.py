import flask_restful
import flask_login

from flask import jsonify, make_response, request
from flask import session as flask_session
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs

from . models import *
from . schemas import *
from flask_login import login_required

import marshmallow
from marshmallow import ValidationError
import webargs
from pprint import pprint
import json

"""
This module servers views of the model as REST api

This module should be refactored to be DRY-er.

"""

user_schema = UserSchema()

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

matchstats_schema = MatchStatsSchema()

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


# decorate all with end points with login_required
class Resource(flask_restful.Resource):
    #method_decorators = [login_required]
    pass


class CreateListResourceBase(Resource):
    @use_kwargs({'name': webargs.fields.Str(required=False),
                 'player_id': webargs.fields.Int(required=False),
                 'match_id': webargs.fields.Int(required=False),
                 'competition_id': webargs.fields.Int(required=False),
                 'opponent_id': webargs.fields.Int(required=False),
                 'expand': webargs.fields.Bool(required=False)})
    def get(self, name, player_id, match_id, competition_id, opponent_id, expand=False):
        query = self.ModelClass.query
        if name:
            query = query.filter_by(name=name)

        if player_id:
            query = query.join(Player).filter(Player.id == player_id)

        if match_id:
            query = query.join(Match).filter(Match.id == match_id)

        if competition_id:
            query = query.join(Match).join(Competition).filter(
                Competition.id == competition_id)

        if opponent_id:
            query = query.join(Match).join(Opponent).filter(
                Opponent.id == opponent_id)

        if expand:
            return self.mm_schema_ex.dump(query.all(), many=True).data

        return self.mm_schema.dump(query.all(), many=True).data

    def post(self):
        request_dict = request.get_json(force=True)
        try:
            self.mm_schema.validate(request_dict)
            modelInst = self.mm_schema.load(request_dict).data

            db.session.add(modelInst)
            db.session.commit()

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

class CreateListPlayer(CreateListResourceBase):
    ModelClass = Player
    mm_schema = player_schema

class CreateListCompetition(CreateListResourceBase):
    ModelClass = Competition
    mm_schema = competition_schema
    mm_schema_ex = competition_schema_ex

class CreateListOpponent(CreateListResourceBase):
    ModelClass = Opponent
    mm_schema = opponent_schema

class CreateListMatch(CreateListResourceBase):
    ModelClass = Match
    mm_schema = match_schema
    mm_schema_ex = match_schema_ex

    @use_kwargs({'opponent_id': webargs.fields.Int(required=False),
                 'competition_id': webargs.fields.Int(required=False) })
    def get(self, opponent_id, competition_id):
        query = self.ModelClass.query

        if opponent_id:
            query = query.filter(self.ModelClass.opponent_id == opponent_id)

        if competition_id:
            query = query.join(Competition).filter(
                Competition.id == competition_id)

        return self.mm_schema.dump(query.all(), many=True).data

class CreateListPlayerMatch(CreateListResourceBase):
    ModelClass = PlayerMatch
    mm_schema = playermatch_schema
    mm_schema_ex = playermatch_schema_ex

class CreateListMatchStats(CreateListResourceBase):
    ModelClass = MatchStats
    mm_schema = matchstats_schema

class CreateListShot(CreateListResourceBase):
    ModelClass = Shot
    mm_schema = shot_schema
    mm_schema_ex = shot_schema_ex

    @use_kwargs({'player_id': webargs.fields.Int(required=False),
                 'match_id': webargs.fields.Int(required=False),
                 'by_opponent': webargs.fields.Bool(required=False),
                 'expand': webargs.fields.Bool(required=False)})
    def get(self, player_id, match_id, by_opponent, expand):
        query = self.ModelClass.query

        if player_id:
            query = query.join(PlayerMatch).join(Player).filter(
                Player.id == player_id)

        if match_id:
            query = query.join(PlayerMatch).join(Match).filter(
                Match.id == match_id)

        if not isinstance(by_opponent, marshmallow.utils._Missing):
            query = query.filter(Shot.by_opponent == by_opponent)

        if expand:
            return self.mm_schema_ex.dump(query.all(), many=True).data

        return self.mm_schema.dump(query.all(), many=True).data

    def post(self):
        shot_dict, _ = super().post()
        request_dict = request.get_json(force=True)

        query = self.ModelClass.query.get(shot_dict['id'])

        goal_dict = request_dict.pop('goal', None)
        if goal_dict:
            goal_dict['shot'] = shot_dict['id']
            goal_schema.validate(goal_dict)
            goal = goal_schema.load(goal_dict).data
            db.session.commit()

            assist_dict = goal_dict.pop('assist', None)
            if assist_dict and assist_dict['player_match']:
                assist_dict.pop('id')
                assist_dict['goal'] = goal.id
                assist_schema.validate(assist_dict)
                assist = assist_schema.load(assist_dict).data

            query.goal = goal

        # todo: add goal/assist?
        db.session.commit()
        results = self.mm_schema.dump(query).data
        return results, 201

class CreateListGoal(CreateListResourceBase):
    ModelClass = Goal
    mm_schema = goal_schema

    @use_kwargs({'player_id': webargs.fields.Int(required=False),
                 'match_id': webargs.fields.Int(required=False),
                 'playermatch_id': webargs.fields.Int(required=False), })
    def get(self, player_id, match_id, playermatch_id):
        query = self.ModelClass.query

        if player_id:
            query = query.join(Shot).join(PlayerMatch).join(Player).filter(
                Player.id == player_id)

        if playermatch_id:
            query = query.join(Shot).join(PlayerMatch).filter(
                PlayerMatch.id == playermatch_id)

        if match_id:
            query = query.join(Shot).join(PlayerMatch).join(Match).filter(
                Match.id == match_id)

        return self.mm_schema.dump(query.all(), many=True).data

class CreateListAssist(CreateListResourceBase):
    ModelClass = Assist
    mm_schema = assist_schema

    @use_kwargs({'player_id': webargs.fields.Int(required=False),
                 'match_id': webargs.fields.Int(required=False),
                 'playermatch_id': webargs.fields.Int(required=False)})
    def get(self, player_id, match_id, playermatch_id):
        query = self.ModelClass.query

        if player_id:
            query = query.join(PlayerMatch).join(Player).filter(
                Player.id == player_id)

        if match_id:
            query = query.join(PlayerMatch).join(Match).filter(Match.id == match_id)

        if playermatch_id:
            query = query.join(PlayerMatch).filter(PlayerMatch.id == playermatch_id)

        return self.mm_schema.dump(query.all(), many=True).data


class GetUpdateDeleteResourceBase(Resource):
    """ base class that adds
        - get(id)
        - patch(id)
        - delete(id)
      """

    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, id, expand=False):
        query = self.ModelClass.query.get_or_404(id)
        if expand:
            return self.mm_schema_ex.dump(query).data
        return self.mm_schema.dump(query).data

    def patch(self, id):
        modelInst = self.ModelClass.query.get_or_404(id)

        request_dict = request.get_json(force=True)
        pprint(request_dict)
        try:
            self.mm_schema.validate(request_dict, partial=True)
            modelInst = self.mm_schema.load(request_dict, partial=True)
            db.session.commit()
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
                resp = jsonify(
                    {"error": "Delete failed, object has associated " + att})
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


class GetCurrentUserID(Resource):  # not GetUpdateDeleteResourceBase
    mm_schema = user_schema

    def get(self, ):
        query = User.query.get_or_404(flask_login.current_user.get_id())
        return self.mm_schema.dump(query).data


class GetCurrentTeamID(Resource):  # not GetUpdateDeleteResourceBase
    mm_schema = team_schema

    def get(self, ):
        team_id = flask_session.get('current_team', None)
        if team_id is None:
            # if no current_team, then get first from current_user
            current_user = User.query.get_or_404(flask_login.current_user.get_id())
            try:
                team_id = current_user.teams[0].id
            except:
                raise ValueError("Need an active team")

        return json.dumps(team_id)

    def post(self):
        request_dict = request.get_json(force=True)

        if not request_dict in [i.id for i in User.query.get_or_404(flask_login.current_user.get_id()).teams]:
            raise ValueError("User not associated with this team")

        team = Team.query.get_or_404(request_dict)
        flask_session['current_team'] = team.id
        return json.dumps(team.id)


class GetUpdateDeleteTeam(GetUpdateDeleteResourceBase):
    ModelClass = Team
    mm_schema = team_schema
    mm_schema = team_schema_ex

    def delete(self, id):
        resp = jsonify({"error": "Deleting of team not allowed!"})
        resp.status_code = 403
        return resp


class GetUpdateDeletePlayer(GetUpdateDeleteResourceBase):
    ModelClass = Player
    mm_schema = player_schema
    mm_schema = player_schema_ex

    def delete(self, id):
        resp = jsonify({"error": "Deleting of player not allowed!"})
        resp.status_code = 403
        return resp


class GetUpdateDeleteMatch(GetUpdateDeleteResourceBase):
    ModelClass = Match
    mm_schema = match_schema
    mm_schema_ex = match_schema_ex

class GetUpdateDeleteMatchStats(GetUpdateDeleteResourceBase):
    ModelClass = MatchStats
    mm_schema = matchstats_schema
    mm_schema_ex = None # todo ?

class GetUpdateDeleteCompetition(GetUpdateDeleteResourceBase):
    ModelClass = Competition
    mm_schema = competition_schema
    mm_schema_ex = competition_schema_ex

class GetUpdateDeleteOpponent(GetUpdateDeleteResourceBase):
    ModelClass = Opponent
    mm_schema = opponent_schema
    mm_schema_ex = opponent_schema_ex

class GetUpdateDeletePlayerMatch(GetUpdateDeleteResourceBase):
    ModelClass = PlayerMatch
    mm_schema = playermatch_schema
    mm_schema_ex = playermatch_schema_ex

class GetUpdateDeleteMatch(GetUpdateDeleteResourceBase):
    ModelClass = Match
    mm_schema = match_schema
    mm_schema_ex = match_schema_ex

class GetUpdateDeleteShot(GetUpdateDeleteResourceBase):
    ModelClass = Shot
    mm_schema = shot_schema
    mm_schema_ex = shot_schema_ex

    def patch(self, id):
        request_dict = request.get_json(force=True)
        modelInst = self.ModelClass.query.get_or_404(id)
        print(">"*30)
        goal_dict = request_dict.pop('goal', {})
        if goal_dict:
            assist_dict = goal_dict.pop('assist', {})

        if request_dict['scored'] == True and goal_dict:
            goal_dict['shot'] = id
            goal_schema.validate(goal_dict, partial=True)

            if modelInst.goal is None:
                # add new Goal
                goal = goal_schema.load(goal_dict, partial=True).data
                print("Add Goal {}".format(goal))

            else:
                # update existing Goal
                # TODO : isthis first get_or_404 needed?
                goal = Goal.query.get_or_404(goal_dict['id'])
                goal = goal_schema.load(goal_dict, partial=True).data
                print("Update Goal {}".format(goal))

            if (goal_dict['assisted'] == True) and assist_dict:
                assist_dict['goal'] = modelInst.goal.id

                if modelInst.goal.assist is None:
                    # add new Assist
                    # todo : this seemswrong
                    assist_dict.pop('id')
                    assist = assist_schema.load(assist_dict, partial=True).data
                    print("Add Assist {}".format(assist))
                else:
                    # update existing Assist
                    assist_schema.validate(assist_dict, partial=True)
                    assist = assist_schema.load(assist_dict).data
                    print("Update Assist {}".format(assist))
            elif modelInst.goal and modelInst.goal.assist:
                assist = modelInst.goal.assist
                db.session.delete(assist)
                print("Delete Assist")

        else:
            if modelInst.goal:
                goal = modelInst.goal
                db.session.delete(goal)
                print("Delete Goal")

        db.session.commit()
        print("<"*30)
        print("now patch the shot")
        print(">"*30)
        # finally patch the shot's main properties
        return super().patch(id)


class GetUpdateDeleteGoal(GetUpdateDeleteResourceBase):
    ModelClass = Goal
    mm_schema = goal_schema
    mm_schema_ex = goal_schema_ex

class GetUpdateDeleteAssist(GetUpdateDeleteResourceBase):
    ModelClass = Assist
    mm_schema = assist_schema
    mm_schema_ex = assist_schema_ex