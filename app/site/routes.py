
from flask import Blueprint, render_template, url_for,redirect
from flask_wtf import FlaskForm, form
from flask_sqlalchemy import SQLAlchemy, query, session
from sqlalchemy import select
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt, generate_password_hash
from flask_login import logout_user, login_required, current_user, login_user
from app.extensions import db, logMan, bcrypt
from app.models import User
from app.api.routes import api

site = Blueprint('site', __name__, template_folder='templates')

@site.route('/', methods=['GET', 'POST'])
def login():
    # return render_template('/empty.html')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect(url_for('.home', user=user))

    return render_template('site/login.html', form=form)

@site.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_pass = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=new_pass)
        db.session.add(new_user)
        db.session.commit()
        form_1 = LoginForm()
        return render_template('site/login.html', form=form_1)
    return render_template('site/register.html', form=form)

@site.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    form = LoginForm()
    return render_template('site/login.html', form=form)

@site.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('site/home.html', user=current_user)

@site.route('/profile', methods=['GET', 'POST', 'PUT'])
@login_required
def profile():
    return render_template('site/profile.html', user=current_user)

@site.route('/getrecipes')
def getrecipes():
    return 'hello world'

@site.route('/myrecipes', methods=['GET', 'POST', 'PUT'])
def myrecipes():
    return 'here are the recipes'

@logMan.user_loader
def load_user(user_id):

    # db.session.execute(db.select(User).filter_by(id=i))
    return User.query.get_id(int(user_id))

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one.')
