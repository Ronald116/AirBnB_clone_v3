#!/usr/bin/python3
"""contains endpoint route '/status'"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """returns a jsonify status"""
    return jsonify({"status": "OK"})
