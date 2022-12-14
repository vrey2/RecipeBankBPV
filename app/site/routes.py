import flask_login
from flask import Blueprint, render_template, url_for,redirect
from flask_wtf import FlaskForm, form
from flask_sqlalchemy import SQLAlchemy, query
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import logout_user, login_required, current_user, login_user

from app.api.routes import getrecipes, getuserrecipes
from app.extensions import db, logMan, bcrypt
from app.models import User, Recipe

site = Blueprint('site', __name__, template_folder='templates')

@site.route('/', methods=['GET'])
def index():
    return render_template('site/index.html')

@site.route('/login', methods=['GET', 'POST'])
def login():
    # return render_template('/empty.html')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        print("submit")
        if user:
            print("if user")
            if check_password_hash(user.password, form.password.data):
                print("password correct")
                login_user(user)
                return redirect(url_for('site.home'))
    else:
        print("not authing")
        form = LoginForm()
        return render_template('site/login.html', form=form)

    return render_template('site/home.html', form=form, user=current_user)

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
    reclist = getrecipes()
    print("this is getrec")
    print(reclist)
    return render_template('site/home.html', current_user=current_user, items=reclist)

@site.route('/profile', methods=['GET', 'POST', 'PUT'])
@login_required
def profile():
    getusrrec = getuserrecipes(current_user.username)
    return render_template('site/profile.html', current_user=current_user, items=getusrrec)

@site.route('/add_record', methods=['GET', 'POST'])
def add_record():
    form1 = AddRecord()
    if form1.validate_on_submit():
        name = form1.name
        serve = form1.serve
        prep = form1.prep
        cook = form1.cook
        ingr = form1.ingr
        instr = form1.instr
        time = form1.time
        author = form1.author
        record = Recipe(name=name.data, serve=serve.data, prep=prep.data, cook=cook.data, ingr=ingr.data, instr=instr.data, time=time.data, author=author.data)
        # Flask-SQLAlchemy magic adds record to database
        db.session.add(record)
        db.session.commit()
        # create a message to send to the template
        message = f"Recipe \"{name.data}\" for  {author.data} has been submitted."
        return render_template('site/add_record.html', message=message, form1=form1)
    else:
        return render_template('site/add_record.html', form1=form1)

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

class AddRecord(FlaskForm):
    # id used only by update/edit
    id_field = HiddenField()
    name = StringField('Recipe name')
    serve = IntegerField('Servers')
    prep = StringField('Prep Time')
    cook = StringField('Cooking Time')
    ingr = StringField('Ingredients')
    instr = StringField('Instructions')
    time = StringField('Time to cook')
    author = StringField('Author (exact username)')
    # updated - date - handled in the route function
    updated = HiddenField()
    submit = SubmitField('Add Record')
