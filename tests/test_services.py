import json

import pytest
from unittest.mock import MagicMock  # pour mocker des objets complexes (ou methodes)

from main_app.services import JSONLoaderService, BookingService


def test_load_clubs(app, json_loader_service, mock_clubs):
    with app.app_context():
        clubs = json_loader_service.get_clubs()
    assert clubs == mock_clubs


def test_load_competitions(app, json_loader_service, mock_competitions):
    with app.app_context():
        competitions = json_loader_service.get_competitions()
    assert competitions == mock_competitions


def test_load_bookings(app, json_loader_service, mock_bookings):
    with app.app_context():
        bookings = json_loader_service.get_bookings()
    assert bookings == mock_bookings


def test_load_clubs_wrong_key(app, monkeypatch, mock_json_with_wrong_key):
    loader = JSONLoaderService()
    monkeypatch.setattr(loader, '_load_data', lambda filename, key: None)
    clubs = loader.get_clubs()
    assert clubs is None


def test_load_competitions_wrong_key(app, monkeypatch, mock_json_with_wrong_key):
    loader = JSONLoaderService()
    monkeypatch.setattr(loader, '_load_data', lambda filename, key: None)
    competitions = loader.get_competitions()
    assert competitions is None


def test_load_bookings_wrong_key(app, monkeypatch, mock_json_with_wrong_key):
    loader = JSONLoaderService()
    monkeypatch.setattr(loader, '_load_data', lambda filename, key: None)
    bookings = loader.get_bookings()
    assert bookings is None


def test_load_clubs_file_not_found(app, monkeypatch, mock_open_missing_file):
    loader = JSONLoaderService()
    with pytest.raises(Exception):
        loader.get_clubs()


def test_load_competitions_file_not_found(app, monkeypatch, mock_open_missing_file):
    loader = JSONLoaderService()
    with pytest.raises(Exception):
        loader.get_competitions()


def test_load_bookings_file_not_found(app, monkeypatch, mock_open_missing_file):
    loader = JSONLoaderService()
    with pytest.raises(Exception):
        loader.get_bookings()


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


def test_load_bookings_json_decode_error(app, monkeypatch, mock_open_corrupted_file):
    loader = JSONLoaderService()
    with app.app_context():
        with pytest.raises(Exception):
            loader.get_bookings()


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


def test_get_club_by_name(app, mock_clubs):
    booking_service = BookingService(mock_clubs, [])
    result = booking_service.get_club_by_name("Iron Temple")
    assert result == {"name": "Iron Temple", "email": "admin@irontemple.com", "points": 4}

    result = booking_service.get_club_by_name("Fake Club")
    assert result is None


