from http import HTTPStatus

from flask import redirect, render_template, abort, flash

from . import app
from .forms import LinkForm
from .models import URLMap
from yacut.exceptions import ItemAlreadyExistsError, RandomError


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(
            form.original_link.data,
            form.custom_id.data,
            flag=True
        )
    except (ItemAlreadyExistsError, RandomError) as e:
        flash(str(e))
        return render_template('index.html', form=form)

    return render_template(
        'index.html',
        form=form,
        short_url=url_map.get_short_url()
    )


@app.route('/<string:short>')
def redirect_view(short):
    url_map = URLMap.get(short)
    if url_map:
        return redirect(url_map.original)
    return abort(HTTPStatus.NOT_FOUND)
