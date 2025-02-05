from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class LinkForm(FlaskForm):
    original_link = TextAreaField(
        'Длинная ссылка',
        validators=[
            DataRequired('Обязательное поле')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(1, 16),
        ]
    )
    submit = SubmitField('Создать')