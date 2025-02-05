from datetime import datetime
import random
import string

from flask import url_for

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(16), default=None, unique=True)
    original = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        if self.short is None:
            setattr(self, 'short', self.get_unique_short_id())
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short,
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        if data.get('custom_id') is not None:
            setattr(self, 'short', data['custom_id'])

    @staticmethod
    def get_unique_short_id():
        characters = (string.ascii_uppercase +
                      string.ascii_lowercase + string.digits)
        short_link = ''.join(random.choice(characters) for _ in range(6))
        while URLMap.query.filter_by(short=short_link).first() is not None:
            short_link = ''.join(random.choice(characters) for _ in range(6))
        return short_link
