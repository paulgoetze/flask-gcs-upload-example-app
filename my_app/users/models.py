from depot.fields.filters.thumbnails import WithThumbnailFilter
from depot.fields.sqlalchemy import UploadedFileField
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from my_app import db
from my_app.config.depot import AVATAR_DEPOT, BACKGROUND_DEPOT


class User(db.Model):
    __tablename__ = 'users'

    COVER_SIZE_SMALL = (32, 32)
    COVER_SIZE_MEDIUM = (128, 128)

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    avatar = db.Column(UploadedFileField(
        upload_storage=AVATAR_DEPOT,
        filters=[
            WithThumbnailFilter(size=COVER_SIZE_SMALL),
            WithThumbnailFilter(size=COVER_SIZE_MEDIUM)
        ]
    ))
    profile_background = db.Column(UploadedFileField(upload_storage=BACKGROUND_DEPOT))

    def __repr__(self):
        return '<User(email={self.email!r})>'.format(self=self)


class UserSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Str(required=True)
    avatar = fields.Function(lambda user: user.avatar and user.avatar.url)
    avatar_small = fields.Function(lambda user: user.avatar and user.avatar.thumb_32x32_url)
    avatar_medium = fields.Function(lambda user: user.avatar and user.avatar.thumb_128x128_url)
    profile_background = fields.Function(lambda user: user.profile_background and user.profile_background.url)

    class Meta:
        type_ = 'users'
        self_view = 'users.get_user'
        self_view_many = 'users.get_users'
        self_view_kwargs = {'user_id': '<id>'}
        strict = True
