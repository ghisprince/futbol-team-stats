#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest
import json
import copy
import os

create_user = False

def get_result(req):
    code = req.status_code
    resp = json.loads(req.data.decode('utf-8'))
    return code, resp

match_data = {
   "data": {
      "attributes": {
         "away_team": {
            "data": {
               "attributes": {
                  "name": "B Team"
               },
               "type": "team"
            }
         },
         "campaign": {
            "data": {
               "attributes": {
                  "name": "Alphabet League"
               },
               "type": "campaign"
            }
         },
         "date_time": "2017-01-18T08:00:00",
         "home_team": {
            "data": {
               "attributes": {
                  "name": "A Team"
               },
               "type": "team"
            }
         }
      },
      "type": "match"
   },
   "links": {
      "self": "/api/v1/matches/1"
   }
}

player_data = {
    "data": {
        "attributes": {
            "name": "Ronaldinho",
            "number": 10,
            },
        "type": "player"
    }
}

team_data = {
    "data": {
        "attributes": {
            "name": "A Team"
        },
        "type": "team"
    }
}


@pytest.mark.usefixtures("testapp")
class TestViews:
    def test_team_getpost(self, testapp):
        code, resp = get_result(testapp.get('/api/v1/teams/'))
        assert code == 200
        assert resp['data'] == []

        # POST
        code, resp = get_result(testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team T"},"type":"team"}}',
                          content_type='application/json'))
        assert code == 201

        # GET
        code, resp = get_result(testapp.get('/api/v1/teams/'))

        # fully test the team data
        assert sorted(list(resp.keys())) == ['data', 'links']
        assert resp['links'] == {'self': '/api/v1/teams/'}
        assert len(resp['data']) == 1

        team1 = resp['data'][0]
        assert sorted(list(team1)) == ['attributes', 'id', 'links', 'type']
        assert team1['id'] == "1"
        assert team1['links'] == {'self': '/api/v1/teams/1'}
        assert team1['type'] == "team"
        assert sorted(list(team1['attributes'])) == ['name']
        assert team1['attributes']['name'] == "Team T"


    def test_team_getbylink(self, testapp):
        # POST
        code, resp = get_result(testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team V"},"type":"team"}}',
                          content_type='application/json'))
        assert code == 201

        # GET (by resource id)
        code, resp = get_result(testapp.get(resp['links']['self']))
        assert resp['data']['attributes']['name'] == "Team V"


    def test_team_query(self, testapp):
        # POST TEAMS
        rv = testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team X"},"type":"team"}}',
                          content_type='application/json')

        rv = testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team Y"},"type":"team"}}',
                          content_type='application/json')

        resp = json.loads(rv.data.decode('utf-8'))
        team_id = resp['data']['id']
        assert team_id == "2"

        rv = testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team Z"},"type":"team"}}',
                          content_type='application/json')

        # GET using query
        rv = testapp.get('/api/v1/teams/?name=Team%20Y')
        resp = json.loads(rv.data.decode('utf-8'))
        assert len(resp['data']) == 1
        assert resp['data'][0]['id'] == team_id


    def test_team_delete(self, testapp):

        code, resp = get_result(testapp.get('/api/v1/teams/'))

        assert code == 200
        assert resp['data'] == []

        # POST
        code, resp = get_result(testapp.post('/api/v1/teams/',
                                       data=json.dumps(team_data),
                                       content_type='application/json'))
        assert code == 201

        # DELETE
        testapp.delete('/api/v1/teams/1')

        code, resp = get_result(testapp.get('/api/v1/teams/'))
        assert code == 200
        assert resp['data'] == []


    def test_team_error(self, testapp):
        # now post a new team
        code, resp = get_result(testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team G"},"type":"team"}}',
                          content_type='application/json'))
        assert code == 201
        id = resp['data']['id']

        code, resp = get_result(testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team G"},"type":"team"}}',
                          content_type='application/json'))

        assert code == 403
        assert "UNIQUE constraint failed" in resp['error']


    def test_match(self, testapp):
        code, resp = get_result(testapp.post('/api/v1/teams/',
                          data=json.dumps(match_data['data']['attributes']['away_team']),
                          content_type='application/json'))
        assert code == 201
        away_team_id = resp['data']['id']

        code, resp = get_result(testapp.post('/api/v1/teams/',
                          data=json.dumps(match_data['data']['attributes']['home_team']),
                          content_type='application/json'))

        assert code == 201
        home_team_id = resp['data']['id']

        code, resp = get_result(testapp.post('/api/v1/campaigns/',
                                       data=json.dumps(match_data['data']['attributes']['campaign']),
                                       content_type='application/json'))
        assert code == 201
        campaign_id = resp['data']['id']

        match_data['data']['attributes']['away_team']['data']['id'] = away_team_id
        match_data['data']['attributes']['home_team']['data']['id'] = home_team_id
        match_data['data']['attributes']['campaign']['data']['id'] = campaign_id

        code, resp = get_result(testapp.post('/api/v1/matches/',
                          data=json.dumps(match_data),
                          content_type='application/json'))
        assert code == 201

        atts = resp['data']['attributes']
        assert atts['away_team']['data']['attributes']['name'] == "B Team"
        assert atts['home_team']['data']['attributes']['name'] == "A Team"
        assert atts['campaign']['data']['attributes']['name'] == "Alphabet League"
        assert atts['date_time'] == "2017-01-18T08:00:00+00:00"


    def test_campaign_post(self, testapp):
        # POST
        code, resp = get_result(testapp.post('/api/v1/campaigns/',
                          data='{"data":{"attributes":{"name":"S1"},"type":"campaign"}}',
                          content_type='application/json'))
        assert code == 201
        assert resp['data']['attributes']['name'] == "S1"

        # POST 2 more
        testapp.post('/api/v1/campaigns/',
                     data='{"data":{"attributes":{"name":"S2"},"type":"campaign"}}',
                     content_type='application/json')

        testapp.post('/api/v1/campaigns/',
                     data='{"data":{"attributes":{"name":"S3"},"type":"campaign"}}',
                     content_type='application/json')

        # GET all 3
        code, resp = get_result(testapp.get('/api/v1/campaigns/'))

        # fully test the team data
        assert sorted(list(resp.keys())) == ['data', 'links']
        assert resp['links'] == {'self': '/api/v1/campaigns/'}
        assert len(resp['data']) == 3

        assert sorted([i['attributes']['name'] for i in resp['data']]) == \
                                ["S1", "S2", "S3"]


    def test_campaign_delete(self, testapp):
        def get_campaigns_name(resp):
            return {i['attributes']['name']: i['links']['self']
                                for i in resp['data']}

        # POST
        content_type = 'application/json'
        data = {"data": {"attributes": {"name": None}, "type": "campaign"}}
        for i in ['A', 'B', 'C', 'D', 'E']:
            data['data']['attributes']['name'] = i
            testapp.post('/api/v1/campaigns/', data=json.dumps(data),
                         content_type=content_type)

        code, resp = get_result(testapp.get('/api/v1/campaigns/'))
        camps = get_campaigns_name(resp)
        assert sorted(camps.keys()) == ['A', 'B', 'C', 'D', 'E']

        # DELETE
        assert camps['B'] == '/api/v1/campaigns/2'
        testapp.delete(camps['B'])
        testapp.delete(camps['D'])

        code, resp = get_result(testapp.get('/api/v1/campaigns/'))
        camps = get_campaigns_name(resp)
        assert sorted(camps.keys()) == ['A', 'C', 'E']


    def test_campaign_query(self, testapp):
        # POST TEAMS
        testapp.post('/api/v1/campaigns/',
                     data='{"data":{"attributes":{"name":"2016 Season"},"type":"campaign"}}',
                     content_type='application/json')

        testapp.post('/api/v1/campaigns/',
                     data='{"data":{"attributes":{"name":"2017 Season"},"type":"campaign"}}',
                     content_type='application/json')

        testapp.post('/api/v1/campaigns/',
                     data='{"data":{"attributes":{"name":"State Cup 2016"},"type":"campaign"}}',
                     content_type='application/json')


        code, resp = get_result(testapp.get('/api/v1/campaigns/'))
        assert len(resp['data']) == 3

        code, resp = get_result(testapp.get(
                            '/api/v1/campaigns/?name=2017%20Season'))

        assert len(resp['data']) == 1
        assert resp['data'][0]['attributes']['name'] == "2017 Season"


    def test_player_post(self, testapp):
        def assertEqual(d, base_data):
            assert d['type'] == base_data["data"]["type"]
            assert d['attributes']['name'] == base_data["data"]['attributes']['name']
            assert d['attributes']['number'] == base_data["data"]['attributes']['number']
            assert d['attributes']['team']['data']['attributes']['name'] == "A Team"
            assert d['links']['self'] == "/api/v1/players/1"

        # post team
        code, resp = get_result(testapp.post('/api/v1/teams/',
                          data=json.dumps(team_data),
                          content_type='application/json'))

        player_data2 = copy.deepcopy(player_data)
        player_data2['data']['attributes']['team'] = resp

        # POST
        code, resp = get_result(testapp.post('/api/v1/players/',
                          data=json.dumps(player_data2),
                          content_type='application/json'))

        assert code == 201

        code, resp = get_result(testapp.get(resp['data']['links']['self']))
        assert code == 200
        assertEqual(resp['data'], player_data2)

        code, resp = get_result(testapp.get('/api/v1/players/'))
        assert code == 200
        assert len(resp["data"]) == 1
        assertEqual(resp["data"][0], player_data2)


    def test_player_patch(self, testapp):

        # this has partial attributes (number not name)
        player_data_patch = {
            "data": {
                "attributes": {
                    "number": 11
                },
                "type": "player"
            }
        }

        # POST
        code, resp = get_result(testapp.post('/api/v1/players/',
                          data=json.dumps(player_data),
                          content_type='application/json'))

        assert code == 201
        player_uri = resp['data']['links']['self']

        # PATCH
        code, resp = get_result(testapp.patch(player_uri,
                          data=json.dumps(player_data_patch),
                          content_type='application/json'))
        assert code == 200
        assert resp['data']['attributes']['name'] == 'Ronaldinho'
        assert resp['data']['attributes']['number'] == 11
        assert resp['data']['attributes']['team'] is None

        # DELETE
        code, resp = get_result(testapp.delete('/api/v1/players/1'))
        assert code == 405  # not supported


    def test_player_query(self, testapp):
        # POST players
        testapp.post('/api/v1/players/',
                     data='{"data":{"attributes":{"name":"Moe"},"type":"player"}}',
                     content_type='application/json')

        testapp.post('/api/v1/players/',
                     data='{"data":{"attributes":{"name":"Larry"},"type":"player"}}',
                     content_type='application/json')

        testapp.post('/api/v1/players/',
                     data='{"data":{"attributes":{"name":"Curly"},"type":"player"}}',
                     content_type='application/json')

        code, resp = get_result(testapp.get('/api/v1/players/'))
        assert len(resp['data']) == 3

        code, resp = get_result(testapp.get(
                            '/api/v1/players/?name=Curly'))

        assert len(resp['data']) == 1
        assert resp['data'][0]['attributes']['name'] == "Curly"


    def test_playermatch_post(self, testapp):
        pass
    
    def test_playermatch_patch(self, testapp):
        pass

    def test_playermatch_delete(self, testapp):
        pass

    def test_shot(self, testapp):
        pass

    def test_goal(self, testapp):
        pass

    def test_assist(self, testapp):
        pass

    def test_shotagainst(self, testapp):
        pass
