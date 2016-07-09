from flask import Blueprint
from flask import render_template

from meerkat import app

page = Blueprint('downloadtimes', __name__)


@page.route('/downloadtimes/')
def list_ranks():
    conn = app.config['CONN']
    ranks = conn.zrevrange('packages:downloadtimes', 0, -1, withscores=True)
    links = []
    for item in ranks:
        links.append(dict(file=item[0], times=int(item[1])))
    return render_template('downloadtimes.html', links=links)
