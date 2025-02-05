from datetime import datetime
import random

from flask import url_for, flash

from yacut import db
from yacut.error_handlers import InvalidAPIUsage, APINotFound
from settings import (MAX_SHORT_LEN, MAX_GENERATED_LEN, CHARACTERS,
                      MAX_ORIGINAL_LEN, INDEX, ITERATIONS)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(MAX_SHORT_LEN), default=None, unique=True)
    original = db.Column(db.String(MAX_ORIGINAL_LEN), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(INDEX, _external=True) + self.short,
        )

    @staticmethod
    def get_unique_short_id():
        for i in range(ITERATIONS):
            short = ''.join(random.choices(CHARACTERS, k=MAX_GENERATED_LEN))
            if URLMap.query.filter_by(short=short).first() is None:
                break
        return short

    @staticmethod
    def create_short(url, short=None, api=True):
        urlmap = None
        if short is not None:
            if URLMap.query.filter_by(
                short=short
            ).first():
                if api is True:
                    raise InvalidAPIUsage(
                        'Предложенный вариант короткой ссылки уже существует.'
                    )
                else:
                    flash(
                        'Предложенный вариант короткой ссылки уже существует.'
                    )
                    return urlmap
            if (len(short) > MAX_SHORT_LEN or
                    any(c not in CHARACTERS for c in short)):
                if api is True:
                    raise InvalidAPIUsage(
                        'Указано недопустимое имя для короткой ссылки'
                    )
                else:
                    flash('Указано недопустимое имя для короткой ссылки')
                    return urlmap
        else:
            short = URLMap.get_unique_short_id()

        urlmap = URLMap(original=url, short=short)
        db.session.add(urlmap)
        db.session.commit()
        if api is True:
            return urlmap
        else:
            flash('Ваша новая ссылка готова:')
            return urlmap

    @staticmethod
    def get_url_by_id(short, api=True):
        urlmap = URLMap.query.filter_by(short=short).first()
        if urlmap:
            return urlmap.original
        if api is True:
            raise APINotFound('Указанный id не найден')
        else:
            return None

    def get_short_url(self):
        return url_for(INDEX, _external=True) + self.short
