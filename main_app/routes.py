from flask import Blueprint, current_app, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    # print("DEBUG test")
    return render_template('index.html')
