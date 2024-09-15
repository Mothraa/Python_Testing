from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

#TODO : regarder url_for qui est chargé pour le logout => a priori pour pointer sur un path lors de redirection
# TODO : authentification ?
# TODO : CSRF token ? autres aspects sécurité ?

@bp.route('/')
def index():
    return render_template('index.html')
