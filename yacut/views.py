from flask import redirect, render_template, abort, flash
from http import HTTPStatus

from . import app
from .forms import LinkForm
from .models import URLMap
from yacut.exceptions import ItemAlreadyExistsError

EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
NOT_VALID = 'Указано недопустимое имя для короткой ссылки'
NEW = 'Ваша новая ссылка готова:'
TOO_LONG = 'Слишком длинный url'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(
            form.original_link.data,
            form.custom_id.data,
            form=True
        )
    except ItemAlreadyExistsError:
        flash(EXISTS)
        return render_template('index.html', form=form)

    return render_template(
        'index.html',
        form=form,
        short_url=url_map.get_short_url()
    )


@app.route('/<string:short>')
def redirect_view(short):
    url = URLMap.get(short)
    if url:
        return redirect(url.original)
    return abort(HTTPStatus.NOT_FOUND)
