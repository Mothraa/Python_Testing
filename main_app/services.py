import json

from flask import current_app


class JSONLoaderService:
    """ Load JSON datas from files of clubs and competitions"""
    clubs_path = None
    competitions_path = None

    def __init__(self):
        self.clubs_path = current_app.config['JSON_CLUBS_PATH']
        self.competitions_path = current_app.config['JSON_COMPETITIONS_PATH']

    def get_clubs(self):
        """Load clubs' list"""
        return self._load_data(self.clubs_path, 'clubs')

    def get_competitions(self):
        """Load competitions' list"""
        return self._load_data(self.competitions_path, 'competitions')

    def _load_data(self, filename, key):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            # on retourne une liste vide si clé non trouvée
            return data.get(key, [])
        except FileNotFoundError:
            raise Exception(f"Le fichier {filename} est introuvable")
        except json.JSONDecodeError:
            raise Exception(f"Erreur de decodage du fichier {filename}")


class JSONSaverService:
    pass


class BookingService:
    def __init__(self, clubs, competitions):
        self.clubs = clubs
        self.competitions = competitions

    def get_club_by_name(self, club_name):
        # TODO : a tester
        return next((c for c in self.clubs if c['name'] == club_name), None)

    def get_competition_by_name(self, competition_name):
        # TODO : a tester
        return next((c for c in self.competitions if c['name'] == competition_name), None)

    def has_enough_places(self, competition, places_required):
        return int(competition['numberOfPlaces']) >= places_required

    def update_competition_places(self, competition, places_required):
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
