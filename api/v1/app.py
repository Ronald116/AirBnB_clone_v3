#!/usr/bin/python3
"""This module contains the application"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask import Blueprint
from os import getenv


app = Flask(__name__)
app.register_app(app_views)


@app.teardown_appcontext
def close_db(obj):
    """calls methods close"""
    storage.close()


@app.errohandler(404)
def error404(error):
    """returns a JSON-formatted 404 status code"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host, int(port), threaded=True)
