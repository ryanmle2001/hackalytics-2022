from flask import Flask, render_template, redirect, url_for
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



if __name__ == "__main__":
    app.run(debug=True)