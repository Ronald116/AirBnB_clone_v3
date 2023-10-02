#!/usr/bin/python3
"""RESTFul api actions for Amenity objects"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all():
    """retrieve all Amenity objects"""
    all_amenities = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(all_amenities)


@app_views.route('/amenities/<int:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """get amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<int:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """delete an instance"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    amenity.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """create an instance"""
    if not request.json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    am = request.json()
    obj = Amenity(**am)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<int:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update an instance"""
    if not request.json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for k, v in request.json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict())
   
    
