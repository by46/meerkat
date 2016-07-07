import string

from flask import abort
from flask import redirect
from flask import render_template

from meerkat import app

conn = app.config['CONN']


@app.route('/packages/')
def list_packages():
    packages = conn.smembers(app.config['PACKAGES'])
    packages = sorted(packages, key=string.lower)
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
        url = 'http://{host}/{group}/{type}/{filename}'.format(host=app.config['DFIS_HOST'],
                                                               group=app.config['DFIS_GROUP'],
                                                               type=app.config['DFIS_TYPE'],
                                                               filename=filename)
        return redirect(url)

    abort(404)
