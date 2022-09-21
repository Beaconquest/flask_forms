from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from os.path import exists


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPER-seCRet-Key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myUserDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICITIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String)
    join_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

if exists('myUserDb.db') == False:
    db.create_all()

@app.route('/')
def index():
    current_users = User.query.all()
    return render_template('index.html', users=current_users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', form=form)