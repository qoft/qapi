import flask
import httpx
from flask import render_template, request, redirect
import config


import utils

blueprint = flask.Blueprint('caption', __name__)


@blueprint.route(f"{config.image_route}/caption/<string:text>", methods=['GET'])
def _caption(text):
    return "esex"


@blueprint.route(f"{config.image_route}/caption/", methods=['GET'])
def _caption_input():
    if request.args:
        return redirect(f"{config.image_route}/caption/{request.args['key']}", code=302)
    return render_template("input.html", type="caption", title="Captioning")





