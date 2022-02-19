import os
import pathlib

from flask import Flask, render_template, request, redirect, abort, jsonify, session
from google_auth_oauthlib.flow import Flow

app = Flask(__name__)
app.secret_key="Hello"

GOOGLE_CLIENT_ID = "829965262603-houdc4q9b3uohkn7t6v97mtic4ehg7og.apps.googleusercontent.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file, scopes=[
    "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
                                     )

@app.route("/")
def login():
    # if user has account -> go to home page
    # else -> go to /create-acount
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

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

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = request.sessions()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oath2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )


if __name__ == "__main__":
    app.run(debug=True)