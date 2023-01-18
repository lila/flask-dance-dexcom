import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.dexcom import make_dexcom_blueprint, dexcom

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["DEXCOM_OAUTH_CLIENT_ID"] = os.environ.get("DEXCOM_OAUTH_CLIENT_ID")
app.config["DEXCOM_OAUTH_CLIENT_SECRET"] = os.environ.get("DEXCOM_OAUTH_CLIENT_SECRET")
dexcom_bp = make_dexcom_blueprint(
    scope="offline_access", 
    redirect_url="http://localhost:5000/login/dexcom/authorized")
app.register_blueprint(dexcom_bp, url_prefix="/login")

@app.route("/")
def index():

    if not dexcom.authorized:
        return redirect(url_for("dexcom.login"))
    
    resp = dexcom.get("/v2/users/self/dataRange")
    assert resp.ok
    return "Datarange = @{login} from Dexcom".format(login=resp.json())

