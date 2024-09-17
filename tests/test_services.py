import pytest

from main_app.services import JSONLoaderService, BookingService


def test_load_clubs(app, json_loader, mock_clubs):
    with app.app_context():
        clubs = json_loader.get_clubs()
    assert clubs == mock_clubs


def test_load_competitions(app, json_loader, mock_competitions):
    with app.app_context():
        competitions = json_loader.get_competitions()
    assert competitions == mock_competitions


def test_load_clubs_wrong_key(app, monkeypatch, mock_json_with_wrong_key):
    loader = JSONLoaderService()
    monkeypatch.setattr(loader, '_load_data', lambda filename, key: [])
    clubs = loader.get_clubs()
    assert clubs == []


def test_load_competitions_wrong_key(app, monkeypatch, mock_json_with_wrong_key):
    loader = JSONLoaderService()
    monkeypatch.setattr(loader, '_load_data', lambda filename, key: [])
    competitions = loader.get_competitions()
    assert competitions == []


def test_load_clubs_file_not_found(app, monkeypatch, mock_open_missing_file):
    loader = JSONLoaderService()
    with pytest.raises(Exception):
        loader.get_clubs()


def test_load_competitions_file_not_found(app, monkeypatch, mock_open_missing_file):
    loader = JSONLoaderService()
    with pytest.raises(Exception):
        loader.get_competitions()


def test_load_clubs_json_decode_error(app, monkeypatch, mock_open_corrupted_file):
    loader = JSONLoaderService()
    with app.app_context():
        with pytest.raises(Exception):
            loader.get_clubs()


def test_load_competitions_json_decode_error(app, monkeypatch, mock_open_corrupted_file):
    loader = JSONLoaderService()
    with app.app_context():
        with pytest.raises(Exception):
            loader.get_competitions()


def test_club_points_are_integers(app):
    loader = JSONLoaderService()
    with app.app_context():
        clubs = loader.get_clubs()
    for club in clubs:
        points = club['points']
        assert isinstance(points, int)


def test_competitions_places_are_integers(app):
    loader = JSONLoaderService()
    with app.app_context():
        competitions = loader.get_competitions()
    for competition in competitions:
        places = competition['numberOfPlaces']
        assert isinstance(places, int)


def test_get_club_by_name(mock_clubs):
    service = BookingService(mock_clubs, [])
    result = service.get_club_by_name("Iron Temple")
    assert result == {"name": "Iron Temple", "email": "admin@irontemple.com", "points": 4}

    result = service.get_club_by_name("Fake Club")
    assert result is None


def test_get_competition_by_name(mock_competitions):
    service = BookingService([], mock_competitions)
    result = service.get_competition_by_name("Fall Classic")
    assert result == {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": 13}

    result = service.get_competition_by_name("Fake Competition")
    assert result is None


def test_has_enough_places(mock_competitions):
    service = BookingService([], mock_competitions)
    competition = service.get_competition_by_name("Spring Festival")  # 25 places
    assert service.has_enough_places(competition, 25) is True
    assert service.has_enough_places(competition, 26) is False
