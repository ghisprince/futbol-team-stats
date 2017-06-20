#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest
from app.models import *
import pdb

create_user = False


@pytest.mark.usefixtures("testapp")
class TestModels:

    def test_user_save(self, testapp):
        """ Test Saving the user model to the database """

        admin = User('admin', 'supersafepassword')
        db.session.add(admin)
        db.session.commit()

        user = User.query.filter_by(username="admin").first()
        assert user is not None

    def test_user_password(self, testapp):
        """ Test password hashing and checking """

        admin = User('admin', 'supersafepassword')

        assert admin.username == 'admin'
        assert admin.check_password('supersafepassword')

    def test_team(self, testapp):
        team = Team("Shark Tornado")
        assert team.name == "Shark Tornado"
        assert team.id is None

        db.session.add(team)
        db.session.commit()
        assert team.id is not None

    def test_get_or_create(self, testapp):
        assert Team.query.filter_by(name="Cabras").first() is None

        # make sure get or create works
        team = get_or_create(db.session, Team, name="Cabras")
        team2 = get_or_create(db.session, Team, name="Cabras")
        assert team2.id == team.id

    def test_player(self, testapp):
        player = Player("Lil' Messi", 10)
        assert player.number == 10
        assert player.name == "Lil' Messi"
        assert player.team is None

        team = Team("Barca")
        player.team == team

        player = Player("Lil' Ronaldhino", 11, team)
        assert player.team.name == "Barca"

    def test_campaign(self, testapp):
        camp = Campaign("Spring 2017")
        assert camp.name == "Spring 2017"

        camp.result = "2nd place"
        assert camp.result == "2nd place"

    def test_match(self, testapp):
        match = Match("2017-01-02T08:00:00",
                      Team("Lil' Barca"),
                      Opponent("Lil' Real Madrid"),)
        assert match.team.name == "Lil' Barca"
        assert match.opponent.name == "Lil' Real Madrid"
        assert match.campaign is None

    def test_match_campaign(self, testapp):
        match = Match("2017-11-12T08:00:00",
                      Team("Lil' Barca"),
                      Opponent("Lil' Real Madrid"),
                      Campaign("Fall 2017"))

        assert match.campaign.name == "Fall 2017"

    def test_complete(self, testapp):

        team = Team("Lil' Barca")
        opponent = Opponent("Lil' Real Madrid")
        match = Match("2017-11-12T08:00:00",
                      team,
                      opponent,
                      Campaign("Fall 2017"))

        player_match1 = PlayerMatch(Player("Lil' Messi", 10),
                                    match,
                                    True, 60, True, 1, 0, 1)

        player_match2 = PlayerMatch(Player("Lil' Ronaldo", 7),
                                    match,
                                    False, 60, False, 0, 1, 2)

        player_match3 = PlayerMatch(Player("Lil' Rakitic", 4),
                                    match,
                                    False, 60, False,)

        shot1 = Shot(player_match1, 30, 30, on_goal=True)
        shot2 = Shot(player_match2, 40, 10, on_goal=False)
        shot3 = Shot(player_match2, 10, 10, on_goal=True)

        goal1 = Goal(shot1)
        assist = Assist(player_match3, goal1)
        goal2 = Goal(shot3)

        # test
        assert player_match1.match.team.name == "Lil' Barca"
        assert player_match1.match.opponent.name == "Lil' Real Madrid"
        assert player_match1.starter
        assert player_match1.subbed_due_to_injury
        assert player_match1.yellow_card == 1

        assert not player_match2.starter
        assert not player_match2.subbed_due_to_injury
        assert player_match2.red_card == 1

        assert len(match.player_matches) == 3
        assert sorted([i.player.number for i in match.player_matches]) == [4, 7, 10]

        # persist everything
        db.session.add(team)
        db.session.add(opponent)
        db.session.add(match)
        db.session.add(player_match1)
        db.session.add(player_match2)
        db.session.add(player_match3)
        db.session.add(goal1)
        db.session.add(shot1)
        db.session.add(shot2)
        db.session.add(shot3)
        db.session.add(assist)

        db.session.commit()

        # now try some deletes
        assert(len(Goal.query.all()) == 2)
        assert(len(Assist.query.all()) == 1)
        assert(len(Shot.query.all()) == 3)

        # delete teh shot that scored, and has an assist
        shot = Shot.query.first()
        shot.delete(shot)

        assert(len(Goal.query.all()) == 1)
        assert(len(Assist.query.all()) == 0)
        assert(len(Shot.query.all()) == 2)

        # delete playermatch should delete all dependent objects
        match.delete(match)
        assert(len(PlayerMatch.query.all()) == 0)
        assert(len(Goal.query.all()) == 0)
        assert(len(Assist.query.all()) == 0)
        assert(len(Shot.query.all()) == 0)


    def test_goal(self, testapp):
        team = Team("Lil' Barca")
        opponent = Opponent("Lil' Real Madrid")
        match = Match("2017-11-12T08:00:00",
                      team,
                      opponent,
                      Campaign("Fall 2017"))

        player_match1 = PlayerMatch(Player("Lil' Messi", 10),
                                    match, True, 60, True, 1, 0, 1)

        player_match2 = PlayerMatch(Player("Lil' Ronaldo", 7),
                                    match, False, 60, False, 0, 1, 2)

        assert player_match1.starter
        assert player_match1.subbed_due_to_injury
        assert player_match1.yellow_card == 1

        assert not player_match2.starter
        assert not player_match2.subbed_due_to_injury
        assert player_match2.red_card == 1

        assert len(match.player_matches) == 2
        assert sorted([i.player.number for i in match.player_matches]) == [7, 10]

    def test_assist(self, testapp):
        team = Team("A Team")
        opponent = Opponent("B Team")
        match = Match("2017-11-12T08:00:00",
                      team,
                      opponent,)

        player_match1 = PlayerMatch(Player("Player A", 10),
                                    match, True, 60, True, 1, 0, 1)

        player_match2 = PlayerMatch(Player("Player B", 7),
                                    match, False, 60, False, 0, 1, 2)

        shot = Shot(player_match1, 1, 1, True, False)
        goal = Goal(shot, 89)
        assist = Assist(player_match2, goal)
        assert assist.goal.shot.player_match.player.name == "Player A"
        assert assist.player_match.player.name == "Player B"
