import httplib
import string

from flask import Blueprint
from flask import Response
from flask import redirect
from flask import render_template

from meerkat import app
from meerkat.db import DataAccess

page = Blueprint('package', __name__)


@page.route('/packages/')
def list_packages():
    packages = DataAccess.get_packages()
    packages = sorted(packages, key=string.lower)
    links = []
    for package in packages:
        info = DataAccess.get_package(package)
        href = '/packages/{0}#md5={1}'.format(package, info.get('md5'))
        links.append(dict(file=package, href=href))
    return render_template('packages.html', links=links)


@page.route('/packages/<filename>')
def download(filename):
    filename = filename.lower()
    if DataAccess.has_package_file(filename):
        url = 'http://{host}/{group}/{type}/pypi/{filename}'.format(host=app.config['DFIS_DOWNLOAD'],
                                                                    group=app.config['DFIS_GROUP'],
                                                                    type=app.config['DFIS_TYPE'],
                                                                    filename=filename)
        DataAccess.add_download_score(filename)
        return redirect(url)

    return Response('package not found', status=httplib.NOT_FOUND)
