from flask import Blueprint
from flask import render_template

from meerkat.db import DataAccess

page = Blueprint('downloadtimes', __name__)


@page.route('/downloadtimes/')
def list_ranks():
    links = []
    for package, times in DataAccess.get_download_range():
        links.append(dict(file=package, times=int(times)))
    return render_template('downloadtimes.html', links=links)
