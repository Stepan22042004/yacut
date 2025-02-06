from flask import redirect, render_template, abort, flash
from http import HTTPStatus

from . import app
from .forms import LinkForm
from .models import URLMap

EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
NOT_VALID = 'Указано недопустимое имя для короткой ссылки'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    url_map = URLMap.create_short(
        form.original_link.data,
        form.custom_id.data
    )
    if url_map[0] is None:
        if URLMap.get(form.custom_id.data):
            flash(EXISTS)
        else:
            flash(NOT_VALID)
    flash('Ваша новая ссылка готова:')
    return render_template('index.html', form=form, short_url=url_map[1])


@app.route('/<string:short>')
def redirect_view(short):
    url = URLMap.get(short)
    if url:
        return redirect(url)
    return abort(HTTPStatus.NOT_FOUND)
