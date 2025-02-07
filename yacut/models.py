from datetime import datetime
import random
import re

from flask import url_for

from yacut import db
from settings import (MAX_SHORT_LEN, MAX_GENERATED_LEN, CHARACTERS,
                      MAX_ORIGINAL_LEN, ITERATIONS, REGEX, REDIRECT_VIEW)
from yacut.exceptions import (ItemAlreadyExistsError,
                              IncorrectShortError,
                              TooLongError, RandomError)

EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
NOT_VALID = 'Указано недопустимое имя для короткой ссылки'
TOO_LONG = 'Слишком длинный url'
RANDOM = 'Не удалось сгенерировать уникальную короткую ссылку'


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
        raise RandomError(RANDOM)

    @staticmethod
    def create(url, short=None, flag=False):
        if not short:
            short = URLMap.get_unique_short_id()
        else:
            if not flag and ((len(short) > MAX_SHORT_LEN or
               re.fullmatch(REGEX, short) is None)):
                raise IncorrectShortError(NOT_VALID)
            if URLMap.get(short):
                raise ItemAlreadyExistsError(EXISTS)
        if not flag and len(url) > MAX_ORIGINAL_LEN:
            raise TooLongError(TOO_LONG)
        url_map = URLMap(original=url, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
