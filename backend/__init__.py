#! ../env/bin/python

from flask import Flask
from flask_caching import Cache
from . controllers.main import main
from . shared import api
from . shared import db
from . shared import ma
from . shared import login_manager

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='{%',
        block_end_string='%}',
        variable_start_string='((',  # instead of jinja2 default of {{
        variable_end_string='))',  # instead of }}
        comment_start_string='{#',
        comment_end_string='#}',
    ))


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. app.settings.ProdConfig
    """

    # app = Flask(__name__)
    app = CustomFlask(__name__)

    app.config.from_object(object_name)

    # initialize the cache
    cache = Cache()
    cache.init_app(app)

    # register SQLAlchemy
    db.init_app(app)

    # register Marshmallow
    ma.init_app(app)

    # register flask_restful api
    api.init_app(app)

    # register LoginManager
    login_manager.init_app(app)

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
