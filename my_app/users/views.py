from http import HTTPStatus

from flask import Blueprint, jsonify, abort, request
from sqlalchemy.exc import IntegrityError
from webargs import fields
from webargs.flaskparser import use_args

from my_app import db
from .models import User, UserSchema

users = Blueprint('users', __name__, url_prefix='/users')

IMAGE_MIME_TYPES = {
    'image/jpeg',
    'image/png'
}


@users.route('')
def get_users():
    """List all users"""

    records = User.query.all()
    data = UserSchema().dump(records, many=True)
    return jsonify(data), HTTPStatus.OK


@users.route('/<user_id>')
def get_user(user_id):
    """Get a user"""

    try:
        user = User.query.get(int(user_id))

        if user:
            data = UserSchema().dump(user)
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
        data = UserSchema().dump(user)
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

    data = UserSchema().dump(user)
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


@users.route('/<user_id>/avatar', methods=['POST'])
def upload_avatar(user_id):
    """Upload an avatar image for a user"""

    user = User.query.get(user_id)

    # check whether the user is available:
    if not user:
        abort(HTTPStatus.NOT_FOUND)

    # check whether an avatar file was provided:
    files = request.files
    avatar = files.get('avatar')

    if not avatar:
        abort(HTTPStatus.BAD_REQUEST, 'no image file provided')

    # check whether the provided avatar file has the right MIME type:
    mime_types = set(avatar.content_type.split(','))
    is_mime_type_allowed = any(mime_types.intersection(IMAGE_MIME_TYPES))

    if not is_mime_type_allowed:
        abort(HTTPStatus.BAD_REQUEST, f'allowed mimetypes are {IMAGE_MIME_TYPES}')

    # if all checks passed, upload the avatar:
    user.avatar = avatar
    db.session.commit()
    data = UserSchema().dump(user)

    return jsonify(data), HTTPStatus.CREATED
