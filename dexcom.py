import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.dexcom import make_dexcom_blueprint, dexcom

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["DEXCOM_OAUTH_CLIENT_ID"] = os.environ.get("DEXCOM_OAUTH_CLIENT_ID")
app.config["DEXCOM_OAUTH_CLIENT_SECRET"] = os.environ.get("DEXCOM_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("dexcom.login"))
    resp = github.get("/user")
    assert resp.ok
    return "You are @{login} on Dexcom".format(login=resp.json()["login"])
