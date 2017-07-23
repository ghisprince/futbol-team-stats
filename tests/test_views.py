#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest
import json
import copy
import os
from pprint import pprint
import pdb

create_user = False


def get_result(req):
    code = req.status_code
    resp = {}
    if code != 204:
        resp = json.loads(req.data.decode('utf-8'))
    return code, resp


team_data = {"name": "A Team"}


@pytest.mark.usefixtures("testapp")
class TestViews:
    def _load_generic_match(self, testapp):
        match_data = {
            "opponent": {"name": "B Team"},
            "competition": None,
            "date_time": "2017-03-18T08:00:00",
            "team": {"name": "A Team"},
            "at_home": False,
        }

        code, resp = get_result(testapp.post('/api/v1/teams/',
                                             data=json.dumps(
                                                 match_data['team']),
                                             content_type='application/json'))
        team_id = resp['id']

        code, resp = get_result(testapp.post('/api/v1/opponents/',
                                             data=json.dumps(
                                                 match_data['opponent']),
                                             content_type='application/json'))
        opponent_id = resp['id']

        match_data['team']['id'] = team_id
        match_data['opponent']['id'] = opponent_id
        _, resp = get_result(testapp.post('/api/v1/matches/',
                                             data=json.dumps(match_data),
                                             content_type='application/json'))

        _, resp = get_result(testapp.get(resp['_links']['self'] + "?expand=true",
                                          content_type='application/json'))

        return resp

    def _load_generic_playermatch(self, testapp):
        match = self._load_generic_match(testapp)
        team = match['team']
        _, player = get_result(testapp.post('/api/v1/players/',
                                            data=json.dumps(
                                                {"name": "G", "number": 11}),
                                            content_type='application/json'))

        playerMatch = {"player": player,
                       "match": match,
                       "starter": True,
                       "minutes": 90,
                       "subbed_due_to_injury": False,
                       "yellow_card": 1,
                       "red_card": 1,
                       "corners": 3}

        code, resp = get_result(testapp.post('/api/v1/playermatches/',
                                             data=json.dumps(playerMatch),
                                             content_type='application/json'))
        # expand=true
        code, resp = get_result(testapp.get(resp['_links']['self'] + "?expand=true",
                                             content_type='application/json'))


        return resp


    def test_team_post(self, testapp):
        code, resp = get_result(testapp.get('/api/v1/teams/'))
        assert code == 200
        assert resp == []

        # POST
        code, resp = get_result(testapp.post('/api/v1/teams/',
                                             data='{"name":"Team T"}',
                                             content_type='application/json'))
        assert code == 201

        # GET
        code, resp = get_result(testapp.get('/api/v1/teams/'))

        # fully test the team data
        assert len(resp) == 1

        team1 = resp[0]
        assert sorted(list(team1)) == sorted(['_links', 'id', 'matches', 'name',
                                              'players', 'teams'])
        assert team1['id'] == 1
        assert team1['name'] == "Team T"
        assert sorted(list(team1['_links'])) == ['collection', 'self']
                                                #'matches', 'players', ]
        assert team1['_links']['self'] == '/api/v1/teams/1'
        #assert team1['_links']['players'] == '/api/v1/teams/1/players/'


    def test_team_getbylink(self, testapp):
        # POST
        code, resp = get_result(testapp.post('/api/v1/teams/',
                                             data='{"name":"Team V"}',
                                             content_type='application/json'))
        assert code == 201

        # GET (by resource id)
        code, resp = get_result(testapp.get(resp['_links']['self']))
        assert resp['name'] == "Team V"

    def test_team_query(self, testapp):
        # POST TEAMS
        rv = testapp.post('/api/v1/teams/',
                          data='{"name":"Team X"}',
                          content_type='application/json')

        rv = testapp.post('/api/v1/teams/',
                          data='{"name":"Team Y"}',
                          content_type='application/json')

        resp = json.loads(rv.data.decode('utf-8'))
        team_id = resp['id']
        assert team_id == 2

        rv = testapp.post('/api/v1/teams/',
                          data='{"name":"Team Z"}',
                          content_type='application/json')

        # GET using query
        rv = testapp.get('/api/v1/teams/?name=Team%20Y')
        resp = json.loads(rv.data.decode('utf-8'))
        assert len(resp) == 1
        assert resp[0]['id'] == team_id

    def test_team_delete(self, testapp):
        code, resp = get_result(testapp.get('/api/v1/teams/'))

        assert code == 200
        assert resp == []

        # POST
        code, resp = get_result(testapp.post('/api/v1/teams/',
                                             data=json.dumps(team_data),
                                             content_type='application/json'))
        assert code == 201

        # DELETE
        code, resp = get_result(testapp.delete('/api/v1/teams/1'))
        assert code == 403

        code, resp = get_result(testapp.get('/api/v1/teams/'))
        assert code == 200
        assert len(resp) == 1

    def test_team_error(self, testapp):
        # now post a new team
        code, resp = get_result(testapp.post('/api/v1/teams/',
                                             data='{"name":"Team G"}',
                                             content_type='application/json'))
        assert code == 201
        id = resp['id']

        code, resp = get_result(testapp.post('/api/v1/teams/',
                                             data='{"name":"Team G"}',
                                             content_type='application/json'))

        # removed the unique constraint in the database since diff Users could
        #  have the same team name
        return
        assert code == 403
        assert "UNIQUE constraint failed" in resp['error']


    def test_match(self, testapp):
        match_data = {
            "opponent": {"name": "B Team"},
            "competition": {"name": "Alphabet League"},
            "date_time": "2017-01-18T08:00:00",
            "team": {"name": "A Team"},
            "at_home": True,
        }

        code, resp = get_result(testapp.post('/api/v1/opponents/',
                                             data=json.dumps(
                                                 match_data['opponent']),
                                             content_type='application/json'))
        assert code == 201
        opponent_id = resp['id']

        code, resp = get_result(testapp.post('/api/v1/teams/',
                                             data=json.dumps(
                                                 match_data['team']),
                                             content_type='application/json'))

        assert code == 201
        team_id = resp['id']

        code, resp = get_result(testapp.post('/api/v1/competitions/',
                                             data=json.dumps(
                                                 match_data['competition']),
                                             content_type='application/json'))
        assert code == 201
        competition_id = resp['id']

        match_data['team']['id'] = team_id
        match_data['opponent']['id'] = opponent_id
        match_data['competition']['id'] = competition_id

        code, resp = get_result(testapp.post('/api/v1/matches/',
                                             data=json.dumps(match_data),
                                             content_type='application/json'))

        assert code == 201
        code, resp = get_result(testapp.get(resp["_links"]["self"] + "?expand=true",
                                            content_type='application/json'))

        assert resp['opponent']['name'] == match_data['opponent']['name']
        assert resp['competition']['name'] == match_data['competition']['name']
        assert resp['date_time'] == "2017-01-18T08:00:00+00:00"
        assert resp['at_home'] == match_data['at_home']

        # Lastly create a match with null competition (aka scrimmage, friendly)
        match_data['competition'] = None
        match_data["date_time"] = "2019-09-09T09:00:00"

        code, resp = get_result(testapp.post('/api/v1/matches/',
                                             data=json.dumps(match_data),
                                             content_type='application/json'))
        assert code == 201

        # then test
        assert resp['competition'] is None
        assert resp['date_time'] == "2019-09-09T09:00:00+00:00"

    def test_competition_post(self, testapp):
        # POST
        code, resp = get_result(testapp.post('/api/v1/competitions/',
                                             data='{"name":"S1"}',
                                             content_type='application/json'))
        assert code == 201
        assert resp['name'] == "S1"

        # POST 2 more
        testapp.post('/api/v1/competitions/',
                     data='{"name":"S2"}',
                     content_type='application/json')

        testapp.post('/api/v1/competitions/',
                     data='{"name":"S3"}',
                     content_type='application/json')

        # GET all 3
        code, resp = get_result(testapp.get('/api/v1/competitions/'))

        # fully test the team data
        assert len(resp) == 3
        assert sorted([i['name'] for i in resp]) == \
               ["S1", "S2", "S3"]

    def test_competition_delete(self, testapp):
        def get_competitions_name(resp):
            return {i['name']: i['_links']['self']
                    for i in resp}

        # POST
        content_type = 'application/json'
        data = {"name": None}
        for i in ['A', 'B', 'C', 'D', 'E']:
            data['name'] = i
            testapp.post('/api/v1/competitions/', data=json.dumps(data),
                         content_type=content_type)

        code, resp = get_result(testapp.get('/api/v1/competitions/'))
        camps = get_competitions_name(resp)
        assert sorted(camps.keys()) == ['A', 'B', 'C', 'D', 'E']

        # DELETE
        assert camps['B'] == '/api/v1/competitions/2'
        testapp.delete(camps['B'])
        testapp.delete(camps['D'])

        code, resp = get_result(testapp.get('/api/v1/competitions/'))
        camps = get_competitions_name(resp)
        assert sorted(camps.keys()) == ['A', 'C', 'E']

    def test_competition_query(self, testapp):
        # POST TEAMS
        testapp.post('/api/v1/competitions/',
                     data='{"name":"2016 Season"}',
                     content_type='application/json')

        testapp.post('/api/v1/competitions/',
                     data='{"name":"2017 Season"}',
                     content_type='application/json')

        testapp.post('/api/v1/competitions/',
                     data='{"name":"State Cup 2016"}',
                     content_type='application/json')

        code, resp = get_result(testapp.get('/api/v1/competitions/'))
        assert len(resp) == 3

        code, resp = get_result(testapp.get(
            '/api/v1/competitions/?name=2017%20Season'))

        assert len(resp) == 1
        assert resp[0]['name'] == "2017 Season"

    def test_player_post_delete(self, testapp):
        def assertEqual(d, base_data):
            assert d['name'] == base_data['name']
            assert d['number'] == base_data['number']
            assert d['_links']['self'] == "/api/v1/players/1"

        player_data = {"name": "Ronaldinho", "number": 10, }

        # post team
        code, resp = get_result(testapp.post('/api/v1/teams/',
                                             data=json.dumps(team_data),
                                             content_type='application/json'))

        player_data['team'] = resp['id']

        # POST
        code, resp = get_result(testapp.post('/api/v1/players/',
                                             data=json.dumps(player_data),
                                             content_type='application/json'))
        assert code == 201

        code, resp = get_result(testapp.get(resp['_links']['self']))
        assert code == 200
        assertEqual(resp, player_data)

        code, resp = get_result(testapp.get('/api/v1/players/'))
        assert code == 200
        assert len(resp) == 1
        assertEqual(resp[0], player_data)

        # POST ANOTHER
        player_data = {"name": "Pele", "number": 10}
        code, resp = get_result(testapp.post('/api/v1/players/',
                                             data=json.dumps(player_data),
                                             content_type='application/json'))
        assert code == 201

        # DELETE
        code, resp = get_result(testapp.delete('/api/v1/players/1'))
        assert code == 403

        code, resp = get_result(testapp.get('/api/v1/players/'))
        assert len(resp) == 2

    def test_player_patch(self, testapp):
        # this has partial attributes (number not name)
        player_data_patch = {"number": 9}

        # POST
        code, resp = get_result(testapp.post('/api/v1/players/',
                                             data=json.dumps({"name": "Suarez",
                                                              "number": 99,
                                                              "team": None}),
                                             content_type='application/json'))

        assert code == 201
        player_uri = resp['_links']['self']

        # PATCH
        code, resp = get_result(testapp.patch(player_uri,
                                              data=json.dumps(
                                                  player_data_patch),
                                              content_type='application/json'))

        assert code == 200
        assert resp['name'] == 'Suarez'
        assert resp['number'] == 9
        assert resp['team'] is None

    def test_player_query(self, testapp):
        # POST players
        testapp.post('/api/v1/players/',
                     data='{"name":"Moe"}',
                     content_type='application/json')

        testapp.post('/api/v1/players/',
                     data='{"name":"Larry"}',
                     content_type='application/json')

        testapp.post('/api/v1/players/',
                     data='{"name":"Curly"}',
                     content_type='application/json')

        code, resp = get_result(testapp.get('/api/v1/players/'))
        assert len(resp) == 3

        code, resp = get_result(testapp.get(
            '/api/v1/players/?name=Curly'))

        assert len(resp) == 1
        assert resp[0]['name'] == "Curly"

    def test_playermatch_post_patch_delete(self, testapp):
        match = self._load_generic_match(testapp)

        _, team = get_result(testapp.get('/api/v1/teams/1', ))

        _, player_1 = get_result(testapp.post('/api/v1/players/',
                                              data='{"name":"Pele"}',
                                              content_type='application/json'))

        player_match_1 = {
            'player': player_1,
            'match': match,
            'starter': True,
            'minutes': 50,
            'subbed_due_to_injury': False,
            'yellow_card': 1,
            'red_card': 0,
            'corners': 5,
        }

        code, pmatch = get_result(testapp.post('/api/v1/playermatches/',
                                               data=json.dumps(player_match_1),
                                               content_type='application/json'))
        assert code == 201
        assert pmatch['shots'] == []
        assert pmatch['assists'] == []
        # assert pmatch['goals'] == []
        assert pmatch['corners'] == player_match_1['corners']
        assert pmatch['minutes'] == player_match_1['minutes']
        assert pmatch['red_card'] == player_match_1['red_card']
        assert pmatch['yellow_card'] == player_match_1['yellow_card']
        assert pmatch['starter'] is player_match_1['starter']
        assert pmatch['subbed_due_to_injury'] is \
               player_match_1['subbed_due_to_injury']


        # call again with expand to get expanded match & player objects
        _, pmatch = get_result(testapp.get(pmatch['_links']['self'] + "?expand=true",
                                           content_type='application/json'))


        assert pmatch['match']['id'] == match['id']
        assert pmatch['player']['name'] == player_1['name']
        assert pmatch['match']['id'] == match['id']

        # POST again, but with diff values
        _, player_2 = get_result(testapp.post('/api/v1/players/',
                                              data='{"name":"Cruyff"}',
                                              content_type='application/json'))

        player_match_2 = {
            'player': player_2,
            'match': match,
            'starter': False,
            'minutes': 89,
            'subbed_due_to_injury': True,
            'yellow_card': 0,
            'red_card': 1,
            'corners': 2,
        }

        code, pmatch = get_result(testapp.post('/api/v1/playermatches/',
                                               data=json.dumps(player_match_2),
                                               content_type='application/json'))
        assert code == 201
        assert pmatch['shots'] == []
        assert pmatch['assists'] == []
        # assert pmatch['goals'] == []
        assert pmatch['corners'] == player_match_2['corners']
        assert pmatch['minutes'] == player_match_2['minutes']
        assert pmatch['red_card'] == player_match_2['red_card']
        assert pmatch['yellow_card'] == player_match_2['yellow_card']
        assert pmatch['starter'] is player_match_2['starter']
        assert pmatch['subbed_due_to_injury'] is \
               player_match_2['subbed_due_to_injury']

        # call again with expand to get expanded match & player objects
        _, pmatch = get_result(testapp.get(pmatch['_links']['self'] + "?expand=true",
                                           content_type='application/json'))

        assert pmatch['match']['id'] == match['id']
        assert pmatch['player']['name'] == player_2['name']
        assert pmatch['match']['id'] == match['id']

        # quick test of patch
        player_match_patch = {'minutes': 55}
        code, pmatch = get_result(testapp.patch('/api/v1/playermatches/2',
                                                data=json.dumps(
                                                    player_match_patch),
                                                content_type='application/json'))

        assert code == 200

        # call again with expand to get expanded match & player objects
        _, pmatch = get_result(testapp.get(pmatch['_links']['self'] + "?expand=true",
                                           content_type='application/json'))

        assert pmatch['player']['name'] == player_2['name']
        assert pmatch['minutes'] == 55

        _, resp = get_result(testapp.get('/api/v1/playermatches/'))
        assert len(resp) == 2
        code, resp = get_result(testapp.delete(pmatch['_links']['self']))
        assert code == 204
        assert resp == {}

        _, resp = get_result(testapp.get('/api/v1/playermatches/'))
        assert len(resp) == 1

    def test_shot(self, testapp):
        def asserShottEqual(source, result):
            # test shot 1
            assert source['x'] == result['x']
            assert source['y'] == result['y']
            assert source['on_goal'] == result['on_goal']
            assert source['scored'] == result['scored']
            assert source['pk'] == result['pk']
            #assert source['player_match']['id'] == result['player_match']['id']
            assert source['by_opponent'] is result['by_opponent']

        pm = self._load_generic_playermatch(testapp)
        shot_data = {"player_match": pm, "x": 1, "y": 10, "on_goal": True,
                     "scored": False, "pk": False, "by_opponent": False}

        code, shot = get_result(testapp.post('/api/v1/shots/',
                                             data=json.dumps(shot_data),
                                             content_type='application/json'))


        asserShottEqual(shot_data, shot)

        # POST another
        shot_data = {"player_match": pm, "x": 20, "y": 2, "on_goal": False,
                     "scored": True, "pk": True, "by_opponent": False}

        code, shot = get_result(testapp.post('/api/v1/shots/',
                                             data=json.dumps(shot_data),
                                             content_type='application/json'))

        asserShottEqual(shot_data, shot)

        # test the playerMatch relationship

        _, pm = get_result(testapp.get(pm['_links']['self']))
        assert len(pm['shots']) == 2

    def test_goal_assist(self, testapp):
        # get a playerMatch
        pm = self._load_generic_playermatch(testapp)

        # create a second
        _, player = get_result(testapp.post('/api/v1/players/',
                                            data=json.dumps({"name": "P",
                                                             "number": 12}),
                                            content_type='application/json'))

        playerMatch_data = {"player": player,
                            "match": pm['match'],
                            "starter": True,
                            "minutes": 90,
                            "subbed_due_to_injury": False,
                            "yellow_card": 0,
                            "red_card": 0,
                            "corners": 0}

        code, pm2 = get_result(testapp.post('/api/v1/playermatches/',
                                            data=json.dumps(playerMatch_data),
                                            content_type='application/json'))
        assert code == 201

        shot_data = {"player_match": pm, "x": 1, "y": 10,
                     "on_goal": True, "scored": True, "pk": False,
                     "by_opponent": False}

        code, shot = get_result(testapp.post('/api/v1/shots/',
                                             data=json.dumps(shot_data),
                                             content_type='application/json'))
        assert code == 201

        goal_data = {'shot': shot, 'time': 91}
        code, goal = get_result(testapp.post('/api/v1/goals/',
                                             data=json.dumps(goal_data),
                                             content_type='application/json'))
        assert code == 201

        assist_data = {"player_match": pm2, 'goal': goal}
        code, goal = get_result(testapp.post('/api/v1/assists/',
                                             data=json.dumps(assist_data),
                                             content_type='application/json'))

        # now a bit of testing
        _, assists = get_result(testapp.get('/api/v1/assists/'))
        _, goals = get_result(testapp.get('/api/v1/goals/'))
        assert len(assists) == 1
        assert len(goals) == 1
        assert goals[0]['assist'] == assists[0]['id']

    def test_shotagainst(self, testapp):
        def assertShotAgainstEqual(base, result):
            assert base['x'] == result['x']
            assert base['y'] == result['y']
            assert base['on_goal'] is result['on_goal']
            assert base['scored'] is result['scored']
            assert base['pk'] is result['pk']
            #assert base['player_match']['id'] == result['player_match']['id']
            assert base['by_opponent'] is result['by_opponent']

        pm = self._load_generic_playermatch(testapp)
        shotagainst_data_1 = {"player_match": pm, "x": 1, "y": 10,
                              "on_goal": True, "pk": False,
                              "by_opponent": True, "scored": False}

        code, shotagainst_1 = get_result(testapp.post('/api/v1/shots/',
                                                      data=json.dumps(
                                                          shotagainst_data_1),
                                                      content_type='application/json'))
        assert code == 201
        assertShotAgainstEqual(shotagainst_data_1, shotagainst_1)

        # POST another
        shotagainst_data_2 = {"player_match": pm, "x": 3, "y": 4,
                              "on_goal": False, "scored": False, "pk": True,
                              "by_opponent": True}

        code, shotagainst_2 = get_result(testapp.post('/api/v1/shots/',
                                                      data=json.dumps(
                                                          shotagainst_data_2),
                                                      content_type='application/json'))
        assert code == 201
        assertShotAgainstEqual(shotagainst_data_2, shotagainst_2)
