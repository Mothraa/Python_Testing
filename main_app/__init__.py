import os
from flask import Flask, g

from .services import JSONLoader
from .routes import bp as main_app_bp


def create_app(config_filename='config.py'):
    app = Flask(__name__)

    # Chargement de la configuration
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(project_dir, config_filename)

    app.config.from_pyfile(config_path)

    app.register_blueprint(main_app_bp)

    @app.before_request
    def load_data():
        if 'clubs' not in g:
            data_loader = JSONLoader()
            g.clubs = data_loader.get_clubs()
            g.competitions = data_loader.get_competitions()

    # with app.app_context():
    #     print(app.url_map)  # for debug
    #     # data_loader = JSONLoader()
    #     # clubs = data_loader.get_clubs()
    #     # competitions = data_loader.get_competitions()

    return app
