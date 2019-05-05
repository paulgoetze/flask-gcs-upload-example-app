from http import HTTPStatus

from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError
from webargs import fields
from webargs.flaskparser import use_args

from my_app import db
from .models import User, UserSchema

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/')
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
            return jsonify(error='not found'), HTTPStatus.NOT_FOUND
    except ValueError as error:
        return jsonify(error=str(error)), HTTPStatus.NOT_FOUND


@users.route('/', methods=['POST'])
@use_args({'email': fields.Str(required=True)})
def create_user(args):
    """Create a new user"""

    email = args.get('email')
    user = User(email=email)

    try:
        db.session.add(user)
        db.session.commit()
        data = UserSchema().dump(user).data
        return jsonify(data)
    except IntegrityError:
        db.session.rollback()
        db.session.close()
        return jsonify(error='user already exists'), HTTPStatus.BAD_REQUEST


@users.route('/', methods=['PUT'])
@use_args({
    'user_id': fields.Int(required=True, location='view_args'),
    'email': fields.Str(required=True)
})
def update(args):
    """Update a user"""

    user = User.query.get(args.get('user_id'))

    if not user:
        jsonify(error='not found'), HTTPStatus.NOT_FOUND

    user.email = args.get('email')
    db.session.add(user)
    db.session.commit()

    data = UserSchema().dump(user).data
    return jsonify(data)


@users.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""

    user = User.query.get(user_id)

    if not user:
        jsonify(error='not found'), HTTPStatus.NOT_FOUND

    db.session.remove(user)
    db.session.commit()

    return jsonify(), HTTPStatus.NO_CONTENT
