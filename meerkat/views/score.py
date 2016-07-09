from flask import Blueprint
from flask import render_template

from meerkat.db import DataAccess

page = Blueprint('score', __name__)


@page.route('/score/')
def list_ranks():
    links = []
    for package, times in DataAccess.get_download_range():
        links.append(dict(file=package, times=int(times)))
    return render_template('score.html', links=links)
