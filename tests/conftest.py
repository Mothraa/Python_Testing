import json

import pytest

from main_app import create_app
from main_app.services import JSONLoaderService, JSONSaverService, BookingService


@pytest.fixture
def minimal_app():
    """Create a minimal application instance for testing (erros loading datas)"""
    app = create_app()
    app.config.update({
        "TESTING": True
    })
    with app.app_context():
        yield app


@pytest.fixture
def app(monkeypatch, mock_clubs, mock_competitions):
    """Create an application instance for testing with mocked data"""
    # Mock JSONLoaderService pour retourner les données mockées au lieu de lire des fichiers
    def mock_get_clubs(self):
        return mock_clubs

    def mock_get_competitions(self):
        return mock_competitions

    monkeypatch.setattr('main_app.services.JSONLoaderService.get_clubs', mock_get_clubs)
    monkeypatch.setattr('main_app.services.JSONLoaderService.get_competitions', mock_get_competitions)

    # Creation de l'app et de la conf
    app = create_app()
    app.config.update({
        "TESTING": True
    })

    with app.app_context():
        yield app


@pytest.fixture
def client():
    """ For simulating client requests (GET/POST) """
    app = create_app()
    app.config.update({
        "TESTING": True
    })
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_clubs():
    return [
        {
            "name": "Simply Lift Mock",
            "email": "john@simplylift.co",
            "points": 13
        },
        {
            "name": "Iron Temple Mock",
            "email": "admin@irontemple.com",
            "points": 4
        },
        {
            "name": "She Lifts Mock",
            "email": "kate@shelifts.co.uk",
            "points": 12
        }
    ]


@pytest.fixture
def mock_competitions():
    return [
        {
            "name": "Spring Festival Mock",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": 25
        },
        {
            "name": "Fall Classic Mock",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": 13
        },
        {
            "name": "Fall Classic 2025 Mock",
            "date": "2025-10-22 13:30:00",
            "numberOfPlaces": 13
        }
    ]


@pytest.fixture
def mock_bookings():
    return {
        "bookings": [
            {
                "competition": "Fall Classic 2025 Mock",
                "clubs": [
                    {
                        "name": "Simply Lift Mock",
                        "places": 5
                    },
                    {
                        "name": "Iron Temple Mock",
                        "places": 3
                    }
                ]
            },
            {
                "competition": "Spring Festival Mock",
                "clubs": [
                    {
                        "name": "She Lifts Mock",
                        "places": 7
                    }
                ]
            }
        ]
    }


@pytest.fixture
def mock_open_corrupted_file(monkeypatch):
    """Mock fixture to simulate a corrupted json file"""
    def mock_open(*args, **kwargs):
        raise json.JSONDecodeError("Expecting value", "document", 0)

    monkeypatch.setattr('builtins.open', mock_open)


@pytest.fixture
def json_loader_service(app, monkeypatch, mock_clubs, mock_competitions, mock_bookings):
    """ Mock fixture to simulate services.JSONLoaderService"""
    with app.app_context():

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


@pytest.fixture
def json_saver_service(app, monkeypatch):
    """Mock fixture for instanciate JSONSaverService"""
    with app.app_context():
        saver_service = JSONSaverService()

        # Mock de la méthode _update_data avec la bonne signature
        def mock_update_data(self, filename, key, new_data):
            print(f"Mock update_data for {key}: {new_data}")  # Simule l'enregistrement
            return {key: new_data}  # Simule une structure JSON avec les données mises à jour

        # Mock de la méthode _save_data pour éviter la sauvegarde réelle
        def mock_save_data(self, filename, data):
            print(f"Mock save_data: writing to {filename} with data: {data}")  # Simule l'écriture des données

        # Patch la méthode _update_data avec la bonne signature
        monkeypatch.setattr(JSONSaverService, '_update_data', mock_update_data)
        monkeypatch.setattr(JSONSaverService, '_save_data', mock_save_data)

        return saver_service


@pytest.fixture
def booking_service(app, mock_clubs, mock_competitions):
    """fixture for instanciate BookingService"""
    with app.app_context():
        return BookingService(clubs=mock_clubs, competitions=mock_competitions)
