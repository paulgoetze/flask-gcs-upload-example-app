from http import HTTPStatus

from flask import jsonify
from marshmallow_jsonapi import fields
from marshmallow import Schema
from werkzeug.exceptions import default_exceptions, HTTPException


class ErrorSchema(Schema):
    code = fields.Int(required=True)
    detail = fields.Str(required=True, attribute='description')

    class Meta:
        type_ = 'error'
        strict = True


def register_error_handlers(app):
    """ Register error handlers for the given app """

    for code in default_exceptions:
        app.register_error_handler(code, json_error)


def json_error(error):
    """Generate a json response from an exception"""

    errors = [ErrorSchema().dump(error)]
    response = jsonify(errors=errors)

    code = status_code(error)
    response.status_code = code

    return response


def status_code(error):
    """Return the errors status code"""

    if isinstance(error, HTTPException):
        return error.code
    else:
        return HTTPStatus.INTERNAL_SERVER_ERROR
