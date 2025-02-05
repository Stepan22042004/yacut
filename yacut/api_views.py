from flask import jsonify, request

from . import app
from .models import URLMap
from yacut.error_handlers import InvalidAPIUsage
from settings import HTTP_OK


@app.route('/api/id/', methods=['POST'])
def create_short():
    if not request.data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = request.get_json()

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if 'custom_id' in data:
        urlmap = URLMap.create_short(data['url'], data['custom_id'])
    else:
        urlmap = URLMap.create_short(data['url'])

    return jsonify(urlmap.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original(short):
    url = URLMap.get_url_by_id(short)
    return jsonify({'url': url}), HTTP_OK
