from flask import jsonify, request
from http import HTTPStatus

from . import app
from .models import URLMap
from yacut.error_handlers import InvalidAPIUsage

REQUIRED = '"url" является обязательным полем!'
NO_BODY = 'Отсутствует тело запроса'
EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
NOT_VALID = 'Указано недопустимое имя для короткой ссылки'
NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short():
    if not request.data:
        raise InvalidAPIUsage(NO_BODY)
    data = request.get_json()

    if 'url' not in data:
        raise InvalidAPIUsage(REQUIRED)

    url_map = URLMap.create_short(data['url'], data.get('custom_id'))[0]

    if url_map is None:
        if URLMap.get(data['custom_id']):
            raise InvalidAPIUsage(EXISTS)
        else:
            raise InvalidAPIUsage(NOT_VALID)

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original(short):
    url = URLMap.get(short)
    if url:
        return jsonify({'url': url}), HTTPStatus.OK
    raise InvalidAPIUsage(message=NOT_FOUND, status_code=HTTPStatus.NOT_FOUND)
