#!/usr/bin/python3
"""contains endpoint route '/status'"""
from flask import jsonify
from flask import Flask
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """returns a jsonify status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "states": storage.count("Storage"),
        "users": storage.count("User")
    })
