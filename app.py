import utils
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os, importlib, sys

app = Flask(__name__)
app.static_folder = "static"
for route_folder in os.listdir("routes"):
    if route_folder.startswith("__"):
        continue
    for route_file in os.listdir(f"routes/{route_folder}"):
        if route_file.startswith("__"):
            continue
        if route_file.endswith(".py"):
            lib = importlib.import_module(f"routes.{route_folder}.{route_file[:-3]}")
            app.register_blueprint(lib.blueprint)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'), code=302)


@app.route("/")
def index():
    routes = dict()
    for route_folder in os.listdir("routes"):
        if route_folder.startswith("__"):
            continue
        routes.update({route_folder: []})

    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and utils.has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if url != "/":
                routes[url.split("/")[1]].append((url, rule.endpoint, ("<" and ">" in rule.rule)))

    return render_template("index.html", routes=routes)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
