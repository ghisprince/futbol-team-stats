from flask_restful import Resource

from flask import request
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs

from flask_jwt_extended import (create_access_token,
                                jwt_required,
                                get_jwt_identity,
                                get_raw_jwt,
                                jwt_refresh_token_required,
                                create_refresh_token)


from . models import *
from . schemas import *

import marshmallow
from marshmallow import ValidationError
import webargs
from pprint import pprint


# initialize instance of each Schema class
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


"""
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)
"""

def generate_tokens(username):
    access_token = create_access_token(identity=username, fresh=True)
    refresh_token = create_refresh_token(identity=username)

    return {'access_token': access_token,
            'refresh_token': refresh_token }

class UserLogin(Resource):
    @use_kwargs({'username': webargs.fields.Str(required=True),
                 'password': webargs.fields.Str(required=True) })
    def post(self, username, password):
        user = User.get_by_username(username)
        try:

            if not user:
                raise

            if user.check_password(password):
                resp = generate_tokens(user.username)
                resp['is_editor'] = user.is_editor
                resp['is_admin'] = False #user.is_admin
                resp['username'] = user.username
                resp['message'] = f'User {user.username} was logged in'

                return resp, 200
            else:
                raise
        except:
            return {'message': 'Login failed'}, 401


class UserLogout(Resource):
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}, 200
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutR(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}, 200
        except:
            return {'message': 'Something went wrong'}, 500


class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class CreateListResourceBase(Resource):
    @jwt_refresh_token_required
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

    @jwt_refresh_token_required
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
            return {"error": err.messages}, 400

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 400


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

    @jwt_refresh_token_required
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

    @jwt_refresh_token_required
    @use_kwargs({'player_id': webargs.fields.Int(required=False),
                 'match_id': webargs.fields.Int(required=False),
                 'competition_id': webargs.fields.Int(required=False),
                 'by_opponent': webargs.fields.Bool(required=False),
                 'expand': webargs.fields.Bool(required=False)})
    def get(self, player_id, match_id, competition_id, by_opponent, expand):
        query = self.ModelClass.query

        if player_id:
            query = query.join(PlayerMatch).join(Player).filter(
                Player.id == player_id)

        if match_id:
            query = query.join(PlayerMatch).join(Match).filter(
                Match.id == match_id)

        if competition_id:
            query = query.join(PlayerMatch).join(Match).join(Competition).filter(
                Competition.id == competition_id)

        if not isinstance(by_opponent, marshmallow.utils._Missing):
            query = query.filter(Shot.by_opponent == by_opponent)

        if expand:
            return self.mm_schema_ex.dump(query.all(), many=True).data

        return self.mm_schema.dump(query.all(), many=True).data

    @jwt_refresh_token_required
    def post(self):
        shot_dict, _ = super().post()
        request_dict = request.get_json(force=True)

        shot = self.ModelClass.query.get(shot_dict['id'])

        goal_dict = request_dict.pop('goal', None)
        if goal_dict:
            shot.on_target = True
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

            shot.goal = goal

        # todo: add goal/assist?
        db.session.commit()
        return self.mm_schema.dump(shot).data, 200

class CreateListGoal(CreateListResourceBase):
    ModelClass = Goal
    mm_schema = goal_schema

    @jwt_refresh_token_required
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


    @jwt_refresh_token_required
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

    @jwt_refresh_token_required
    @use_kwargs({'expand': webargs.fields.Bool(required=False)})
    def get(self, id, expand=False):
        query = self.ModelClass.query.get_or_404(id)
        if expand:
            return self.mm_schema_ex.dump(query).data
        return self.mm_schema.dump(query).data

    @jwt_refresh_token_required
    def patch(self, id):
        modelInst = self.ModelClass.query.get_or_404(id)
        request_dict = request.get_json(force=True)

        try:
            self.mm_schema.validate(request_dict, partial=True)
            modelInst = self.mm_schema.load(request_dict, partial=True)
            db.session.commit()
            return self.get(id)

        except ValidationError as err:
            return {"error": err.messages}, 400

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    @jwt_refresh_token_required
    def delete(self, id):
        modelInst = self.ModelClass.query.get_or_404(id)
        for att in ['matches', 'playermatches', ]:
            if getattr(modelInst, att, None):
                return {"error": "Delete failed, object has associated " + att}, 403

        try:
            modelInst.delete(modelInst)
            return {}, 204

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 400


class GetUpdateDeleteTeam(GetUpdateDeleteResourceBase):
    ModelClass = Team
    mm_schema = team_schema
    mm_schema = team_schema_ex

    @jwt_refresh_token_required
    def delete(self, id):
        return {"error": "Deleting of team not allowed!"}, 403


class GetUpdateDeletePlayer(GetUpdateDeleteResourceBase):
    ModelClass = Player
    mm_schema = player_schema
    mm_schema = player_schema_ex

    @jwt_refresh_token_required
    def delete(self, id):
        return {"error": "Deleting of player not allowed!"}, 403


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

    @jwt_refresh_token_required
    def patch(self, id):
        request_dict = request.get_json(force=True)
        shot = self.ModelClass.query.get_or_404(id)
        goal_dict = request_dict.pop('goal', {})
        if goal_dict:
            assist_dict = goal_dict.pop('assist', {})

        if request_dict['scored'] == True and goal_dict:
            shot.on_target = True
            goal_dict['shot'] = id
            goal_schema.validate(goal_dict, partial=True)

            if shot.goal is None:
                # new Goal
                goal = goal_schema.load(goal_dict, partial=True).data
                db.session.add(goal)
                db.session.commit()
                shot.goal = goal

            else:
                # update existing Goal
                goal = Goal.query.get_or_404(goal_dict['id']) # this overwritten on next line?
                goal = goal_schema.load(goal_dict, partial=True).data

            if (goal_dict['assisted'] == True) and assist_dict:
                assist_dict['goal'] = shot.goal.id

                if shot.goal.assist is None:
                    # add new Assist (this seems wrong)
                    assist_dict.pop('id')
                    assist = assist_schema.load(assist_dict, partial=True).data
                else:
                    # update existing Assist
                    assist_schema.validate(assist_dict, partial=True)
                    assist = assist_schema.load(assist_dict).data
                db.session.add(assist)

            elif shot.goal and shot.goal.assist:
                assist = shot.goal.assist
                db.session.delete(assist)

        else:
            if shot.goal:
                goal = shot.goal
                db.session.delete(goal)

        db.session.commit()
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
