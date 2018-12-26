from flask import Blueprint, render_template, flash, redirect, url_for, send_file, session, request, jsonify

#from .. extensions import cache
from .. models import *
from .. api import *

main = Blueprint('main', __name__)
