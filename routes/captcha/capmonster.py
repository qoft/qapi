import flask
from flask import render_template, request, redirect, url_for, flash, jsonify
import httpx
import utils
import config

blueprint = flask.Blueprint('capmonster', __name__)


@blueprint.route(f"{config.captcha_route}/capmonster/<string:key>", methods=['GET'])
def _capmonster(key):
    if len(key) != 32:
        return utils.view({"error": True, "message": "bad key", "type": "capmonster"})
    try:
        sex = httpx.post(f"https://api.capmonster.cloud/getbalance", json={"clientKey": key}).json()
    except httpx._exceptions.ConnectError:
        return jsonify({"error": True, "message": "error connecting to capmonster.cloud"})
    json = dict()
    json.update({"type": "Capmonster"})
    match sex["errorId"]:
        case 1:
            json.update({"error": True, "message": "Bad Key."})
        case 0:
            json.update({"error": False, "balance": sex["balance"]})
    return utils.view(json)


@blueprint.route(f"{config.captcha_route}/capmonster/", methods=['GET'])
def _capmonster_input():
    if request.args:
        print(f"/{request.args['key']}")
        return redirect(f"{config.captcha_route}/capmonster/{request.args['key']}", code=302)
    return render_template("input.html", type="capmonster", title="Capmonster")






