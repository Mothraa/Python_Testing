from main_app.services import load_club_data, load_competition_data


def test_load_clubs(monkeypatch, mock_clubs):
    monkeypatch.setattr('main_app.services.load_club_data', lambda: mock_clubs)
    clubs = load_club_data()
    assert clubs == mock_clubs


def test_load_competitions(monkeypatch, mock_competitions):
    monkeypatch.setattr('main_app.services.load_competition_data', lambda: mock_competitions)
    clubs = load_competition_data()
    assert clubs == mock_competitions
