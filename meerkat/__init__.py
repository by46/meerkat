from __future__ import absolute_import

import redis
from flask import Flask

from meerkat import cabinet
from . import utils

app = Flask(__name__, instance_relative_config=True)

from meerkat import views

app.register_blueprint(views.portal.page)
app.register_blueprint(views.index.page)
app.register_blueprint(views.simple.page)
app.register_blueprint(views.packages.page)

app.config.from_object('config.default')
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG_FILE')

app.config['CONN'] = conn = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])