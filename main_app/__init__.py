import os
from flask import Flask

from .services import JSONLoader


def create_app(config_filename='config.py'):
    app = Flask(__name__)

    # Chargement de la configuration
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(project_dir, 'config.py')

    app.config.from_pyfile(config_path)
    # print(app.config)
    # print(app.config.get('JSON_CLUBS_PATH'))

    # Importe et enregistre les routes et les vues
    with app.app_context():
        from . import routes  # Importer les routes
        # from . import server # import du code en cours de refacto

        # chargement des données JSON
        data_loader = JSONLoader()
        clubs = data_loader.get_clubs()
        competitions = data_loader.get_competitions()

    return app