def test_get_competition_by_name(app, mock_competitions):
    booking_service = BookingService([], mock_competitions)
    result = booking_service.get_competition_by_name("Fall Classic")
    assert result == {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": 13}

    result = booking_service.get_competition_by_name("Fake Competition")
    assert result is None


def test_has_enough_places(app, mock_competitions):
    booking_service = BookingService([], mock_competitions)
    competition = booking_service.get_competition_by_name("Spring Festival")  # 25 places
    assert booking_service.has_enough_places(competition, 25) is True
    assert booking_service.has_enough_places(competition, 26) is False


def test_has_enough_points(app, mock_clubs):
    booking_service = BookingService(mock_clubs, [])
    # 'Iron Temple' => 4 points
    club = booking_service.get_club_by_name('Iron Temple')
    result = booking_service.has_enough_points(club, 3)
    assert result is True
    club = booking_service.get_club_by_name('Iron Temple')
    result = booking_service.has_enough_points(club, 5)
    assert result is False


def test_with_max_places_under_limit(app):
    # instanciation sans données juste pour appeler la methode
    booking_service = BookingService([], [])
    # Dans le cas ou MAX_PLACES is 12
    assert booking_service.is_ok_with_max_places_limit(11) is True


def test_with_max_places_exceed_limit(app):
    # instanciation sans données juste pour appeler la methode
    booking_service = BookingService([], [])
    # Dans le cas ou MAX_PLACES is 12
    assert booking_service.is_ok_with_max_places_limit(13) is False


def test_is_competition_in_future(app, mock_clubs, mock_competitions):
    booking_service = BookingService(mock_clubs, mock_competitions)
    future_competition = mock_competitions[2]  # Fall Classic 2025 (in future)
    assert booking_service.is_competition_in_future(future_competition) is True


def test_is_competition_in_past(app, mock_clubs, mock_competitions):
    booking_service = BookingService(mock_clubs, mock_competitions)
    past_competition = mock_competitions[0]  # Spring Festival (in past, 2020)
    assert booking_service.is_competition_in_future(past_competition) is False


def test_save_clubs(json_saver_service, mock_clubs, mock_open_file, monkeypatch):
    """Test saving clubs in json file"""
    # On mock la fonction builtin open
    monkeypatch.setattr('builtins.open', mock_open_file)
    # mock de json.dump avec monkeypatch
    mock_json_dump = MagicMock()
    monkeypatch.setattr(json, 'dump', mock_json_dump)
    # mock de _load_data pour ne pas lire le fichier
    mock_existing_data = {'clubs': []}
    monkeypatch.setattr(json_saver_service, '_load_data', lambda filename: mock_existing_data)

    # on appelle la methode a tester : save_clubs
    json_saver_service.save_clubs(mock_clubs)

    # On verifie que le fichier a été ouvert correctement
    mock_open_file.assert_called_once_with(json_saver_service.clubs_path, 'w')
    # On vérifie que l'ensemble des methodes interne est appelé correctement
    expected_data = {'clubs': mock_clubs}
    mock_json_dump.assert_called_once_with(expected_data, mock_open_file(), indent=4)


def test_save_competitions(json_saver_service, mock_competitions, mock_open_file, monkeypatch):
    """Test saving competitions in json file"""
    # On mock la fonction open
    monkeypatch.setattr('builtins.open', mock_open_file)
    # On mock de json.dump
    mock_json_dump = MagicMock()
    monkeypatch.setattr(json, 'dump', mock_json_dump)
    # On mock _update_data
    mock_updated_data = {'competitions': mock_competitions}
    monkeypatch.setattr(json_saver_service, '_update_data', lambda path, key, data: mock_updated_data)
    # On mock _clean_competitions (nettoyage de la donnée)
    mock_clean_competitions = MagicMock()
    monkeypatch.setattr(json_saver_service, '_clean_competitions', mock_clean_competitions)

    # on appelle la methode a tester : save_competitions
    json_saver_service.save_competitions(mock_competitions)

    # On verifie que le fichier est bien ouvert en mode écriture
    mock_open_file.assert_called_once_with(json_saver_service.competitions_path, 'w')
    # On vérifie que _clean_competitions est correctement appelé (bonnes données)
    mock_clean_competitions.assert_called_once_with(mock_competitions)
    # On vérifie que l'ensemble des methodes interne est appelé correctement
    expected_data = {'competitions': mock_competitions}
    mock_json_dump.assert_called_once_with(expected_data, mock_open_file(), indent=4)


def test_save_bookings(json_saver_service, mock_bookings, mock_open_file, monkeypatch):
    """Test saving bookings in json file"""
    # On mock la fonction open
    monkeypatch.setattr('builtins.open', mock_open_file)
    # On mock de json.dump
    mock_json_dump = MagicMock()
    monkeypatch.setattr(json, 'dump', mock_json_dump)
    # On mock _update_data
    mock_updated_data = {'bookings': mock_bookings}
    monkeypatch.setattr(json_saver_service, '_update_data', lambda path, key, data: mock_updated_data)

    # on appelle la methode a tester : save_bookings
    json_saver_service.save_bookings(mock_bookings)

    # On verifie que le fichier est bien ouvert en mode écriture
    mock_open_file.assert_called_once_with(json_saver_service.bookings_path, 'w')
    # On vérifie que l'ensemble des methodes interne est appelé correctement
    expected_data = {'bookings': mock_bookings}
    mock_json_dump.assert_called_once_with(expected_data, mock_open_file(), indent=4)
