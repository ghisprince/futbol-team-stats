from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


import datetime
db = SQLAlchemy()


class CRUD_MixIn():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

# many to many relationship between User and Team
association = db.Table('association',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('team_id', db.Integer, db.ForeignKey('team.id')))


class User(db.Model, CRUD_MixIn, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    team = db.relationship('Team', secondary=association,
                           backref=db.backref('teams', lazy='dynamic'))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {}>'.format(self.username)

# objects
class Team(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

    home_matches = db.relationship('Match', foreign_keys='Match.home_team_id', backref='home_team', lazy='dynamic')
    away_matches = db.relationship('Match', foreign_keys='Match.away_team_id', backref='away_team', lazy='dynamic')
    player_matches = db.relationship("PlayerMatch", back_populates="team")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "Team (name={})".format(self.name)

    @property
    def matches(self):
        return self.home_matches.union(self.away_matches)




class Campaign(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    matches = db.relationship("Match", back_populates="campaign")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "Campaign (name={})".format(self.name)




class Match(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    date_time = db.Column(db.DateTime(), nullable=False, unique=True)

    # relationships
    player_matches = db.relationship("PlayerMatch", back_populates="match")

    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    #home_team = db.relationship("Team", back_populates="home_matches")

    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    #away_team = db.relationship("Team", back_populates="away_matches")

    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    campaign = db.relationship("Campaign", back_populates="matches")

    def __init__(self, date_time, home_team, away_team, campaign=None):
        self.date_time = datetime.datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        self.home_team = home_team
        self.away_team = away_team
        self.campaign = campaign

    def __repr__(self):
        return "Match (home_team={}, away_team={}, date_time={})".format(self.home_team,
                                                                         self.away_team,
                                                                         self.date_time)


class Player(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    number = db.Column(db.Integer(), nullable=True)

    # relationships
    player_matches = db.relationship("PlayerMatch", back_populates="player")

    def __init__(self, name, number=None):
        self.name = name
        self.number = number

    def __repr__(self):
        return "Player (number={}, name={})".format(self.number, self.name)




class PlayerMatch(db.Model, CRUD_MixIn):
    __table_args__ = (db.UniqueConstraint('player_id', 'match_id'),)

    id = db.Column(db.Integer(), primary_key=True)
    started = db.Column(db.Boolean(), default=False, nullable=False)
    minutes = db.Column(db.Integer(), default=0, nullable=False)
    subbed_due_to_injury = db.Column(db.Boolean(), default=False)
    yellow_card = db.Column(db.Integer(), default=0)
    red_card = db.Column(db.Integer(), default=0)
    corner = db.Column(db.Integer(), default=0)

    # relationships
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship("Player", back_populates="player_matches")

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team = db.relationship("Team", back_populates="player_matches")

    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    match = db.relationship("Match", back_populates="player_matches")

    shots = db.relationship("Shot", back_populates="player_match")
    goals = db.relationship("Goal", back_populates="player_match")
    assists = db.relationship("Assist", back_populates="player_match")
    shots_against = db.relationship("ShotAgainst", back_populates="player_match")

    def __init__(self, player, team, match, started=True, minutes=0,
                 subbed_due_to_injury=None,
                 yellow_card=None, red_card=None, corner=None,):
        self.player = player
        self.team = team
        self.match = match
        self.started = started
        self.minutes = minutes
        self.subbed_due_to_injury = subbed_due_to_injury
        self.yellow_card = yellow_card
        self.red_card = red_card
        self.corner = corner

    def __repr__(self):
        return "PlayerMatch (player={}, started={}, minutes={})".format(
            self.player.name, self.started, self.minutes,)




class Shot(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    x = db.Column(db.Integer(), )
    y = db.Column(db.Integer(), )
    on_goal = db.Column(db.Boolean(), default=False, nullable=False)
    pk = db.Column(db.Boolean(), default=False, nullable=False)

    # relationships
    player_match_id = db.Column(db.Integer, db.ForeignKey('player_match.id'),
                                nullable=False)
    player_match = db.relationship("PlayerMatch", back_populates="shots")

    goal = db.relationship("Goal", uselist=False, back_populates="shot")

    def __init__(self, player_match, x=None, y=None, on_goal=None, pk=None, goal=None):
        self.player_match = player_match
        self.x = x
        self.y = y
        self.on_goal = on_goal
        self.pk = pk

    def __repr__(self):
        return "Shot (player={}, x={}, y={}, on_goal={}, pk={})".format(
            self.player_match.player.name, self.x, self.y, self.on_goal, self.pk)


class Goal(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.Integer(), nullable=True)

    player_match_id = db.Column(db.Integer, db.ForeignKey('player_match.id'),
                                nullable = False)
    player_match = db.relationship("PlayerMatch", back_populates="goals")

    # relationships
    shot_id = db.Column(db.Integer, db.ForeignKey('shot.id'), nullable=False)
    shot = db.relationship("Shot", back_populates="goal")

    assist = db.relationship("Assist", back_populates="goal")

    def __init__(self, player_match, shot, time=None, ):
        self.time = time
        self.shot = shot
        self.player_match = player_match

    def __repr__(self):
        return "Goal (player={}, assist.player )".format(
            self.player_match.player.name, self.assist.player_match.player.name)


class Assist(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    player_match_id = db.Column(db.Integer, db.ForeignKey('player_match.id'),
                                nullable=False )
    player_match = db.relationship("PlayerMatch", back_populates="assists")

    # relationships
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)
    goal = db.relationship("Goal", back_populates="assist")

    def __init__(self, player_match, goal):
        self.player_match = player_match
        self.goal = goal

    def __repr__(self):
        return "Assist (player={}, goal.player={})".format(
            self.player_match.player.name, self.goal.player_match.player.name )


class ShotAgainst(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    x = db.Column(db.Integer(), )
    y = db.Column(db.Integer(), )
    on_goal = db.Column(db.Boolean(), default=False, nullable=False)
    goal = db.Column(db.Boolean(), default=False, nullable=False)
    pk = db.Column(db.Boolean(), default=False, nullable=False)

    # relationships
    player_match_id = db.Column(db.Integer, db.ForeignKey('player_match.id'),
                                nullable=False)
    player_match = db.relationship("PlayerMatch", back_populates="shots_against")

    def __init__(self, x=None, y=None, on_goal=None, saved=None, goal=None, pk=None, ):
        self.x = x
        self.y = y
        self.on_goal = on_goal
        self.saved = saved
        self.goal = goal
        self.pk = pk

