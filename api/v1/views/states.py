#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State

@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_all():
    """get all states"""
    all_states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(all_states)


@app_views.route('/states/<int:state_id>',methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """retrieve a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<int:state_id>', methods=['DELETE'],
                  strict_slashes=False)
def del_state(state_id):
    """delete a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    state.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create():
    """create an instance"""
    if not request.json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    cs = request.json()
    obj = State(**cs)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def post_method(state_id):
    """ post method """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())