from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,SubmitField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICIATIONS']= False

db = SQLAlchemy(app)

# Coffee list [mock database]
# coffee = ['espresso', 'house', 'kenyan', 'sumatran']

# create database model(s)
class CoffeeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coffee_name = db.Column(db.String(80), index=True)
    coffee_description = db.Column(db.String(250), index=False)

    def __repr__(self):
        return f'{self.id} {self.coffee_name} {self.coffee_description}'

#create flask form
class CoffeeForm(FlaskForm):
    name = StringField('Coffee Name')
    description = TextAreaField('Coffee Description')
    submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
    pass

# initialize database
# db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'name' in request.form:
        db.session.add(CoffeeModel(coffee_name=request.form['name'], coffee_description=request.form['description']))
        db.session.commit()
    return render_template("index.html", blends=CoffeeModel.query.all(), template_form=CoffeeForm())

@app.route('/update', methods=['GET', 'POST'])
def update():
    return render_template("update.html", blends=CoffeeModel.query.all(), template_form=Updateform())