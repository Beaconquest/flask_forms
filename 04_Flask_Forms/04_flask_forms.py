from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from os.path import exists


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPER-seCRet-Key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myUserDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    join_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

if exists('myUserDb.db') == False:
    db.create_all()

@app.route('/')
def index():
    current_users = User.query.all()
    return render_template('index.html', current_users=current_users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', title='Register', form=form)

# user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index', _external=True, _scheme='https'))
        else:
            return redirect(url_for('login', _external=True, _scheme='https'))
    return render_template('login.html', form=form)

# user route
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
