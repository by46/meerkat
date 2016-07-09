from __future__ import absolute_import

from flask import Flask

from . import utils

__version__ = '0.0.1'
__author__ = 'benjamin.c.yan'

app = Flask(__name__, instance_relative_config=True)

from meerkat import views

app.register_blueprint(views.portal.page)
app.register_blueprint(views.index.page)
app.register_blueprint(views.simple.page)
app.register_blueprint(views.packages.page)
app.register_blueprint(views.score.page)

app.config.from_object('config.default')
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG_FILE')
app.config['VERSION'] = __version__
