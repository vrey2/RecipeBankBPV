from flask import Flask
from flask_bootstrap import Bootstrap

from app.api.routes import api
from app.site.routes import site
from app.admin.routes import admin

from app.extensions import db
def booty(app):
    boot = Bootstrap(app)
    return boot

def data(app):
    ...
def create_app():
    app = Flask(__name__)

    booty(app)

    app.register_blueprint(api)
    app.register_blueprint(site)
    app.register_blueprint(admin)

    app.config['SECRET_KEY'] = 'secretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # thios is only here cause i was testing. this makes DB but does not build.
    with app.app_context():
        db.create_all()


    return app

