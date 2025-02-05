import string

from flask import jsonify, request

from . import app
from .models import URLMap
from yacut import db


CHARACTERS = (string.ascii_uppercase +
              string.ascii_lowercase + string.digits)


@app.route('/api/id/', methods=['POST'])
def create_short():
    if not request.data:
        return jsonify({'message': 'Отсутствует тело запроса'}), 400
    data = request.get_json()

    if 'url' not in data:
        return jsonify(
            {'message': '\"url\" является обязательным полем!'}
        ), 400

    if 'custom_id' in data and URLMap.query.filter_by(
        short=data['custom_id']
    ).first():
        return jsonify(
            {'message': 'Предложенный вариант короткой ссылки уже существует.'}
        ), 400

    if 'custom_id' in data and (len(data['custom_id']) > 16 or
                                any(c not in CHARACTERS for c
                                    in data['custom_id'])):
        return jsonify(
            {'message': 'Указано недопустимое имя для короткой ссылки'}
        ), 400

    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap:
        return jsonify({'url': urlmap.original}), 200
    return jsonify({'message': 'Указанный id не найден'}), 404
