from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import MAX_SHORT_LEN, MAX_ORIGINAL_LEN, REGEX

REQUIRED = 'Обязательное поле'
YOUR_VARIANT = 'Ваш вариант короткой ссылки'
SUBMIT = 'Создать'
LONG = 'Длинная ссылка'


class LinkForm(FlaskForm):
    original_link = StringField(
        LONG,
        validators=[
            Length(1, MAX_ORIGINAL_LEN),
            DataRequired(REQUIRED)
        ]
    )
    custom_id = StringField(
        YOUR_VARIANT,
        validators=[
            Optional(),
            Length(1, MAX_SHORT_LEN),
            Regexp(REGEX)
        ]
    )
    submit = SubmitField(SUBMIT)
