from datetime import datetime
import random
import re

from flask import url_for

from yacut import db
from settings import (MAX_SHORT_LEN, MAX_GENERATED_LEN, CHARACTERS,
                      MAX_ORIGINAL_LEN, ITERATIONS, REGEX, REDIRECT_VIEW)
from yacut.exceptions import (ItemAlreadyExistsError,
                              IncorrectShortError, TooLongError)

EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(MAX_SHORT_LEN), default=None, unique=True)
    original = db.Column(db.String(MAX_ORIGINAL_LEN), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_short_url(),
        )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    def get_short_url(self):
        return url_for(REDIRECT_VIEW, short=self.short, _external=True)

    @staticmethod
    def get_unique_short_id():
        for i in range(ITERATIONS):
            short = ''.join(random.choices(CHARACTERS, k=MAX_GENERATED_LEN))
            if URLMap.get(short) is None:
                return short
        return ''.join(random.choices(CHARACTERS, k=MAX_GENERATED_LEN))

    @staticmethod
    def create(url, short=None, form=False):
        if not short:
            short = URLMap.get_unique_short_id()
        else:
            if not form and ((len(short) > MAX_SHORT_LEN or
               re.fullmatch(REGEX, short) is None)):
                raise IncorrectShortError
            if URLMap.get(short):
                raise ItemAlreadyExistsError
        if not form and len(url) > MAX_ORIGINAL_LEN:
            raise TooLongError
        url_map = URLMap(original=url, short=short)
        #message_in_html = url_map.get_short_url()
        db.session.add(url_map)
        db.session.commit()
        return url_map
