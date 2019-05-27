from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import datetime

from .settings import Config
from .shared import db


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

'''
class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)
'''

# many to many relationship between User and Team
class TeamsUsers(db.Model):
    __tablename__ = 'teams_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column('team_id', db.Integer, db.ForeignKey('team.id'))


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description


class User(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    token = db.Column(db.String())
    email = db.Column(db.String())

    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))

    teams = db.relationship('Team', secondary='teams_users',
                            backref=db.backref('teams', lazy='dynamic'))

    def __init__(self, username, password, email=None):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def generate_auth_token(self, expiration=6000):
        # 6000 seconds = 100 minutes
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    @hybrid_property
    def is_editor(self):
        """ return True if editor is in roles"""
        return "editor" in [i.name for i in self.roles]

    def __repr__(self):
        return '<User {} (id={})>'.format(self.id, self.username)


class Team(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    team_crest_uri = db.Column(db.String())

    # relationships
    matches = db.relationship('Match', back_populates="team")
    players = db.relationship("Player", back_populates="team")
    opponents = db.relationship("Opponent", back_populates="team")
    competitions = db.relationship("Competition", back_populates="team")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "Team (id={}, name={})".format(self.id, self.name)


class Opponent(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    note = db.Column(db.String())
    team_crest_uri = db.Column(db.String())
    external_url = db.Column(db.String())

    # relationships
    matches = db.relationship("Match", back_populates="opponent")

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'),
                        nullable=False, index=True)

    team = db.relationship("Team",
                           uselist=False,
                           back_populates="opponents")

    @hybrid_property
    def num_match_won(self):
        """ return competition result in W-D-L format """
        return len([i for i in self.matches if (i.result == "win")])

    @hybrid_property
    def num_match_tied(self):
        """ return competition result in W-D-L format """
        return len([i for i in self.matches if (i.result == "tie")])

    @hybrid_property
    def num_match_lost(self):
        """ return competition result in W-D-L format """
        return len([i for i in self.matches if (i.result == "loss")])

    @hybrid_property
    def num_match(self):
        """ number of matches """
        return len(self.matches)

    @hybrid_property
    def match_results(self):
        """ return competition result in W-D-L format """
        return "{}-{}-{}".format(self.num_match_won,
                                 self.num_match_tied,
                                 self.num_match_lost)

    @hybrid_property
    def goal_differential(self):
        """ team's goal differential vs this opponent """
        return sum([i.goal_differerential for i in self.matches])

    def __init__(self, name, team, external_url=None, note=None):
        self.name = name
        self.team = team
        self.external_url = external_url
        self.note = note

    def __repr__(self):
        return "Opponent (id={}, name={})".format(self.id, self.name)


class Competition(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    result = db.Column(db.String())
    note = db.Column(db.String())
    level = db.Column(db.String())
    external_url = db.Column(db.String())

    # relationships
    matches = db.relationship("Match", back_populates="competition")

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'),
                        nullable=False, index=True)
    team = db.relationship("Team",
                           uselist=False,
                           back_populates="competitions")

    @hybrid_property
    def start_date(self):
        """ date of first match """
        if len(self.matches) == 0:
            return datetime.datetime.now().strftime("%Y-%m-%d")
        min_date = min([i.date_time for i in self.matches])
        return min_date.strftime("%Y-%m-%d")

    @hybrid_property
    def num_match_won(self):
        """ number of matches won """
        return len([i for i in self.matches if (i.result == "win")])

    @hybrid_property
    def num_match_tied(self):
        """ number of matches tied """
        return len([i for i in self.matches if (i.result == "tie")])

    @hybrid_property
    def num_match_lost(self):
        """ number of matches lost """
        return len([i for i in self.matches if (i.result == "loss")])

    @hybrid_property
    def num_match(self):
        """ number of matches """
        return len(self.matches)

    @hybrid_property
    def match_results(self):
        """ return competition result in W-D-L format """
        return "{}-{}-{}".format(self.num_match_won,
                                 self.num_match_tied,
                                 self.num_match_lost)

    @hybrid_property
    def goal_differential(self):
        """ team's goal differential vs this opponent """
        return sum([i.goal_differerential for i in self.matches])

    @hybrid_property
    def clean_sheets(self):
        """ team's clean sheets aka no goals allowed """
        return len([1 for i in self.matches if (i.num_goals_against == 0)])

    def __init__(self, name, team, level=None, result=None, external_url=None, note=None):
        self.name = name
        self.team = team
        self.level = level
        self.result = result
        self.external_url = external_url
        self.note = note

    def __repr__(self):
        return "Competition (id={}, name={})".format(self.id, self.name)


class Match(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    date_time = db.Column(db.DateTime(), nullable=False, index=True)
    at_home = db.Column(db.Boolean())
    duration = db.Column(db.Integer())  # match duration in minutes
    note = db.Column(db.String())

    # relationships
    player_matches = db.relationship("PlayerMatch", back_populates="match",
                                     cascade="all, delete-orphan")

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'),
                        nullable=False, index=True)
    team = db.relationship("Team",
                           uselist=False,
                           back_populates="matches")

    opponent_id = db.Column(db.Integer, db.ForeignKey('opponent.id'),
                            nullable=False, index=True)
    opponent = db.relationship("Opponent",
                               uselist=False,
                               back_populates="matches")

    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'),
                               index=True)
    competition = db.relationship("Competition",
                                  uselist=False,
                                  back_populates="matches")

    match_stats = db.relationship("MatchStats",
                                  uselist=False,
                                  back_populates="match",
                                  cascade="all, delete-orphan")

    @hybrid_property
    def opponent_name(self):
        return self.opponent.name

    @hybrid_property
    def competition_name(self):
        return self.competition.name

    @hybrid_property
    def result(self):
        goals_for = self.num_goals
        goals_against = self.num_goals_against

        if goals_for > goals_against:
            result = "win"
        elif goals_for < goals_against:
            result = "loss"
        else:
            result = "tie"

        return result

    @hybrid_property
    def result_long(self):
        return "{}-{} {}".format(self.num_goals,
                                 self.num_goals_against,
                                 self.result)

    @hybrid_property
    def score(self):
        return "{}-{}".format(self.num_goals,
                              self.num_goals_against)

    @hybrid_property
    def label(self):
        return "match 2 of tourney X (2017/11/5), - or something"

    @hybrid_property
    def num_goals(self):
        return sum([i.num_goals for i in self.player_matches])

    @hybrid_property
    def num_goals_against(self):
        return sum([i.num_goals_against for i in self.player_matches])

    def _goals_timeline(self, by_opponent):
        goals = db.session.query(Goal).join(Shot).join(PlayerMatch).join(Match) \
            .filter(Match.id == self.id).filter(Shot.by_opponent == by_opponent).all()

        return [i.label for i in sorted(goals, key=lambda x: x.time if x.time else 0)]

    @hybrid_property
    def goal_differerential(self):
        return self.num_goals - self.num_goals_against

    @hybrid_property
    def goals_timeline(self):
        return self._goals_timeline(by_opponent=False)

    @hybrid_property
    def goals_against_timeline(self):
        return self._goals_timeline(by_opponent=True)

    @hybrid_property
    def num_shots(self):
        return sum([i.num_shots for i in self.player_matches])

    @hybrid_property
    def num_shots_on_target(self):
        return sum([i.num_shots_on_target for i in self.player_matches])

    @hybrid_property
    def num_shots_against(self):
        return sum([i.num_shots_against for i in self.player_matches])

    @hybrid_property
    def opponent_num_shots_on_target(self):
        return sum([i.num_shots_against_on_target for i in self.player_matches])

    @hybrid_property
    def shot_on_target_pct(self):
        try:
            return round(self.num_shots_on_target / self.num_shots * 100, 1)
        except ZeroDivisionError:
            return 0.0

    @hybrid_property
    def opponent_shot_on_target_pct(self):
        try:
            return round(self.opponent_num_shots_on_target /
                         self.num_shots_against * 100, 1)
        except ZeroDivisionError:
            return 0.0

    @hybrid_property
    def num_corners(self):
        return sum([i.corners for i in self.player_matches])

    @hybrid_property
    def num_opponent_corners(self):
        try:
            return self.match_stats.opponent_corners
        except:
            return

    @hybrid_property
    def num_yellow_cards(self):
        return sum([i.yellow_cards for i in self.player_matches])

    @hybrid_property
    def num_opponent_yellow_cards(self):
        try:
            return self.match_stats.opponent_yellow_cards
        except:
            return

    @hybrid_property
    def num_red_cards(self):
        return sum([i.red_cards for i in self.player_matches])

    @hybrid_property
    def num_opponent_red_cards(self):
        try:
            return self.match_stats.opponent_red_cards
        except:
            return

    @hybrid_property
    def num_passes(self):
        try:
            return self.match_stats.passes
        except:
            return

    @hybrid_property
    def num_opponent_passes(self):
        try:
            return self.match_stats.opponent_passes
        except:
            return

    @hybrid_property
    def num_pass_strings(self):
        try:
            return self.match_stats.pass_strings
        except:
            return

    @hybrid_property
    def num_opponent_pass_strings(self):
        try:
            return self.match_stats.opponent_pass_strings
        except:
            return

    @hybrid_property
    def pass_pct(self):
        try:
            return self.match_stats.pass_pct
        except:
            return

    @hybrid_property
    def opponent_pass_pct(self):
        try:
            return self.match_stats.opponent_pass_pct
        except:
            return

    def __init__(self, date_time, team, opponent, competition=None,
                 at_home=True, duration=None, note=None):
        self.date_time = date_time #datetime.datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S", )
        self.team = team
        self.opponent = opponent
        self.competition = competition
        self.at_home = at_home
        self.duration = duration
        self.note = note

    def __repr__(self):
        return "Match (id={}, team={}, opponent={}, date_time={})".format(
            self.id, self.team, self.opponent, self.date_time)


