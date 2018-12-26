from flask import Blueprint

#from .. extensions import cache
from . models import *
from . api import *

main = Blueprint('futbol', __name__, url_prefix='/futbol')

@main.route("/ping")
def pong():
    return "Pong!"