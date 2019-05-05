from http import HTTPStatus

from flask import Blueprint, jsonify, abort
from sqlalchemy.exc import IntegrityError
from webargs import fields
from webargs.flaskparser import use_args

from my_app import db
from .models import User, UserSchema

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('')
def get_users():
    """List all users"""

    records = User.query.all()
    data = UserSchema().dump(records, many=True).data
    return jsonify(data), HTTPStatus.OK


@users.route('/<user_id>')
def get_user(user_id):
    """Get a user"""

    try:
        user = User.query.get(int(user_id))

        if user:
            data = UserSchema().dump(user).data
            return jsonify(data), HTTPStatus.OK
        else:
            return abort(HTTPStatus.NOT_FOUND)
    except ValueError:
        return abort(HTTPStatus.NOT_FOUND)


@users.route('', methods=['POST'])
@use_args({'email': fields.Str(required=True)})
def create_user(args):
    """Create a new user"""

    email = args.get('email')
    user = User(email=email)
    db.session.add(user)

    try:
        db.session.commit()
        data = UserSchema().dump(user).data
        return jsonify(data), HTTPStatus.CREATED
    except IntegrityError:
        db.session.rollback()
        return abort(HTTPStatus.BAD_REQUEST, 'user already exists')


@users.route('/<user_id>', methods=['PUT'])
@use_args({'email': fields.Str(required=True)})
def update(args, user_id):
    """Update a user"""

    user = User.query.get(user_id)

    if not user:
        abort(HTTPStatus.NOT_FOUND)

    user.email = args.get('email')
    db.session.commit()

    data = UserSchema().dump(user).data
    return jsonify(data)


@users.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""

    user = User.query.get(user_id)

    if not user:
        return abort(HTTPStatus.NOT_FOUND)

    db.session.delete(user)
    db.session.commit()

    return jsonify(), HTTPStatus.NO_CONTENT
