from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

# from app.api.routes import api
from app.site.routes import site
from app.admin.routes import admin

from app.extensions import db, logMan, bcrypt
from app.models import User
def booty(app):
    boot = Bootstrap(app)
    return boot

def data(app):
    db = SQLAlchemy(app)
    db.init_app(app)
    db.create_all()
    return db

def create_app():
    app = Flask(__name__,template_folder='./site/templates',static_folder='./site/static')

    booty(app)

    # app.register_blueprint(api)
    app.register_blueprint(site)
    app.register_blueprint(admin)

    app.config['SECRET_KEY'] = 'secretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #database
    db.init_app(app)
    #bcrypt
    bcrypt.init_app(app)
    #login manager
    logMan.init_app(app)
    logMan.login_view = 'site.login'

    # thios is only here cause i was testing. this makes DB but does not build.
    with app.app_context():
        db.create_all()


    return app

if __name__ == '__main__':
    app = create_app()
    data(app)
    app.run(debug=True)
