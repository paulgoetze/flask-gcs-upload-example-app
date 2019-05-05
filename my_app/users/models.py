from depot.fields.sqlalchemy import UploadedFileField
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from my_app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    avatar = db.Column(UploadedFileField())

    def __repr__(self):
        return '<User(email={self.email!r})>'.format(self=self)


class UserSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Str(required=True)
    avatar = fields.Function(lambda user: user.avatar.url)

    class Meta:
        type_ = 'users'
        self_view = 'users.get_user'
        self_view_many = 'users.get_users'
        self_view_kwargs = {'user_id': '<id>'}
        strict = True
