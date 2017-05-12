from flask_restful import Resource
from flask import jsonify, make_response, request
from sqlalchemy.exc import SQLAlchemyError

from .models import *
from .schemas import *
from marshmallow import ValidationError


team_schema = TeamSchema(strict=True)
player_schema = PlayerSchema(strict=True)
match_schema = MatchSchema(strict=True)
campaign_schema = CampaignSchema(strict=True)
playermatch_schema = PlayerMatchSchema(strict=True)

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
    def get(self):
        query = self.dbModel.query.all()
        return self.mm_schema.dump(query, many=True).data

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            #import pdb;pdb.set_trace()
            self.mm_schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            dbModelInst = self.dbModelInstFromDict(request_dict)
            dbModelInst.add(dbModelInst)
            query = self.dbModel.query.get(dbModelInst.id)
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


class GetUpdateDeleteResourceBase(Resource):
    def get(self, id):
        print("YEAH 1")
        query = self.dbModel.query.get_or_404(id)
        return self.mm_schema.dump(query).data

    def patch(self, id):
        dbModelInst = self.dbModel.query.get_or_404(id)
        raw_dict = request.get_json(force=True)
        try:
            self.mm_schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(dbModelInst, key, value)

            dbModelInst.update()
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

class CreateListTeam(CreateListResourceBase):
    dbModel = Team
    mm_schema = team_schema

    def dbModelInstFromDict(self, request_dict):
        return self.dbModel(request_dict['name'], )

class CreateListCampaign(CreateListResourceBase):
    dbModel = Campaign
    mm_schema = campaign_schema

    def dbModelInstFromDict(self, request_dict):
        return self.dbModel(request_dict['name'], )


class CreateListMatch(CreateListResourceBase):
    dbModel = Match
    mm_schema = match_schema

    def dbModelInstFromDict(self, request_dict):
        # THIS IS ALL WRONG
        dbModelInst = self.dbModel(date_time=request_dict['date_time'].replace("+00:00",""),
                                   home_team=Team.query.get_or_404(request_dict['home_team']['data']['id']),
                                   away_team=Team.query.get_or_404(request_dict['away_team']['data']['id']),
                                   campaign=Campaign.query.get_or_404(request_dict['campaign']['data']['id']),
                                   )
        return dbModelInst


class CreateListPlayer(CreateListResourceBase):
    dbModel = Player
    mm_schema = player_schema

    def dbModelInstFromDict(self, request_dict):
        return self.dbModel(request_dict['name'], request_dict['number'],)


class CreateListPlayerMatch(CreateListResourceBase):
    dbModel = PlayerMatch
    mm_schema = playermatch_schema

    def dbModelInstFromDict(self, request_dict):
        import pdb;pdb.set_trace()
        player = db.session.query(Player).filter_by(id=request_dict['player']['data']['id']).one()
        match = db.session.query(Match).filter_by(id=request_dict['match']['data']['id']).one()
        team = db.session.query(Team).filter_by(id=request_dict['team']['data']['id']).one()
        dbModelInst = self.dbModel(player=player, team=team, match=match,
                                   started=request_dict['started'],
                                   minutes=request_dict['minutes'],
                                   subbed_due_to_injury=request_dict['subbed_due_to_injury'],
                                   yellow_card=request_dict['yellow_card'],
                                   red_card=request_dict['red_card'],
                                   corner=request_dict['corner'],
                                   )

        return dbModelInst


###########################################
###########################################
###########################################
###########################################





class GetUpdateDeleteTeam(Resource):
    def get(self, team_id):
        query = Team.query.get_or_404(team_id)
        return team_schema.dump(query).data

    def patch(self, team_id):
        team = Team.query.get_or_404(team_id)
        raw_dict = request.get_json(force=True)
        try:
            team_schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(team, key, value)

            team.update()
            return self.get(team_id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

    def delete(self, team_id):
        team = Team.query.get_or_404(team_id)
        try:
            delete = team.delete(team)
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class GetUpdateDeleteMatch(Resource):
    def get(self, match_id):
        query = Match.query.get_or_404(match_id)
        return match_schema.dump(query).data

    def patch(self, match_id):
        match = Match.query.get_or_404(match_id)
        raw_dict = request.get_json(force=True)
        try:
            match_schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(match, key, value)

            match.update()
            return self.get(match_id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class GetUpdateDeletePlayer(Resource):
    def get(self, player_id):
        query = Player.query.get_or_404(player_id)
        return player_schema.dump(query).data

    def patch(self, player_id):
        player = Player.query.get_or_404(player_id)
        raw_dict = request.get_json(force=True)
        try:
            player_schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            import pdb;pdb.set_trace()
            for key, value in request_dict.items():
                setattr(player, key, value)

            player.update()
            return self.get(player_id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class GetUpdateDeleteCampaign(Resource):
    def get(self, campaign_id):
        query = Campaign.query.get_or_404(campaign_id)
        return campaign_schema.dump(query).data

    def patch(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        raw_dict = request.get_json(force=True)
        try:
            campaign_schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(campaign, key, value)

            campaign.update()
            return self.get(campaign_id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class GetUpdateDeletePlayerMatch(Resource):
    def get(self, playermatch_id):
        query = PlayerMatch.query.get_or_404(playermatch_id)
        return playermatch_schema.dump(query).data

    def patch(self, playermatch_id):
        playermatch = PlayerMatch.query.get_or_404(playermatch_id)
        raw_dict = request.get_json(force=True)
        try:
            playermatch_schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(playermatch, key, value)

            playermatch.update()
            return self.get(playermatch_id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp











'''
class CreateListTeam(Resource):
    def get(self):
        query = Team.query.all()
        return team_schema.dump(query, many=True).data

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            team_schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            team = Team(request_dict['name'],)
            team.add(team)
            query = Team.query.get(team.id)
            results = team_schema.dump(query).data
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

class GetUpdateDeleteTeam(Resource):
    def get(self, id):
        query = Team.query.get_or_404(id)
        return team_schema.dump(query).data

    def patch(self, id):
        team = Team.query.get_or_404(id)
        raw_dict = request.get_json(force=True)
        try:
            team_schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(team, key, value)

            team.update()
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


class CreateListPlayer(Resource):
    def get(self):
        query = Player.query.all()
        return player_schema.dump(query, many=True).data

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            player_schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            player = Player(request_dict['name'],)
            player.add(player)
            query = Player.query.get(player.id)
            results = player_schema.dump(query).data
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


class GetUpdateDeletePlayer(Resource):
    def get(self, id):
        query = Player.query.get_or_404(id)
        return player_schema.dump(query).data

    def patch(self, id):
        player = Player.query.get_or_404(id)
        raw_dict = request.get_json(force=True)
        try:
            player_schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(player, key, value)

            player.update()
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

class CreateListPlayerMatch(Resource):
    def get(self):
        query = PlayerMatch.query.all()
        return playermatch_schema.dump(query, many=True).data

class CreateListMatch(Resource):
    def get(self):
        query = Match.query.all()
        return match_schema.dump(query, many=True).data

'''






