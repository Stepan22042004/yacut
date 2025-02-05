from flask import redirect, render_template, abort

from . import app
from .forms import LinkForm
from .models import URLMap
from settings import HTTP_NOT_FOUND


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    message_in_html = None
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    if not form.custom_id.data:
        urlmap = URLMap.create_short(form.original_link.data, api=False)
    else:
        urlmap = URLMap.create_short(
            form.original_link.data,
            form.custom_id.data,
            api=False
        )
    if urlmap is not None:
        message_in_html = urlmap.get_short_url()
    return render_template('index.html', form=form, short=message_in_html)


@app.route('/<string:short>')
def redirect_view(short):
    url = URLMap.get_url_by_id(short, api=False)
    if url:
        return redirect(url)
    return abort(HTTP_NOT_FOUND)
