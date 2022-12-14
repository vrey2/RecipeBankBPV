from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, subquery
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
logMan = LoginManager()
bcrypt = Bcrypt()
