from http import HTTPStatus

from flask import jsonify, request

from . import app
from .models import URLMap
from yacut.error_handlers import InvalidAPIUsage
from yacut.exceptions import (ItemAlreadyExistsError, RandomError,
                              IncorrectShortError, TooLongError)

REQUIRED = '"url" является обязательным полем!'
NO_BODY = 'Отсутствует тело запроса'
NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short():
    if not request.data:
        raise InvalidAPIUsage(NO_BODY)
    data = request.get_json()

    if 'url' not in data:
        raise InvalidAPIUsage(REQUIRED)
    try:
        url_map = URLMap.create(data['url'], data.get('custom_id'))
    except (ItemAlreadyExistsError, IncorrectShortError,
            TooLongError, RandomError) as e:
        raise InvalidAPIUsage(str(e))

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original(short):
    url_map = URLMap.get(short)
    if url_map:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage(message=NOT_FOUND, status_code=HTTPStatus.NOT_FOUND)
