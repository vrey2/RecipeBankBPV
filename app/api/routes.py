from flask import Blueprint, render_template

api = Blueprint('api', __name__)

@api.route('/getrecipes')
def getrecipes():
    return 'hello world'


