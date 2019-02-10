from flask import Flask
from . main import main
from . shared import api
from . shared import db
from . shared import ma
from . shared import jwt

def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. app.settings.ProdConfig
    """

    # app = Flask(__name__)
    app = Flask(__name__)
    app.config.from_object(object_name)

    # register extensions
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    api.init_app(main)

    # register our blueprints
    app.register_blueprint(main)

    if not app.debug:
        import logging

        event_handler = logging.FileHandler("logfile.txt")
        event_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))

        event_handler.setLevel(logging.WARNING)
        app.logger.addHandler(event_handler)

    return app
