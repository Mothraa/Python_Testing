import pytest

from main_app.services import JSONLoaderService, BookingService


# @pytest.fixture
# def booking_service(mock_clubs, mock_competitions):
#     return BookingService(clubs=mock_clubs, competitions=mock_competitions)  # mocks defined in conftest.py


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
    assert booking_service.is_competition_in_futur(future_competition) is True


def test_is_competition_in_past(app, mock_clubs, mock_competitions):
    booking_service = BookingService(mock_clubs, mock_competitions)
    past_competition = mock_competitions[0]  # Spring Festival (in past, 2020)
    assert booking_service.is_competition_in_futur(past_competition) is False
