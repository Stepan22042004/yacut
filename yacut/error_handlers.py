from . import app

from flask import render_template


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404