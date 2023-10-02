#!/usr/bin/python3
"""City objects that handles all default RESTFul api actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<int:state_id>/cities', strict_slashes=False)
def get_all(state_id):
    """retrieves all lists of City objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = [obj.to_dict() for obj in state.cities]
    return jsonify(list_cities)


@app_views.route('/cities/<int:city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """get city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<int:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """delete city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    city.save()
    return jsonify({}), 200


@app_views.route('/states/<int:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """create a new instance"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    pc = request.json()
    obj = City(**pc)
    obj.state_id = state.id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<int:city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """update city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json():
        return make_response(jsonify({'eror': 'Not a JSON'}), 400)
    for key, value in request.json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict())
