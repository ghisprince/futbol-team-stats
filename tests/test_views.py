#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest
import json
import requests
import os

create_user = False

data_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json"))


match_test_data = {
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



@pytest.mark.usefixtures("testapp")
class TestViews:
    def test_team_getpost(self, testapp):
        rv = testapp.get('/api/v1/teams/')
        assert rv.status_code == 200
        resp = json.loads(rv.data.decode('utf-8'))
        assert resp['data'] == []

        # POST
        rv = testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team T"},"type":"team"}}',
                          content_type='application/json')
        assert rv.status_code == 201
        resp = json.loads(rv.data.decode('utf-8'))

        # GET
        rv = testapp.get('/api/v1/teams/')
        resp = json.loads(rv.data.decode('utf-8'))

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
        rv = testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team V"},"type":"team"}}',
                          content_type='application/json')
        assert rv.status_code == 201
        resp = json.loads(rv.data.decode('utf-8'))

        # GET (by resource id)
        rv = testapp.get(resp['links']['self'])
        resp = json.loads(rv.data.decode('utf-8'))
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
        rv = testapp.get('/api/v1/teams/')
        assert rv.status_code == 200
        resp = json.loads(rv.data.decode('utf-8'))
        assert resp['data'] == []

        # POST
        rv = testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team V"},"type":"team"}}',
                          content_type='application/json')
        assert rv.status_code == 201

        # DELETE
        rv = testapp.delete('/api/v1/teams/1')

        rv = testapp.get('/api/v1/teams/')
        assert rv.status_code == 200
        resp = json.loads(rv.data.decode('utf-8'))
        assert resp['data'] == []


    def test_team_error(self, testapp):
        # now post a new team
        rv = testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team G"},"type":"team"}}',
                          content_type='application/json')
        assert rv.status_code == 201
        resp = json.loads(rv.data.decode('utf-8'))
        id = resp['data']['id']

        rv = testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team G"},"type":"team"}}',
                          content_type='application/json')
        assert rv.status_code == 403
        resp = json.loads(rv.data.decode('utf-8'))
        assert "UNIQUE constraint failed" in resp['error']


    def test_match(self, testapp):
        # now post a new team

        rv = testapp.post('/api/v1/teams/',
                          data=json.dumps(match_test_data['data']['attributes']['away_team']),
                          content_type='application/json')
        assert rv.status_code == 201
        resp = json.loads(rv.data.decode('utf-8'))
        away_team_id = resp['data']['id']

        rv = testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Z Team"},"type":"team"}}',
                          content_type='application/json')
        assert rv.status_code == 201

        rv = testapp.post('/api/v1/teams/',
                          data=json.dumps(match_test_data['data']['attributes']['home_team']),
                          content_type='application/json')
        assert rv.status_code == 201
        resp = json.loads(rv.data.decode('utf-8'))
        home_team_id = resp['data']['id']

        rv = testapp.post('/api/v1/campaigns/',
                          data=json.dumps(match_test_data['data']['attributes']['campaign']),
                          content_type='application/json')
        assert rv.status_code == 201
        resp = json.loads(rv.data.decode('utf-8'))
        campaign_id = resp['data']['id']

        match_test_data['data']['attributes']['away_team']['data']['id'] = away_team_id
        match_test_data['data']['attributes']['home_team']['data']['id'] = home_team_id
        match_test_data['data']['attributes']['campaign']['data']['id'] = campaign_id

        rv = testapp.post('/api/v1/matches/',
                          data=json.dumps(match_test_data),
                          content_type='application/json')
        assert rv.status_code == 201

        resp = json.loads(rv.data.decode('utf-8'))
        atts = resp['data']['attributes']
        assert atts['away_team']['data']['attributes']['name'] == "B Team"
        assert atts['home_team']['data']['attributes']['name'] == "A Team"
        assert atts['campaign']['data']['attributes']['name'] == "Alphabet League"
        assert atts['date_time'] == "2017-01-18T08:00:00+00:00"
