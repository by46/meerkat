from __future__ import absolute_import

import hashlib
import httplib
import time
from cStringIO import StringIO
from collections import namedtuple

import redis
from flask import Flask
from flask import abort
from flask import render_template
from flask import request

import cabinet
import utils

app = Flask(__name__)

conn = redis.Redis(host='scpodb02')
DFIS_HOST = 'scmesos04'
DFIS_GROUP = 'test_ttl'
DFIS_TYPE = 'carl'
SIMPLES = 'simples'
PACKAGES = 'packages'

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
    links = conn.smembers(SIMPLES)
    return render_template('simple.html', links=links)


@app.route('/simple/<prefix>/')
def simple(prefix=''):
    key = 'packages:{0}'.format(prefix)
    packages = conn.smembers(key)
    links = []
    for package in packages:
        package_key = 'package:{0}'.format(package)
        info = conn.hgetall(package_key)
        href = '{0}#md5={1}'.format(info.get('url'), info.get('md5'))
        links.append(dict(file=package, href=href))

    return render_template('simple_detail.html', links=links, prefix=prefix)


@app.route('/packages/')
def list_packages():
    packages = conn.smembers(PACKAGES)
    links = []
    for package in packages:
        package_key = 'package:{0}'.format(package)
        info = conn.hgetall(package_key)
        href = '{0}#md5={1}'.format(info.get('url'), info.get('md5'))
        links.append(dict(file=package, href=href))

    return render_template('packages.html', links=links)


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
        client = cabinet.Cabinet(host=DFIS_HOST)
        result = client.upload(StringIO(content), DFIS_GROUP, DFIS_TYPE, 'UPDATE', filename)
        if result == httplib.OK:
            # TODO(benjamin): process package
            pkg_name, version = pkg
            url = client.make_url(DFIS_GROUP, DFIS_TYPE, filename)
            conn.sadd(PACKAGES, filename)
            conn.sadd(SIMPLES, pkg_name)
            key = 'packages:{0}'.format(pkg_name)
            conn.sadd(key, filename)
            key = 'package:{0}'.format(filename)
            info = dict(md5=md5, url=url, timestamp=time.time())
            conn.hmset(key, info)


if __name__ == '__main__':
    from gevent.wsgi import WSGIServer

    WSGIServer(('', 8889), application=app).serve_forever()
