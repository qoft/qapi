from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

import os, importlib

app = Flask(__name__)
app.static_folder = "static"
for route_folder in os.listdir("routes"):
    for route_file in os.listdir(f"routes/{route_folder}"):
        if route_file.endswith(".py"):
            lib = importlib.import_module(f"routes.{route_folder}.{route_file[:-3]}")
            app.register_blueprint(lib.blueprint)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'), code=302)


@app.route("/")
def index():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if url == "/":
                continue
            links.append((url, rule.endpoint))
    print(links)
    return render_template("index.html", links=links)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)





if __name__ == '__main__':
    app.run(debug=True)
