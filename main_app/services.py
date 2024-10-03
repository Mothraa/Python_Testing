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
        """load json data from file"""
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
    """Services for booking places in competitions"""
    def __init__(self, clubs, competitions):
        self.clubs = clubs
        self.competitions = competitions
        self.max_places = current_app.config.get('MAX_PLACES')

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
        """check if the competition has enough places"""
        return int(competition['numberOfPlaces']) >= places_required

    def is_ok_with_max_places_limit(self, places_required):
        """check if the booking request is under the limit fixed"""
        return places_required <= self.max_places

    def has_enough_points(self, club, places_required):
        """check if the club has enough points"""
        return club['points'] >= places_required

    def add_future_status_to_competitions(self):
        """add the boolean attribut "competition_with_future_status to competitions data"""
        competitions_with_future_status = []
        for competition in self.competitions:
            competition_with_status = dict(competition)
            competition_with_status['is_competition_in_future'] = self.is_competition_in_future(competition)
            competitions_with_future_status.append(competition_with_status)
        return competitions_with_future_status

    def is_competition_in_future(self, competition) -> bool:
        """check if competition is past or in future"""
        competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        # TODO autoriser pour la date J+1 uniquement (sans heure) ? a spécifier.
        return competition_date > datetime.now()

    def get_reserved_places(self, bookings, club, competition) -> int:
        """Return number of places reserved by club for the competition"""
        existing_booking = self._find_existing_booking(bookings, competition)
        if not existing_booking:
            return 0  # si pas de réservation trouvée
        club_booking = next((cb for cb in existing_booking['clubs'] if cb['name'] == club['name']), {'places': 0})
        return club_booking['places']
        # if existing_booking and club['name'] in existing_booking['clubs']:
        #     return existing_booking['clubs'][club['name']]
        # return 0  # si pas de réservation trouvée

    def update_competition_places(self, competition, places_required):
        """update competition number of places"""
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required

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
        """Find a booking for a specified competition"""
        for booking in bookings.get('bookings', []):
            if booking['competition'] == competition['name']:
                return booking
        return None

    def _update_existing_booking(self, existing_booking, club, places_required):
        """update places number in case of club already reserved places for this tournament"""
        for club_reservation in existing_booking['clubs']:
            if club_reservation['name'] == club['name']:
                # update de la valeur
                club_reservation['places'] += places_required
                return True

    def _add_new_booking(self, bookings, club, competition, places_required):
        """Add a new book for a club (first booking for this tournament)"""
        new_booking = {
            "competition": competition['name'],
            "clubs": [
                {
                    "name": club['name'],
                    "places": places_required
                }
            ]
        }
        if 'bookings' not in bookings:
            bookings['bookings'] = []
        bookings['bookings'].append(new_booking)


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
        """load json data from file"""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        # TODO : autres exceptions ?
        except json.JSONDecodeError:
            raise Exception(f"Erreur de decodage de {filename}")

    def _save_data(self, filename, data):
        """save json data as file"""
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