class MatchStats(db.Model, CRUD_MixIn):
    """ match statistics beyond what's derived from player_match """
    id = db.Column(db.Integer(), primary_key=True)

    # high level opponent stats
    opponent_yellow_cards = db.Column(db.Integer(), default=0)
    opponent_red_cards = db.Column(db.Integer(), default=0)
    opponent_corners = db.Column(db.Integer(), default=0)
    opponent_fouls = db.Column(db.Integer())

    # team pass numbers
    passes = db.Column(db.Integer())
    pass_strings = db.Column(db.Integer())
    pass_pct = db.Column(db.Float())

    # opponent pass numbers
    opponent_passes = db.Column(db.Integer())
    opponent_pass_strings = db.Column(db.Integer())
    opponent_pass_pct = db.Column(db.Float())

    # possession split
    possession = db.Column(db.Float())

    # relationships
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'),
                         nullable=False, index=True)
    match = db.relationship("Match",
                            uselist=False,
                            back_populates="match_stats")

    def __init__(self, match, passes=None, pass_strings=None, pass_pct=None,
                 possession=None,
                 opponent_passes=None,
                 opponent_pass_strings=None,
                 opponent_pass_pct=None,
                 opponent_yellow_cards=None,
                 opponent_red_cards=None,
                 opponent_corners=None,
                 opponent_fouls=None):
        self.match = match
        self.passes = passes
        self.pass_strings = pass_strings
        self.pass_pct = pass_pct
        self.possession = possession
        self.opponent_passes = opponent_passes
        self.opponent_pass_strings = opponent_pass_strings
        self.opponent_pass_pct = opponent_pass_pct
        self.opponent_yellow_cards = opponent_yellow_cards
        self.opponent_red_cards = opponent_red_cards
        self.opponent_corners = opponent_corners
        self.opponent_fouls = opponent_fouls

    def __repr__(self):
        return "MatchStats (id={}, passes={}, opponent_passes={})".format(
            self.id, self.passes, self.opponent_passes)


