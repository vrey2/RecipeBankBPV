from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getrecipes')
def getrecipes():
    return print('data')

