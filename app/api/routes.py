from flask import Blueprint, render_template
from ..extensions import db
from ..models import *
from faker import Faker
from faker_sqlalchemy import SqlAlchemyProvider

fake = Faker()
fake.add_provider(SqlAlchemyProvider)

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getrecipes')
def getrecipes():
    recipes = db.session.execute(db.select(Recipe).order_by(Recipe.id)).scalars()
    return recipes.all()

@api.route('/buildFakeDB')
def buildFakeDB():
    mike1 = User(username=fake.first_name(), password=fake.ssn())
    db.session.add(mike1)
    instance = fake.sqlalchemy_model(Recipe)
    instance.author = mike1.username
    db.session.add(instance)
    db.session.commit()
    print(mike1)
    print(instance)
    return "done!"
