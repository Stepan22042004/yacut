from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, Regexp


REQUIRED = 'Обязательное поле'
YOUR_VARIANT = 'Ваш вариант короткой ссылки'
SUBMIT = 'Создать'


class LinkForm(FlaskForm):
    original_link = TextAreaField(
        'Длинная ссылка',
        validators=[
            DataRequired(REQUIRED)
        ]
    )
    custom_id = StringField(
        YOUR_VARIANT,
        validators=[
            Optional(),
            Length(1, 16),
            Regexp(r'^[a-zA-Z0-9_]+$')
        ]
    )
    submit = SubmitField(SUBMIT)
