from main_app.services import load_club_data, load_competition_data


def test_load_clubs(monkeypatch, mock_clubs):
    monkeypatch.setattr('main_app.services.load_club_data', lambda: mock_clubs)
    clubs = load_club_data()
    assert clubs == mock_clubs


def test_load_clubs_wrong_key(mock_json_with_wrong_key):
    clubs = load_club_data()
    assert clubs == []


def test_load_competitions(monkeypatch, mock_competitions):
    monkeypatch.setattr('main_app.services.load_competition_data', lambda: mock_competitions)
    competitions = load_competition_data()
    assert competitions == mock_competitions


def test_load_competitions_wrong_key(mock_json_with_wrong_key):
    competitions = load_competition_data()
    assert competitions == []
