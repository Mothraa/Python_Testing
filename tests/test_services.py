import pytest

from main_app.services import JSONLoader


def test_load_clubs(app, json_loader, mock_clubs):
    with app.app_context():
        clubs = json_loader.get_clubs()
    assert clubs == mock_clubs


def test_load_competitions(app, json_loader, mock_competitions):
    with app.app_context():
        competitions = json_loader.get_competitions()
    assert competitions == mock_competitions


def test_load_clubs_wrong_key(app, monkeypatch, mock_json_with_wrong_key):
    loader = JSONLoader()
    monkeypatch.setattr(loader, '_load_data', lambda filename, key: [])
    clubs = loader.get_clubs()
    assert clubs == []


def test_load_competitions_wrong_key(app, monkeypatch, mock_json_with_wrong_key):
    loader = JSONLoader()
    monkeypatch.setattr(loader, '_load_data', lambda filename, key: [])
    competitions = loader.get_competitions()
    assert competitions == []


def test_load_clubs_file_not_found(app, monkeypatch, mock_open_missing_file):
    loader = JSONLoader()
    with pytest.raises(Exception):
        loader.get_clubs()


def test_load_competitions_file_not_found(app, monkeypatch, mock_open_missing_file):
    loader = JSONLoader()
    with pytest.raises(Exception):
        loader.get_competitions()


def test_load_clubs_json_decode_error(app, monkeypatch, mock_open_corrupted_file):
    loader = JSONLoader()
    with app.app_context():
        with pytest.raises(Exception):
            loader.get_clubs()


def test_load_competitions_json_decode_error(app, monkeypatch, mock_open_corrupted_file):
    loader = JSONLoader()
    with app.app_context():
        with pytest.raises(Exception):
            loader.get_competitions()


def test_club_points_are_integers(app):
    loader = JSONLoader()
    with app.app_context():
        clubs = loader.get_clubs()
    for club in clubs:
        points = club['points']
        assert isinstance(points, int)
