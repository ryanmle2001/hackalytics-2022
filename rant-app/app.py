from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import db.database as db
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    if True: #TODO: replace with Google Auth -> if no account already
        return  redirect(url_for('create_account'))
    return redirect(url_for('home'))

@app.route("/home", methods=["GET", "POST"])
def home():
    return "This is the home page after login + creating a new account"


@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    return render_template("create_account.html")

@app.route("/new-account", methods=["GET", "POST"])
def new_account():
    username = request.form["username"]
    if username in db.get_users():
        return redirect(url_for("create_account"))
    user = {"username": request.form["username"],
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "display_name": request.form["display_name"],
            "age": request.form['age']}
    db.insert_user(user)
    return redirect(url_for("home"))


@app.route('/user/<string:username>')
def display_user(username):
    return f"Displaying {username}'s account"

@app.route('/user/<string:username>/edit-my-profile')
def edit_my_user(username):
    return f"Editing {username}'s account"


@app.route('/user/<string:username>/view-my-profile')
def display_my_user(username):
    return f"Diplaying my account"


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))



if __name__ == "__main__":
    app.run(debug=True)