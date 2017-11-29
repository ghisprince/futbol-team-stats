from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth

db = SQLAlchemy()
ma = Marshmallow()
api = Api()
auth = HTTPBasicAuth()