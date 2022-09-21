from datetime import datetime
from email.policy import default
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPER-seCRet-Key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myUserDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICITIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String)
    join_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    pass
@app.route('/')
def index():
    return render_template('index.html')