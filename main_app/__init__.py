from flask import Flask
# from .db_init import init_db


def create_app(config_filename='config.py'):
    app = Flask(__name__)

    # Charger la configuration de l'application depuis config.py
    app.config.from_object('config')  # 'config' est le nom du module de configuration

    # Importer et enregistrer les routes et les vues
    with app.app_context():
        from . import routes  # Importer les routes
        # Initialiser la base de données ici, si nécessaire
        # from .db_init import init_db
        # init_db(app)

    # TODO chargement des données JSON
    return app
