from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import db.database as db
import json

app = Flask(__name__)

@app.route("/")
def login():
    # if user has account -> go to home page
    # else -> go to /create-acount
    return "This is the main page - login"

@app.route("/home", methods=["GET", "POST"])
def home():
    return "This is the home page after login + creating a new account"


@app.route("/create_account", methods=["GET", "POST"])
def create_account():

    return "Creating accounts"


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