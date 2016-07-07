from flask import Blueprint
from flask import render_template

page = Blueprint('portal', __name__, url_prefix='/portal')


@page.route('/')
def index():
    return render_template('portal.html')
