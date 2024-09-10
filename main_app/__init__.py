from flask import Flask

from services import load_club_data, load_competition_data

def create_app(config_filename='config.py'):
    app = Flask(__name__)

    # Charge la configuration de l'application depuis config.py
    app.config.from_object(config_filename) 

    # Importe et enregistre les routes et les vues
    with app.app_context():
        from . import routes  # Importer les routes

    # TODO : load json data => comment déclarer ? object data ? flask app.config ?
    # competitions = load_competition_data()
    # clubs = load_club_data()
    return app
