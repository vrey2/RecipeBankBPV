from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from app.api.routes import api
from app.site.routes import site
from app.admin.routes import admin
def booty(app):
    boot = Bootstrap(app)
    return boot

def data(app):
    db = SQLAlchemy(app)
    db.init_app(app)
    db.create_all()
    return db

def create_app():
    app = Flask(__name__)

    booty(app)

    app.register_blueprint(api)
    app.register_blueprint(site)
    app.register_blueprint(admin)

    app.config['SECRET_KEY'] = 'secretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app/data.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    return app

if __name__ == '__main__':
    app = create_app()
    data(app)
    app.run(debug=True)
