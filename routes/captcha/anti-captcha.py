import flask
from flask import render_template, request, redirect, url_for, flash, jsonify
import httpx
import utils
import config
blueprint = flask.Blueprint('anti-captcha', __name__)


@blueprint.route(f"{config.captcha_route}/anti-captcha/<string:key>", methods=['GET'])
def _anti_captcha(key):
    if len(key) != 32:
        return utils.view({"error": True, "message": "bad key", "type": "anti-captcha"})

    sex = httpx.post(f"https://api.anti-captcha.com/getBalance", json={"clientKey": key}).json()
    json = dict()
    json.update({"type": "anti-captcha"})
    match sex["errorId"]:
        case 1:
            json.update({"error": True, "message": "Bad Key."})
        case 0:
            json.update({"error": False, "balance": sex["balance"]})
    return utils.view(json)


@blueprint.route(f"{config.captcha_route}/anti-captcha/", methods=['GET'])
def _anti_captcha_input():
    if request.args:
        return redirect(f"{config.captcha_route}/anti-captcha/{request.args['key']}", code=302)
    return render_template("input.html", type="anti-captcha", title="anti-captcha", placeholder="APIKey")






