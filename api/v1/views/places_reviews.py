#!/usr/bin/python3
"""RESTFul api for Review objects"""

from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, make_response, abort, request


@app_views.route('/places/<int:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all(place_id):
    """retrive all"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<int:review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """get review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<int:review_id>', methods=['DELETE'],
                 stict_slashes=False)
def del_review(review_id):
    """delete review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    review.save()
    return jsonify({}), 200


@app_views.route('/places/<int:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create an instance"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'text' not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    review = request.get_json()
    review['palce_id'] = place_id
    user = storage.get(User, review['user_id'])
    if user is None:
        abort(404)
    obj = Review(**review)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ updates by id """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())