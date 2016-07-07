import hashlib
import httplib
import time
from cStringIO import StringIO

from flask import abort
from flask import render_template
from flask import request
from flask import Blueprint

from meerkat import app
from meerkat import cabinet
from meerkat import utils


page = Blueprint('index', __name__)


@page.route('/', methods=['GET'])
def index():
    conn = app.config['CONN']
    total_packages = conn.scard(app.config['PACKAGES'])
    return render_template('index.html', total_packages=total_packages)


@page.route('/', methods=['POST'])
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


def file_upload():
    conn = app.config['CONN']
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
    client = cabinet.Cabinet(host=app.config['DFIS_HOST'])
    app.logger.info('upload package to dfis %s %s %s %s', app.config['DFIS_HOST'], app.config['DFIS_GROUP'],
                    app.config['DFIS_TYPE'],
                    filename)
    result = client.upload(StringIO(content), app.config['DFIS_GROUP'], app.config['DFIS_TYPE'], 'UPDATE', filename)
    if result != httplib.OK:
        app.logger.error('upload package error: status code %s', result)
        abort(500)

    pkg_name, version = name_and_version
    safe_filename = filename.lower()
    url = client.make_url(app.config['DFIS_GROUP'], app.config['DFIS_TYPE'], filename)
    conn.sadd(app.config['PACKAGES'], filename)
    conn.sadd(app.config['SIMPLES'], pkg_name)
    _, pkg_name = utils.normalize_pkg_name(pkg_name)
    key = 'packages:{0}'.format(pkg_name)
    conn.sadd(key, filename)
    key = 'package:{0}'.format(safe_filename)
    info = dict(md5=md5, url=url, timestamp=time.time(), filename=filename)
    conn.hmset(key, info)
