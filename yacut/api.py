from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidRequestError
from .models import Story


@app.route('/api/stories/', methods=['GET'])
def get_stories():
    stories = Story.query.all()
    return jsonify(
        [
            story.to_dict() for story in stories
        ]
    )


@app.route('/api/add_story/', methods=['POST'])
def add_story():
    data = request.get_json()
    if 'title' not in data or 'text' not in data:
        raise InvalidRequestError('В запросе отсутствуют обязательные поля')
    story = Story()
    story.from_dict(data)
    db.session.add(story)
    db.session.commit()
    return jsonify(story.to_dict())