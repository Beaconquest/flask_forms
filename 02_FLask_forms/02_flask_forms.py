from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_super_secret_key'

class TaskForm(FlaskForm):
    task = StringField('New Task:')
    submit = SubmitField('Add Task')

tasks = []

@app.route('/', methods=['GET', 'POST'] )
def index():
    if 'task' in request.form:
        if request.form['task'] in  tasks:
            flash(f"<<{request.form['task']}>> is already included in the task list!")
        else:
            tasks.append(request.form['task'])
    return render_template('index.html', tasks=tasks, template_task_form=TaskForm())
 