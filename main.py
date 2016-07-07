from __future__ import absolute_import

import hashlib
import httplib
import time
from cStringIO import StringIO
from collections import namedtuple

import redis
from flask import Flask
from flask import abort
from flask import redirect
from flask import render_template
from flask import request

import cabinet
import config
import utils

app = Flask(__name__)

conn = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

Upload = namedtuple('Upload', 'pkg, sig')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def update():
    try:
        action = request.form[':action']
    except KeyError:
        abort(400)

    if action in ('verify', 'submit'):
        pass
    elif action == 'file_upload':
        file_upload()
    return "OK"


@app.route('/simple/')
def simple_index():
    links = conn.smembers(config.SIMPLES)
    return render_template('simple.html', links=links)


@app.route('/simple/<prefix>/')
def simple(prefix=''):
    normalized, prefix = utils.normalize_pkg_name(prefix)
    if normalized:
        return redirect('/simple/{0}/'.format(prefix))

    key = 'packages:{0}'.format(prefix.lower())
    if not conn.exists(key):
        abort(404)

    packages = conn.smembers(key)
    links = []
    for package in packages:
        package_key = 'package:{0}'.format(package)
        info = conn.hgetall(package_key)
        href = '/packages/{0}#md5={1}'.format(package, info.get('md5'))
        links.append(dict(file=package, href=href))

    return render_template('simple_detail.html', links=links, prefix=prefix)


@app.route('/packages/')
def list_packages():
    packages = conn.smembers(config.PACKAGES)
    links = []
    for package in packages:
        package_key = 'package:{0}'.format(package.lower())
        info = conn.hgetall(package_key)
        href = '/packages/{0}#md5={1}'.format(package, info.get('md5'))
        links.append(dict(file=package, href=href))

    return render_template('packages.html', links=links)


@app.route('/packages/<filename>')
def download(filename):
    filename = filename.lower()
    key = 'package:{0}'.format(filename)
    if conn.exists(key):
        # TODO(benjamin): add statistic info
        url = 'http://{host}/{group}/{type}/{filename}'.format(host=config.DFIS_HOST, group=config.DFIS_GROUP,
                                                               type=config.DFIS_TYPE,
                                                               filename=filename)
        return redirect(url)

    abort(404)


def file_upload():
    # TODO(benjamin): process gpg_signature
    package = request.files.get('content', None)
    if not package:
        abort(400)

    filename = package.filename
    if not utils.is_valid_pkg_filename(filename):
        # TODO(benjamin): add error description
        abort(400)

    name_and_version = utils.guess_pkgname_and_version(filename)
    if name_and_version is None:
        # TODO(benjamin): add error description
        abort(400)

    content = package.stream.read()
    md5 = hashlib.md5(content).hexdigest()
    client = cabinet.Cabinet(host=config.DFIS_HOST)
    app.logger.info('upload package to dfis %s %s %s %s', config.DFIS_HOST, config.DFIS_GROUP, config.DFIS_TYPE,
                    filename)
    result = client.upload(StringIO(content), config.DFIS_GROUP, config.DFIS_TYPE, 'UPDATE', filename)
    if result != httplib.OK:
        app.logger.error('upload package error: status code %s', result)
        abort(500)

    pkg_name, version = name_and_version
    safe_filename = filename.lower()
    url = client.make_url(config.DFIS_GROUP, config.DFIS_TYPE, filename)
    conn.sadd(config.PACKAGES, filename)
    conn.sadd(config.SIMPLES, pkg_name)
    _, pkg_name = utils.normalize_pkg_name(pkg_name)
    key = 'packages:{0}'.format(pkg_name)
    conn.sadd(key, filename)
    key = 'package:{0}'.format(safe_filename)
    info = dict(md5=md5, url=url, timestamp=time.time(), filename=filename)
    conn.hmset(key, info)


if __name__ == '__main__':
    from gevent.wsgi import WSGIServer
    import os
    import os.path
    import logging
    from logging.handlers import RotatingFileHandler

    logs = "/var/meerkat/logs"
    if not os.path.exists(logs):
        os.makedirs(logs)

    handler = RotatingFileHandler(os.path.join(logs, 'error.log'), maxBytes=1024 * 1024 * 10, backupCount=10)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    WSGIServer(('', 8080), application=app).serve_forever()
