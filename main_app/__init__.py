import os
from flask import Flask, g

from .services import JSONLoaderService, BookingService
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
        # si les données n'ont pas encore été chargées
        if 'clubs' not in g:
            load_service = JSONLoaderService()
            g.clubs = load_service.get_clubs()
            g.competitions = load_service.get_competitions()

            # on ajoute le statut (bool) pour savoir\
            # si la compétition a déjà eu lieu (false) ou est dans le futur (true)
            booking_service = BookingService(g.clubs, g.competitions)
            g.competitions = booking_service.add_future_status_to_competitions()

    return app
