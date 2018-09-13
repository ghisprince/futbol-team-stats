from .shared import api
from .views import *

"""
Module adding all the views/rest end point to urls 

"""

api.add_resource(CreateListTeam, '/api/v1/teams/')
api.add_resource(CreateListPlayer, '/api/v1/players/')
api.add_resource(CreateListMatch, '/api/v1/matches/')
api.add_resource(CreateListMatchStats, '/api/v1/matchstats/')
api.add_resource(CreateListPlayerMatch, '/api/v1/playermatches/')
api.add_resource(CreateListCompetition, '/api/v1/competitions/')
api.add_resource(CreateListOpponent, '/api/v1/opponents/')
api.add_resource(CreateListShot, '/api/v1/shots/')
api.add_resource(CreateListGoal, '/api/v1/goals/')
api.add_resource(CreateListAssist, '/api/v1/assists/')

api.add_resource(GetCurrentUserID, '/api/v1/currentuser')
api.add_resource(GetCurrentTeamID, '/api/v1/currentteam')
api.add_resource(GetUpdateDeleteTeam, '/api/v1/teams/<int:team_id>')
api.add_resource(GetUpdateDeletePlayer, '/api/v1/players/<int:player_id>')
api.add_resource(GetUpdateDeleteMatch, '/api/v1/matches/<int:match_id>')
api.add_resource(GetUpdateDeleteMatchStats, '/api/v1/matchstats/<int:matchstats_id>')
api.add_resource(GetUpdateDeletePlayerMatch, '/api/v1/playermatches/<int:playermatch_id>')
api.add_resource(GetUpdateDeleteCompetition, '/api/v1/competitions/<int:competition_id>')
api.add_resource(GetUpdateDeleteOpponent, '/api/v1/opponents/<int:opponent_id>')
api.add_resource(GetUpdateDeleteShot, '/api/v1/shots/<int:shot_id>')
api.add_resource(GetUpdateDeleteGoal, '/api/v1/goals/<int:goal_id>')
api.add_resource(GetUpdateDeleteAssist, '/api/v1/assists/<int:assist_id>')
