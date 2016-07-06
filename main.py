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

conn = redis.Redis(host='scpodb02')

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
    key = 'packages:{0}'.format(prefix)
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
        package_key = 'package:{0}'.format(package)
        info = conn.hgetall(package_key)
        href = '/packages/{0}#md5={1}'.format(package, info.get('md5'))
        links.append(dict(file=package, href=href))

    return render_template('packages.html', links=links)


@app.route('/packages/<filename>')
def download(filename):
    key = 'package:{0}'.format(filename)
    if conn.exists(key):
        # TODO(benjamin): add statistic info
        url = 'http://{host}/{group}/{type}/{filename}'.format(host=config.DFIS_HOST, group=config.DFIS_GROUP,
                                                               type=config.DFIS_TYPE,
                                                               filename=filename)
        return redirect(url)

    abort(404)


def file_upload():
    package = Upload._make(request.files.get(f, None) for f in ('content', 'gpg_signature'))
    if not package.pkg:
        abort(400)

    if package.sig and '{0}.asc'.format(package.pkg.raw_filename) != package.sig.raw_filename:
        abort(400)

    for f in package:
        if not f:
            continue
        # upload package to dfis
        filename = f.filename
        if not utils.is_valid_pkg_filename(filename):
            # TODO(benjamin): add error description
            abort(400)

        pkg = utils.guess_pkgname_and_version(filename)
        if pkg is None:
            # TODO(benjamin): add error description
            abort(400)

        content = f.stream.read()
        md5 = hashlib.md5(content).hexdigest()
        client = cabinet.Cabinet(host=config.DFIS_HOST)
        app.logger.info('upload package to dfis %s %s %s %s', config.DFIS_HOST, config.DFIS_GROUP, config.DFIS_TYPE,
                        filename)
        result = client.upload(StringIO(content), config.DFIS_GROUP, config.DFIS_TYPE, 'UPDATE', filename)
        if result == httplib.OK:
            pkg_name, version = pkg
            url = client.make_url(config.DFIS_GROUP, config.DFIS_TYPE, filename)
            conn.sadd(config.PACKAGES, filename)
            conn.sadd(config.SIMPLES, pkg_name)
            key = 'packages:{0}'.format(pkg_name)
            conn.sadd(key, filename)
            key = 'package:{0}'.format(filename)
            info = dict(md5=md5, url=url, timestamp=time.time())
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
