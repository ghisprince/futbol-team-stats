from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
api = Api()
jwt = JWTManager()
