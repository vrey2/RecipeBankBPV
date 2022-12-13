

from .extensions import db
from flask_login import UserMixin
class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True)
    password = db.Column('password', db.String(20))

class Recipe(db.Model):
    __tablename__ = 'Recipes'
    id = db.Column('id', db.Integer, primary_key= True)
    name = db.Column('name', db.String(150))
    serving = db.Column('serve', db.Integer())
    prep = db.Column('prep', db.String(100))
    cook = db.Column('cook', db.String(100))
    ingredients = db.Column('ingr', db.String(1000))
    instruction = db.Column('instr', db.String(1000))
    time = db.Column('time', db.String(100))
    user_id = db.Column('user_id', db.ForeignKey('user.id'), nullable=False)
    # author = db.relationship('User', backref=db.backref('Recipe', uselist=False))