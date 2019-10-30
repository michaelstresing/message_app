from flask import Blueprint, jsonify, request
from datetime import datetime

from application import db
from application.models import User

UserAPI = Blueprint('user_api', __name__)


@UserAPI.route('/', methods=['POST'])
def create_user():
    """API request to Create a new User"""

    try:
        user = User.from_user(request.json)
    except KeyError as e:
        return jsonify(f'Missing key: {e.args[0]}'), 400

    db.session.add(user)
    db.session.commit()
    return jsonify(), 200
    

@UserAPI.route('/<string:username>')
def get_user(username):
    """API request to Get a User by username"""

    user = User.query.filter(User.username == username).first()
    if user is None:
        return 'User not found', 404
    return jsonify(user.to_user()), 200


@UserAPI.route('/', methods=['GET'])
def get_all():
    user = User.query.all()
    jsonuser = [usr.to_user() for usr in user]
    return jsonify(jsonuser), 200


@UserAPI.route('<string:username>', methods=['PUT'])
def edit_user(username):

    User.query.filter(User.username == username).update(request.json)
    user = User.query.filter(User.username == username).first_or_404()
    user.dateupdated = datetime.utcnow()
    db.session.commit()
    return jsonify(user.to_user()), 200


@UserAPI.route('/<string:username>', methods=['DELETE'])
def delete_user(username):

    user = User.query.filter(User.username == username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return jsonify(), 200
