from flask import render_template, jsonify

from yacut import app, db
from settings import HTTP_NOT_FOUND, HTTP_BAD_REQUEST, HTTP_SERVER_ERROR


class APINotFound(Exception):
    status_code = HTTP_NOT_FOUND

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


class InvalidAPIUsage(Exception):
    status_code = HTTP_BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(APINotFound)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTP_NOT_FOUND)
def page_not_found(error):
    return render_template('error.html'), HTTP_NOT_FOUND


@app.errorhandler(HTTP_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html'), HTTP_SERVER_ERROR
