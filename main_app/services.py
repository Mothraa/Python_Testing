import json
from datetime import datetime

from flask import current_app


class JSONLoaderService:
    """ Load JSON datas from files of clubs and competitions"""
    clubs_path = None
    competitions_path = None
    bookings_path = None

    def __init__(self):
        self.clubs_path = current_app.config['JSON_CLUBS_PATH']
        self.competitions_path = current_app.config['JSON_COMPETITIONS_PATH']
        self.bookings_path = current_app.config['JSON_BOOKINGS_PATH']

    def get_clubs(self):
        """Load clubs' list"""
        return self._load_data(self.clubs_path, 'clubs')

    def get_competitions(self):
        """Load competitions' list"""
        return self._load_data(self.competitions_path, 'competitions')

    def get_bookings(self):
        """Load bookings' dict"""
        return self._load_data(self.bookings_path, 'bookings')

    def _load_data(self, filename, key):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            # on retourne None si clé non trouvée
            return data.get(key, None)
        except FileNotFoundError:
            raise Exception(f"Le fichier {filename} est introuvable")
        except json.JSONDecodeError:
            raise Exception(f"Erreur de decodage de {filename}")


class BookingService:
    def __init__(self, clubs, competitions):
        self.clubs = clubs
        self.competitions = competitions
        self.max_places = current_app.config.get('MAX_PLACES')

    def get_club_by_name(self, club_name):
        return next((c for c in self.clubs if c['name'] == club_name), None)

    def get_competition_by_name(self, competition_name):
        return next((c for c in self.competitions if c['name'] == competition_name), None)

    def has_enough_places(self, competition, places_required):
        return int(competition['numberOfPlaces']) >= places_required

    def is_ok_with_max_places_limit(self, places_required):
        return places_required <= self.max_places

    def has_enough_points(self, club, places_required):
        return club['points'] >= places_required

    def update_competition_places(self, competition, places_required):
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required

    def is_competition_in_future(self, competition):
        competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        return competition_date > datetime.now()


class JSONSaverService:
    def __init__(self, clubs_path, competitions_path, bookings_path):
        self.clubs_path = clubs_path
        self.competitions_path = competitions_path
        self.bookings_path = bookings_path

    def save_clubs(self, clubs):
        """Save clubs"""
        data = self._load_data(self.clubs_path)  # on récupère les données existantes
        data['clubs'] = clubs  # maj du dict data avec les données de clubs
        self._save_data(self.clubs_path, 'clubs', data)  # sauvegarde du fichier

    def save_competitions(self, competitions):
        """Save competitions"""
        data = self._load_data(self.competitions_path)  # on récupère les données existantes
        data['competitions'] = competitions  # maj des données
        self._save_data(self.competitions_path, 'competitions', data)  # sauvegarde du fichier

    def _load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        # TODO : autres exceptions ?
        except json.JSONDecodeError:
            raise Exception(f"Erreur de decodage de {filename}")

    def _save_data(self, filename, key, data):
        try:
            with open(filename, 'w') as f:
                json.dump({key: data}, f, indent=4)
        # TODO : autres exceptions ?
        except IOError as e:
            raise Exception(f"Erreur de sauvegarde de {filename}: {e}")
