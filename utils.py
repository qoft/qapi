from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from currency import convert_currency


def view(json):
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify(json)
    return render_template(
        'view.html',
        error=json["error"],
        title=str(json["type"]).capitalize(),
        balance=json["balance"] if not json["error"] else 0,
        message=json["message"] if json["error"] else None,
    )


def convert(amount, from_currency, to_currency):
    return convert_currency(
        from_=from_currency,
        to=to_currency,
        amount=float(amount),
    )


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
