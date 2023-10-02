#!/usr/bin/python3
"""handles RESTFul api actions for User objects"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, make_response, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all():
    """get all instances"""
    all_users = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(all_users)


@app_views.route('/users/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get an instance by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<int:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """delete an instance"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    user.save()
    return jsonify({}), 200


@app_views.route('/user', methods=['POST'], strict_slashes=False)
def post_user():
    """create a new instance"""
    if not request.json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = request.json()
    user_obj = User(**user)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def post_user(user_id):
    """update an instance  """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())