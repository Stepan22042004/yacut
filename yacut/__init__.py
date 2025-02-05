import pathlib
import os

from flask import Flask, redirect, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = 'SUPER SECRET KEY'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import api_views, views, error_handlers