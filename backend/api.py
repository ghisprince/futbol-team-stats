from .shared import api
from .views import *

"""
Module adding all the views/rest end point to urls

"""
api.add_resource(RefreshToken, '/api/refresh')
api.add_resource(UserLogin, '/api/login')
api.add_resource(UserLogout, '/api/logout')
api.add_resource(UserLogoutR, '/api/logoutr')

api.add_resource(CreateListTeam, '/api/teams')
api.add_resource(CreateListPlayer, '/api/players')
api.add_resource(CreateListMatch, '/api/matches')
api.add_resource(CreateListMatchStats, '/api/matchstats')
api.add_resource(CreateListPlayerMatch, '/api/playermatches')
api.add_resource(CreateListCompetition, '/api/competitions')
api.add_resource(CreateListSeason, '/api/seasons')
api.add_resource(CreateListOpponent, '/api/opponents')
api.add_resource(CreateListShot, '/api/shots')
api.add_resource(CreateListGoal, '/api/goals')
api.add_resource(CreateListAssist, '/api/assists')

api.add_resource(GetUpdateDeleteTeam, '/api/teams/<int:id>')
api.add_resource(GetUpdateDeletePlayer, '/api/players/<int:id>')
api.add_resource(GetUpdateDeleteMatch, '/api/matches/<int:id>')
api.add_resource(GetUpdateDeleteMatchStats, '/api/matchstats/<int:id>')
api.add_resource(GetUpdateDeletePlayerMatch, '/api/playermatches/<int:id>')
api.add_resource(GetUpdateDeleteCompetition, '/api/competitions/<int:id>')
api.add_resource(GetUpdateDeleteSeason, '/api/seasons/<int:id>')
api.add_resource(GetUpdateDeleteOpponent, '/api/opponents/<int:id>')
api.add_resource(GetUpdateDeleteShot, '/api/shots/<int:id>')
api.add_resource(GetUpdateDeleteGoal, '/api/goals/<int:id>')
api.add_resource(GetUpdateDeleteAssist, '/api/assists/<int:id>')

api.add_resource(GetPlayerSeasonData, '/api/playerseasondata/<int:id>')
api.add_resource(GetSeasonSeasonData, '/api/teamseasondata/<int:id>')


