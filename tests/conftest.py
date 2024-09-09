import pytest

from main_app import create_app
#from unittest.mock import MagicMock  # pour des objets complexes

@pytest.fixture
def client():
    """ For simulating client requests (GET/POST)"""
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_clubs():
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {   "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]


@pytest.fixture
def mock_competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]


@pytest.fixture
def mock_open_missing_file(monkeypatch):

    def mock_open(*args, **kwargs):
        raise FileNotFoundError
    
    monkeypatch.setattr('builtins.open', mock_open)


@pytest.fixture
def mock_open_corrupted_file(monkeypatch):

    def mock_open(*args, **kwargs):
        raise FileNotFoundError
    
    monkeypatch.setattr('builtins.open', mock_open)

# class TestClass:
#     def setup_method(self, method):
#         print("--> Setup method")

#     def teardown_method(self, method):
#         print("\n--> Teardown method")

#     def test_one(self):
#         print("--> Run first test")
