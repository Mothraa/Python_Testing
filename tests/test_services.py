import pytest

from main_app.services import JSONLoaderService, BookingService


@pytest.mark.unit
def test_load_clubs(app, json_loader_service, mock_clubs):
    with app.app_context():
        clubs = json_loader_service.get_clubs()
    assert clubs == mock_clubs


@pytest.mark.unit
def test_load_competitions(app, json_loader_service, mock_competitions):
    with app.app_context():
        competitions = json_loader_service.get_competitions()
    assert competitions == mock_competitions


@pytest.mark.unit
def test_load_bookings(app, json_loader_service, mock_bookings):
    with app.app_context():
        bookings = json_loader_service.get_bookings()
    assert bookings == mock_bookings


@pytest.mark.unit
def test_load_clubs_file_not_found(minimal_app, monkeypatch):
    """Testing FileNotFoundError exception when json clubs file is not found"""

    # on simule l'ouverture d'un fichier non trouvé
    def mock_open_missing_file(*args, **kwargs):
        raise FileNotFoundError("Fichier non trouvé")
    monkeypatch.setattr('builtins.open', mock_open_missing_file)

    # on utilise d'un contexte d'app réduit (pour ne pas charger les données via l'app)
    with minimal_app.app_context():
        loader = JSONLoaderService()
        with pytest.raises(Exception, match="Le fichier .* est introuvable"):
            loader.get_clubs()


@pytest.mark.unit
def test_load_competitions_file_not_found(minimal_app, monkeypatch):
    """Testing FileNotFoundError exception when json competitions file is not found"""

    # on simule l'ouverture d'un fichier non trouvé
    def mock_open_missing_file(*args, **kwargs):
        raise FileNotFoundError("Fichier non trouvé")
    monkeypatch.setattr('builtins.open', mock_open_missing_file)

    # on utilise d'un contexte d'app réduit (pour ne pas charger les données via l'app)
    with minimal_app.app_context():
        loader = JSONLoaderService()
        with pytest.raises(Exception, match="Le fichier .* est introuvable"):
            loader.get_competitions()


@pytest.mark.unit
def test_load_bookings_file_not_found(minimal_app, monkeypatch):
    """Testing FileNotFoundError exception when json bookings file is not found"""

    # on simule l'ouverture d'un fichier non trouvé
    def mock_open_missing_file(*args, **kwargs):
        raise FileNotFoundError("Fichier non trouvé")
    monkeypatch.setattr('builtins.open', mock_open_missing_file)

    # on utilise d'un contexte d'app réduit (pour ne pas charger les données via l'app)
    with minimal_app.app_context():
        loader = JSONLoaderService()
        with pytest.raises(Exception, match="Le fichier .* est introuvable"):
            loader.get_bookings()


@pytest.mark.unit
def test_load_clubs_json_decode_error(minimal_app, monkeypatch, mock_open_corrupted_file):
    """Testing exception when json clubs file is corrupted"""
    loader = JSONLoaderService()
    with minimal_app.app_context():
        with pytest.raises(Exception):
            loader.get_clubs()


@pytest.mark.unit
def test_load_competitions_json_decode_error(minimal_app, monkeypatch, mock_open_corrupted_file):
    """Testing exception when json competitions file is corrupted"""
    loader = JSONLoaderService()
    with minimal_app.app_context():
        with pytest.raises(Exception):
            loader.get_competitions()


@pytest.mark.unit
def test_load_bookings_json_decode_error(minimal_app, monkeypatch, mock_open_corrupted_file):
    """Testing exception when json bookings file is corrupted"""
    loader = JSONLoaderService()
    with minimal_app.app_context():
        with pytest.raises(Exception):
            loader.get_bookings()


@pytest.mark.unit
def test_get_club_by_name(app, mock_clubs):
    """Test function to get club informations by name"""
    booking_service = BookingService(mock_clubs, [])
    result = booking_service.get_club_by_name("Iron Temple Mock")
    assert result == {"name": "Iron Temple Mock", "email": "admin@irontemple.com", "points": 4}

    result = booking_service.get_club_by_name("Fake Club")
    assert result is None


@pytest.mark.unit
def test_get_competition_by_name(app, mock_competitions):
    """Test function to get competition informations by name"""
    booking_service = BookingService([], mock_competitions)
    result = booking_service.get_competition_by_name("Fall Classic Mock")
    assert result == {"name": "Fall Classic Mock", "date": "2020-10-22 13:30:00", "numberOfPlaces": 13}

    result = booking_service.get_competition_by_name("Fake Competition")
    assert result is None


@pytest.mark.unit
def test_has_enough_places(app, mock_competitions):
    """Test the function which checks the number of places available"""
    booking_service = BookingService([], mock_competitions)
    competition = booking_service.get_competition_by_name("Spring Festival Mock")  # 25 places
    assert booking_service.has_enough_places(competition, 25) is True
    assert booking_service.has_enough_places(competition, 26) is False


@pytest.mark.unit
def test_has_enough_points(app, mock_clubs):
    """test of the function which checks that the club has enough points to book"""
    booking_service = BookingService(mock_clubs, [])
    # 'Iron Temple' => 4 points
    club = booking_service.get_club_by_name('Iron Temple Mock')
    result = booking_service.has_enough_points(club, 3)
    assert result is True
    club = booking_service.get_club_by_name('Iron Temple Mock')
    result = booking_service.has_enough_points(club, 5)
    assert result is False


@pytest.mark.unit
def test_with_max_places_limit(app):
    """test of the function which checks the limit of booking places"""
    # instanciation sans données juste pour appeler la methode
    booking_service = BookingService([], [])
    # Dans le cas ou MAX_PLACES is 12
    assert booking_service.is_ok_with_max_places_limit(11) is True
    assert booking_service.is_ok_with_max_places_limit(13) is False


@pytest.mark.unit
def test_is_competition_in_the_future_or_past(app, mock_clubs, mock_competitions):
    """test of the function which checks if the competition is in the future"""
    booking_service = BookingService(mock_clubs, mock_competitions)
    future_competition = mock_competitions[2]  # Fall Classic 2025 (in future)
    past_competition = mock_competitions[0]  # Spring Festival (in past, 2020)
    assert booking_service.is_competition_in_future(future_competition) is True
    assert booking_service.is_competition_in_future(past_competition) is False
