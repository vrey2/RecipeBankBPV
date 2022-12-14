import bcrypt
from flask import Blueprint, render_template, url_for,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

site = Blueprint('site', __name__, template_folder='templates')

@site.route('/', methods=['GET', 'POST'])
def login():
    # return render_template('/empty.html')
    form = LoginForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(username=form.username.data).first()
        return redirect(url_for('site/home.html'))

    return render_template('site/login.html', form=form)

@site.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_pass = bcrypt.gensalt(form.password.data)
        new_user = User(username=form.username.data, password=new_pass)

        return render_template('site/login.html')
    return render_template('site/register.html', form=form)
class User(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True)
    password = db.Column('password', db.String(20))

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
        # existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one.')
