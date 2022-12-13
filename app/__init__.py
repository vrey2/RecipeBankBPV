from flask import Flask
from flask_bootstrap import Bootstrap

from app.api.routes import api
from app.site.routes import site
from app.admin.routes import admin
def booty(app):
    boot = Bootstrap(app)
    return boot

def data(app):


def create_app():
    app = Flask(__name__)

    booty(app)

    app.register_blueprint(api)
    app.register_blueprint(site)
    app.register_blueprint(admin)

    app.config['SECRET_KEY'] = 'secretKey'

    return app

