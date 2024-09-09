from main_app.services import loadClubs, loadCompetitions


def test_load_clubs(monkeypatch, mock_clubs):
    monkeypatch.setattr('main_app.services.loadClubs', lambda: mock_clubs)
    clubs = loadClubs()
    assert clubs == mock_clubs


def test_competitions(monkeypatch, mock_competitions):
    monkeypatch.setattr('main_app.services.loadCompetitions', lambda: mock_competitions)
    clubs = loadCompetitions()
    assert clubs == mock_competitions
