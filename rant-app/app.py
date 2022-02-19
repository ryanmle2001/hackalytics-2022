from flask import Flask, url_for, render_template, request, redirect, abort, jsonify, session, flash, make_response
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import pathlib
import os
import requests
from pip._vendor import cachecontrol
import google.auth.transport.requests
import db.database as db
import ml.model as model

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
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info['email']

    if session["email"] in db.get_users():
        return redirect('/home')
    return redirect(url_for("create_account"))

@app.route("/create-account", methods=["GET"])
def create_account():
    if "google_id" not in session:
        return session # Authorization required
    return render_template("create_account.html")

@app.route("/new-account", methods=["GET", "POST"])
def new_account():
    if request.method == "POST":
        # username = request.form["username"]
        # if username in db.get_users():
        #     flash("This username is taken")
        #     return redirect(url_for("create_account"))
        user = {"email": session["email"],
                "first_name": request.form["first_name"],
                "last_name": request.form["last_name"],
                "display_name": request.form["display_name"],
                "age": request.form['age'],
                "interests": [],
                "rant_count": 0,
                "rants": []
                }
        db.insert_user(user)
        return redirect(url_for("home"))
    else:
        return redirect(url_for("index"))

@app.route("/home")
def home():
    if "google_id" not in session:
        return abort(401)  # Authorization required
    rants = db.get_rants(session["email"])
    return render_template("home.html", rants=rants)

@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method == "POST":
        rant_id = session["email"][:session["email"].index("@")] + '-' + str(db.get_user_field(session["email"], "rant_count"))
        rant_text = request.form["upload"]
        rant_score = model.analyze(rant_text)
        rant_category = []
        rant = {"rant_id": rant_id,
                "email": session["email"],
                "text": rant_text,
                "sentiment_score": rant_score,
                "categories": rant_category
        }
        db.insert_rant(rant)
        return redirect(f"/rant/{rant_id}")
    return redirect(url_for("home"))


@app.route('/rant/<string:rant_id>', methods=["GET", "POST"])
def match(rant_id):
    if session["email"][:session["email"].index("@")] not in rant_id:
        return redirect(url_for("home"))
    match = db.match_rant(rant_id)
    return render_template("match.html", match=match)

# @app.route('/user/<string:username>')
# def display_user(username):
#     return f"Displaying {username}'s account"

@app.route('/user/<string:username>/edit-my-profile')
def edit_my_user(username):
    return f"Editing {username}'s account"


@app.route('/user/<string:username>/view-my-profile')
def display_my_user(username):
    return f"Displaying my account"


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))


@app.route("/logout")
def logout():
    session.clear()
    #TODO: figure out how to clear google auth cookies
    return redirect("/")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

@app.errorhandler(500) #TODO add proper handler here
def page_not_found(error):
    return render_template("page_not_found.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
