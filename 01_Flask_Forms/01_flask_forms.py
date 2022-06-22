from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "bluemuffins_in_winter_lane"


@app.route('/form01')
def index():
    flash("Who are you?")
    return render_template("index.html")

@app.route("/greet", methods=["POST", "GET"])
def greet():
    flash("Greetings " + str(request.form['name_input']) + ", the light welcomes you.")
    return render_template("index.html")
