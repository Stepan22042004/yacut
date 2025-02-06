from datetime import datetime
import random
import re

from flask import request

from yacut import db
from settings import (MAX_SHORT_LEN, MAX_GENERATED_LEN, CHARACTERS,
                      MAX_ORIGINAL_LEN, ITERATIONS, REGEX)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(MAX_SHORT_LEN), default=None, unique=True)
    original = db.Column(db.String(MAX_ORIGINAL_LEN), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=request.url_root + self.short,
        )

    @staticmethod
    def get(short):
        url_map = URLMap.query.filter_by(short=short).first()
        if url_map:
            return url_map.original
        return None

    def get_short_url(self):
        return request.url_root + self.short

    @staticmethod
    def get_unique_short_id():
        for i in range(ITERATIONS):
            short = ''.join(random.choices(CHARACTERS, k=MAX_GENERATED_LEN))
            if URLMap.get(short) is None:
                return short

    @staticmethod
    def create_short(url, short=None):
        url_map = None
        message_in_html = None
        if short is not None and short != '':
            if URLMap.get(short):
                return url_map, message_in_html
            if (len(short) > MAX_SHORT_LEN or
               re.fullmatch(REGEX, short) is None):
                return url_map, message_in_html
        else:
            short = URLMap.get_unique_short_id()

        url_map = URLMap(original=url, short=short)
        message_in_html = url_map.get_short_url()
        db.session.add(url_map)
        db.session.commit()
        return url_map, message_in_html
