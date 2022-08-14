import flask
from flask import render_template, request, redirect, url_for, flash, jsonify
import httpx
import utils

blueprint = flask.Blueprint('capmonster', __name__)


@blueprint.route("/keys/capmonster/<string:key>", methods=['GET'])
def _capmonster(key):
    if len(key) != 32:
        return utils.view({"error": True, "message": "bad key", "type": "capmonster"})

    sex = httpx.post(f"https://api.capmonster/getBalance", json={"clientKey": key}).json()
    json = dict()
    json.update({"type": "Capmonster"})
    match sex["errorId"]:
        case 1:
            json.update({"error": True, "message": "Bad Key."})
        case 0:
            json.update({"error": False, "balance": sex["balance"]})
    return utils.view(json)


@blueprint.route("/keys/capmonster/", methods=['GET'])
def _capmonster_input():
    if request.args:
        print(f"/{request.args['key']}")
        return redirect(f"/captcha/capmonster/{request.args['key']}", code=302)
    return render_template("input.html", type="capmonster", title="Capmonster")






