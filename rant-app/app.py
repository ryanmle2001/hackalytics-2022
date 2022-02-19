from flask import Flask, url_for, render_template, request, redirect, abort, jsonify, session
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import pathlib
import os
import requests
from pip._vendor import cachecontrol
import google.auth.transport.requests
import db.database as db

app = Flask(__name__)
app.secret_key="Hello"

GOOGLE_CLIENT_ID = "829965262603-houdc4q9b3uohkn7t6v97mtic4ehg7og.apps.googleusercontent.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file, scopes=[
    "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    # if user has account -> go to home page
    # else -> go to /create-acount
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["email"] = id_info['email']

    if id_info["email"] in db.get_emails():
        return redirect(url_for('home'))
    return render_template("create_account.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    return "This is the home page after login + creating a new account"


@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    username = request.form["username"]
    if username in db.get_users():
        return redirect(url_for("create_account"))
    user = {"email": session["email"],
            "username": request.form["username"],
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


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

@app.errorhandler(500) #TODO add proper handler here
def page_not_found(error):
    return render_template("page_not_found.html"), 500



if __name__ == "__main__":
    app.run(debug=True)