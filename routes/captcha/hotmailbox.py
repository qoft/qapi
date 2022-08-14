import flask
import httpx
from flask import render_template, request, redirect



import utils

blueprint = flask.Blueprint('hotmailbox', __name__)


@blueprint.route("/keys/hotmailbox/<string:key>", methods=['GET'])
def _hotmailbox(key):
    if len(key) != 32:
        return utils.view({"error": True, "message": "bad key", "type": "capmonster"})

    sex = httpx.get(f"https://api.hotmailbox.me/user/balance", params={"apikey": key}).json()
    json = dict()
    json.update({"type": "Hotmailbox"})
    match sex["Code"]:
        case 1:
            json.update({"error": True, "message": "Bad Key."})
        case 0:
            json.update({"error": False, "balance": utils.convert(sex["Balance"], "VND", "USD")})
    return utils.view(json)


@blueprint.route("/keys/hotmailbox/", methods=['GET'])
def _hotmailbox_input():
    if request.args:
        print(f"/{request.args['key']}")
        return redirect(f"/keys/hotmailbox/{request.args['key']}", code=302)
    return render_template("input.html", type="hotmailbox", title="Hotmailbox")






