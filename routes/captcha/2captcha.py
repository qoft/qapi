import flask
import httpx
from flask import render_template, request, redirect
import config

from utils import view

blueprint = flask.Blueprint('2captcha', __name__)


@blueprint.route(f"{config.captcha_route}/2captcha/<string:key>", methods=['GET'])
def _2captcha(key):
    if len(key) != 32:
        return view({"error": True, "message": "bad key", "type": "2captcha"})

    sex = httpx.post("https://2captcha.com/res.php", params={"key": key, "action": "getbalance"}).text
    message = dict()
    message.update({"type": "2captcha"})
    match sex:
        case "ERROR_WRONG_USER_KEY":
            message.update({"error": True, "message": "bad key"})
        case "ERROR_KEY_DOES_NOT_EXIST":
            message.update({"error": True, "message": "bad key"})
        case _:
            message.update({"error": False, "balance": sex})

    return view(message)


@blueprint.route(f"{config.captcha_route}/2captcha/", methods=['GET'])
def _2captcha_input():
    if request.args:
        print(f"/{request.args['key']}")
        return redirect(f"{config.captcha_route}/2captcha/{request.args['key']}", code=302)
    return render_template("input.html", type="2captcha", title="2captcha")