class Player(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    number = db.Column(db.Integer())
    active = db.Column(db.Integer(), nullable=False, default=True)

    # relationships
    player_matches = db.relationship("PlayerMatch", back_populates="player")

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True,
                        index=True)
    team = db.relationship("Team", back_populates="players")

    @hybrid_property
    def label(self):
        return "{} #{}".format(self.name, self.number)

    @hybrid_property
    def num_apps(self):
        return len(self.player_matches)

    def __init__(self, name, number=None, team=None, active=True):
        self.name = name
        self.number = number
        self.team = team
        self.active = active

    def __repr__(self):
        return "Player (id={}, number={}, name={})".format(
            self.id, self.number, self.name)


class PlayerMatch(db.Model, CRUD_MixIn):
    __table_args__ = (db.UniqueConstraint('player_id', 'match_id'),)

    id = db.Column(db.Integer(), primary_key=True)
    starter = db.Column(db.Boolean(), default=False)
    minutes = db.Column(db.Integer(), default=0)
    subbed_due_to_injury = db.Column(db.Boolean(), default=False)
    yellow_cards = db.Column(db.Integer(), default=0)
    red_cards = db.Column(db.Integer(), default=0)
    corners = db.Column(db.Integer(), default=0)
    fouls = db.Column(db.Integer(), default=0)

    # relationships
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                          nullable=False, index=True)
    player = db.relationship("Player",
                             uselist=False,
                             back_populates="player_matches")

    match_id = db.Column(db.Integer, db.ForeignKey('match.id'),
                         nullable=False, index=True)
    match = db.relationship("Match",
                            uselist=False,
                            back_populates="player_matches")

    shots = db.relationship("Shot", back_populates="player_match",
                            cascade="all, delete-orphan")

    # goal cascades to assist
    assists = db.relationship("Assist", back_populates="player_match")

    @hybrid_property
    def player_label(self):
        return self.player.label

    @hybrid_property
    def num_shots(self):
        return len([i for i in self.shots if not i.by_opponent])

    @hybrid_property
    def num_shots_against(self):
        return len([i for i in self.shots if i.by_opponent])

    @hybrid_property
    def num_shots_on_target(self):
        return len([i for i in self.shots if (not i.by_opponent and i.on_target)])

    @hybrid_property
    def num_shots_against_on_target(self):
        return len([i for i in self.shots if (i.by_opponent and i.on_target)])

    @hybrid_property
    def num_goals(self):
        return len([i for i in self.shots if (i.scored and not i.by_opponent)])

    @hybrid_property
    def num_goals_against(self):
        return len([i for i in self.shots if (i.scored and i.by_opponent)])

    @hybrid_property
    def num_saves(self):
        return len([i for i in self.shots if i.by_opponent])

    @hybrid_property
    def num_assists(self):
        return len(self.assists)

    def __init__(self, player, match, starter=True, minutes=0,
                 subbed_due_to_injury=None,
                 yellow_cards=None, red_cards=None, corners=None, ):
        self.player = player
        self.match = match
        self.starter = starter
        self.minutes = minutes
        self.subbed_due_to_injury = subbed_due_to_injury
        self.yellow_cards = yellow_cards
        self.red_cards = red_cards
        self.corners = corners

    def __repr__(self):
        return "PlayerMatch (id={}, player={}, starter={}, minutes={})".format(
            self.id, self.player.name, self.starter, self.minutes, )


