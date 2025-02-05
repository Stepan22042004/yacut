from flask import redirect, render_template, url_for, abort, flash

from . import app, db
from .forms import LinkForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    message = None
    if form.validate_on_submit():
        if not form.custom_id.data:
            short_link = URLMap.get_unique_short_id()
            message = url_for('index_view', _external=True) + short_link
            flash('Ваша новая ссылка готова:')
            urlmap = URLMap(
                original=form.original_link.data,
                short=short_link
            )
            db.session.add(urlmap)
        else:
            if URLMap.query.filter_by(short=form.custom_id.data).first():
                flash('Предложенный вариант короткой ссылки уже существует.')
            else:
                message = url_for(
                    'index_view',
                    _external=True
                ) + form.custom_id.data
                flash('Ваша новая ссылка готова:')
                urlmap = URLMap(
                    original=form.original_link.data,
                    short=form.custom_id.data
                )
                db.session.add(urlmap)
    db.session.commit()

    return render_template('index.html', form=form, short_url=message)


@app.route('/<string:short_url>')
def redirect_view(short_url):
    long_url = URLMap.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.original)
    return abort(404)
