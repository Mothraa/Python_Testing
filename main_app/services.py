import json
import copy
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
        """Load clubs"""
        return self._load_data(self.clubs_path, 'clubs')

    def get_competitions(self):
        """Load competitions"""
        return self._load_data(self.competitions_path, 'competitions')

    def get_bookings(self):
        """Load bookings"""
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
        # self.data_loader = JSONLoaderService()

    def get_club_by_name(self, club_name):
        """returns a club from its name"""
        for club in self.clubs:
            if club['name'] == club_name:
                return club
        return None

    def get_competition_by_name(self, competition_name):
        """returns a competition from its name"""
        for competition in self.competitions:
            if competition['name'] == competition_name:
                return competition
        return None

    def has_enough_places(self, competition, places_required):
        return int(competition['numberOfPlaces']) >= places_required

    def is_ok_with_max_places_limit(self, places_required):
        return places_required <= self.max_places

    def has_enough_points(self, club, places_required):
        return club['points'] >= places_required

    def update_competition_places(self, competition, places_required):
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required

    def is_competition_in_future(self, competition) -> bool:
        competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        # TODO autoriser pour la date J+1 uniquement (sans heure) ?
        return competition_date > datetime.now()

    def add_future_status_to_competitions(self):
        """add the attribut "competition_wit"""
        competitions_with_future_status = []
        for competition in self.competitions:
            competition_with_status = dict(competition)
            competition_with_status['is_competition_in_future'] = self.is_competition_in_future(competition)
            competitions_with_future_status.append(competition_with_status)
        return competitions_with_future_status

    def get_reserved_places(self, bookings, club, competition) -> int:
        """Return number of places reserved by club for the competition"""
        existing_booking = self._find_existing_booking(bookings, competition)
        if existing_booking and club['name'] in existing_booking['clubs']:
            return existing_booking['clubs'][club['name']]
        return 0  # si pas de réservation trouvée

    def handle_bookings(self, club, competition, places_required, bookings):
        """Handle bookings..."""
        existing_booking = self._find_existing_booking(bookings, competition)
        # si des réservations sont déjà existantes pour cette compétition et ce club
        if existing_booking:
            self._update_existing_booking(existing_booking, club, places_required)
        # si c'est une nouvelle réservation pour la compétition
        else:
            self._add_new_booking(bookings, club, competition, places_required)

        return bookings

    def _find_existing_booking(self, bookings, competition):
        """Trouve une réservation existante pour la compétition donnée"""
        # for booking in bookings:
        #     if booking['competition'] == competition['name']:
        #         return booking

        competition_name = competition['name']  # Assure-toi d'extraire le nom de la compétition
        # if competition_name in bookings:
        #     return bookings[competition_name]
        # return None
        return bookings.get(competition_name, None)

    def _update_existing_booking(self, existing_booking, club, places_required):
        """Met à jour le nombre de places réservées pour un club existant."""
        # si le club a déjà pris des places pour le tournoi
        if club['name'] in existing_booking['clubs']:
            existing_booking['clubs'][club['name']] += places_required
        # si le tournoi a déjà des places reservées (par d'autres clubs)\
        # mais que le club n'a pas encore reservé de place
        else:
            existing_booking['clubs'][club['name']] = places_required

    def _add_new_booking(self, bookings, club, competition, places_required):
        """Add a new book for a club"""
        competition_name = competition['name']
        bookings[competition_name] = {'clubs': {}}
        bookings[competition_name]['clubs'][club['name']] = places_required


class JSONSaverService:
    def __init__(self):
        self.clubs_path = current_app.config['JSON_CLUBS_PATH']
        self.competitions_path = current_app.config['JSON_COMPETITIONS_PATH']
        self.bookings_path = current_app.config['JSON_BOOKINGS_PATH']

    def save_clubs(self, clubs):
        """Save clubs"""
        updated_data = self._update_data(self.clubs_path, 'clubs', clubs)
        self._save_data(self.clubs_path, updated_data)

    def save_competitions(self, competitions):
        """Save competitions"""
        competitions_copy = copy.deepcopy(competitions)  # copie pour éviter d'ecraser g.competitions
        self._clean_competitions(competitions_copy)
        updated_data = self._update_data(self.competitions_path, 'competitions', competitions_copy)
        self._save_data(self.competitions_path, updated_data)

    def save_bookings(self, bookings):
        """Save bookings"""
        updated_data = self._update_data(self.bookings_path, 'bookings', bookings)
        self._save_data(self.bookings_path, updated_data)

    def _load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        # TODO : autres exceptions ?
        except json.JSONDecodeError:
            raise Exception(f"Erreur de decodage de {filename}")

    def _save_data(self, filename, data):
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        # TODO : autres exceptions ?
        except IOError as e:
            raise Exception(f"Erreur de sauvegarde de {filename}: {e}")

    def _update_data(self, filename, key, new_data):
        """ load existing data and return updated datas"""
        existing_data = self._load_data(filename)
        existing_data[key] = new_data
        return existing_data

    def _clean_competitions(self, competitions):
        """delete 'is_competition_in_future' (clean data before saving)"""
        for competition in competitions:
            competition.pop("is_competition_in_future", None)