class Shot(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    x = db.Column(db.Integer(), )
    y = db.Column(db.Integer(), )
    on_target = db.Column(db.Boolean(), default=False, nullable=False)
    pk = db.Column(db.Boolean(), default=False)
    by_opponent = db.Column(db.Boolean(), default=False)
    blocked = db.Column(db.Boolean(), nullable=True)

    # relationships
    player_match_id = db.Column(db.Integer, db.ForeignKey('player_match.id'),
                                nullable=False, index=True)
    player_match = db.relationship("PlayerMatch",
                                   uselist=False,
                                   back_populates="shots")

    goal = db.relationship("Goal", uselist=False, back_populates="shot",
                           cascade="all, delete-orphan")

    @hybrid_property
    def scored(self):
        return self.goal is not None

    @hybrid_property
    def player_number(self):
        return self.player_match.player.number

    @hybrid_property
    def player_label(self):
        return self.player_match.player_label

    def __init__(self, player_match, x=None, y=None, on_target=None,
                 pk=None, by_opponent=None, blocked=None):
        self.player_match = player_match
        self.x = x
        self.y = y
        self.on_target = on_target
        self.pk = pk
        self.by_opponent = by_opponent
        self.blocked = blocked

    def __repr__(self):
        return "Shot (id={}, player={}, x={}, y={}, on_target={})".format(
            self.id,
            self.player_match.player.name,
            self.x, self.y, self.on_target,
            self.pk, self.by_opponent)


class Goal(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.Integer(), nullable=True)
    own_goal = db.Column(db.Boolean(), default=False)

    @hybrid_property
    def assisted(self):
        return self.assist is not None

    # relationships
    shot_id = db.Column(db.Integer, db.ForeignKey('shot.id'),
                        nullable=False, index=True)
    shot = db.relationship("Shot", uselist=False, back_populates="goal")

    assist = db.relationship("Assist", back_populates="goal", uselist=False,
                             cascade="all, delete-orphan")

    @hybrid_property
    def label(self):
        if self.time is not None:
            time = str(self.time) + "'"
        else:
            time = "?'"

        assist = ""
        if self.assist:
            assist = " ({})".format(self.assist.player_match.player.name)

        # reuse assist to carry PK/OG tags
        if self.shot.pk:
            assist = " PK"

        if self.own_goal:
            assist = " OG"

        # if team goal, put player's name, else blank
        if self.shot.by_opponent:
            player = ""
        else:
            player = self.shot.player_match.player.name

        return "{}{} {}".format(player, assist, time)

    def __init__(self, shot, time=None):
        self.shot = shot
        self.time = time

    def __repr__(self):
        return "Goal (id={}, player={}, )".format(
            self.id, self.shot.player_match.player.name)


class Assist(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer(), primary_key=True)

    # relationships
    player_match_id = db.Column(db.Integer, db.ForeignKey('player_match.id'),
                                nullable=False, index=True)
    player_match = db.relationship("PlayerMatch",
                                   uselist=False,
                                   back_populates="assists")

    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'),
                        nullable=False, index=True)
    goal = db.relationship("Goal", uselist=False, back_populates="assist")

    @hybrid_property
    def player_label(self):
        return self.player_match.player_label

    def __init__(self, player_match, goal):
        self.player_match = player_match
        self.goal = goal

    def __repr__(self):
        return "Assist (id={}, player={}, Goal.player={})".format(
            self.id,
            self.player_match.player.name,
            self.goal.shot.player_match.player.name)
