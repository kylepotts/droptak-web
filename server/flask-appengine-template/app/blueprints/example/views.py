from flask import Blueprint, render_template


bp = Blueprint('example', __name__, url_prefix = '/example')


@bp.route('/')
def home():
    return render_template('example/home.html')