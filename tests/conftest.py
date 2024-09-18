import json
from unittest.mock import mock_open
#from unittest.mock import MagicMock  # pour des objets complexes

import pytest

from main_app import create_app
from main_app.services import JSONLoaderService


@pytest.fixture
def app():
    """Create an application instance for testing"""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        yield app


@pytest.fixture
def client():
    """ For simulating client requests (GET/POST)
        for routing or integrating tests """
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_clubs():
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": 13
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": 4
        },
        {   "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": 12
        }
    ]


@pytest.fixture
def mock_competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": 25
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": 13
        },
        {
            "name": "Fall Classic 2025",
            "date": "2025-10-22 13:30:00",
            "numberOfPlaces": 13
        }
    ]


@pytest.fixture
def mock_bookings():
    return {
            "competition_a": {
                "club1": 5,
                "club2": 3
            },
            "competition_b": {
                "club1": 1,
                "club3": 2,
                "club4": 8
            },
            "competition_c": {
                "club1": 6,
                "club2": 4
            }
            }


@pytest.fixture
def mock_open_missing_file(monkeypatch):

    def mock_open(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr('builtins.open', mock_open)


@pytest.fixture
def mock_open_corrupted_file(monkeypatch):

    def mock_open(*args, **kwargs):
        raise json.JSONDecodeError("Expecting value", "document", 0)

    monkeypatch.setattr('builtins.open', mock_open)


@pytest.fixture
def mock_json_with_wrong_key(monkeypatch):
    json_data = json.dumps({"wrong_key": "value_we_dont_care"})
    monkeypatch.setattr('builtins.open', mock_open(read_data=json_data))


@pytest.fixture
def json_loader(app, monkeypatch, mock_clubs, mock_competitions, mock_bookings):
    """ Fixture to simulate services.JSONLoaderService"""
    with app.app_context():
        # Simulation du chemin des fichiers json dans app.config
        app.config['json_clubs_path'] = 'repertory/mock_clubs.json'
        app.config['json_competitions_path'] = 'repertory/mock_competitions.json'
        app.config['json_booking_path'] = 'repertory/mock_booking.json'


        # for mocking JSONLoaderService._load_data
        def mock_load_data(self, filename, key):
            if key == 'clubs':
                return mock_clubs
            elif key == 'competitions':
                return mock_competitions
            elif key == 'bookings':
                return mock_bookings
            return []

        monkeypatch.setattr(JSONLoaderService, '_load_data', mock_load_data)

    return JSONLoaderService()
