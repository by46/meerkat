import string

from flask import Blueprint
from flask import abort
from flask import redirect
from flask import render_template

from meerkat import app
from meerkat import utils

page = Blueprint('simple', __name__)


@page.route('/simple/')
def simple_index():
    conn = app.config['CONN']
    links = conn.smembers(app.config['SIMPLES'])
    links = sorted(links, key=string.lower)
    return render_template('simple.html', links=links)


@page.route('/simple/<prefix>/')
def simple(prefix=''):
    conn = app.config['CONN']
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
