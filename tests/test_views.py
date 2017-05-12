#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest
import json
import requests

create_user = False


@pytest.mark.usefixtures("testapp")
class TestViews:
    def test_team(self, testapp):
        rv = testapp.get('/api/v1/teams/')
        assert rv.status_code == 200
        resp = json.loads(rv.data.decode('utf-8'))
        assert resp['data'] == []

        # now post a new team
        rv = testapp.post('/api/v1/teams/',
                          data='{"data":{"attributes":{"name":"Team T"},"type":"team"}}',
                          content_type='application/json')
        assert rv.status_code == 201

        # and get the teams
        rv = testapp.get('/api/v1/teams/')
        resp = json.loads(rv.data.decode('utf-8'))

        assert sorted(list(resp.keys())) == ['data', 'links']
        assert resp['links'] == {'self': '/api/v1/teams/'}
        assert len(resp['data']) == 1
        team1 = resp['data'][0]
        assert sorted(list(team1)) == ['attributes', 'id', 'links', 'type']

        assert team1['id'] == 1
        assert team1['links'] == {'self': '/api/v1/teams/1'}
        assert team1['type'] == "team"

        assert sorted(list(team1['attributes'])) == ['name']
        assert team1['attributes']['name'] == "Team T"


        # also by id (same result as above's team1
        rv = testapp.get('/api/v1/teams/1')
        resp = json.loads(rv.data.decode('utf-8'))

        team1 = resp['data']
        assert sorted(list(team1)) == ['attributes', 'id', 'links', 'type']

        assert team1['id'] == 1
        assert team1['links'] == {'self': '/api/v1/teams/1'}
        assert team1['type'] == "team"

        assert sorted(list(team1['attributes'])) == ['name']
        assert team1['attributes']['name'] == "Team T"

        # finally delete
        rv = testapp.delete('/api/v1/teams/1')

        rv = testapp.get('/api/v1/teams/')
        assert rv.status_code == 200
        resp = json.loads(rv.data.decode('utf-8'))
        assert resp['data'] == []
