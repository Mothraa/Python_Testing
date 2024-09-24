# memo : pas besoin d'importer les fixtures présentes dans conftest, pytest s'en charge !
# TODO : validation email : (email-validator ou pyIsEmail ou par regex) en complément de la verif de base du template


def test_index_status_code(client):
    response = client.get('/')
    assert response.status_code == 200


def test_index_read_content(client):
    """ Check if we are on the right page """
    response = client.get('/')
    assert b'GUDLFT Registration' in response.data


def test_no_email(client):
    # POST avec le champ email vide et on suit la redirection
    response = client.post('/showSummary', data={'email': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email not found' in response.data


def test_email_valid(client, mock_clubs):
    response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})
    assert response.status_code == 200
    assert b'Welcome, kate@shelifts.co.uk' in response.data


def test_email_not_valid(client):
    response = client.post('/showSummary', data={'email': 'pipo@mail.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email not found' in response.data


def test_purchase_places_in_a_past_competition(client, mocker, mock_clubs, mock_competitions, booking_service):
    # On simule une compétition dans le passé
    club = mock_clubs[0]
    competition = mock_competitions[0]
    mocker.patch.object(booking_service, 'is_competition_in_future', return_value=False)

    # données pour la requete
    data = {
        'club': club['name'],
        'competition': competition['name'],
        'places': 1
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)

    assert b"Competition already past" in response.data
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_booking_reservation_is_ok(client, json_loader_service, mock_clubs, mock_competitions, mock_bookings):
    """ mock a valid places reservation"""
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Fall Classic 2025',
        'places': '2'
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data


def test_book_club_and_competition_ok(client, mock_clubs, mock_competitions):
    """Test pour un club et une compétition existants."""
    response = client.get('/book/Spring Festival/Simply Lift')

    assert response.status_code == 200
    assert b'Simply Lift' in response.data
    assert b'Spring Festival' in response.data


def test_book_with_unknown_club(client, mock_clubs, mock_competitions):
    """Test pour un club inexistant."""
    response = client.get('/book/Spring Festival/fake_Club', follow_redirects=True)

    assert response.status_code == 200  # redirection
    assert b"Something went wrong-please try again" in response.data


def test_book_with_unknown_competition(client, mock_clubs, mock_competitions):
    """Test pour une compétition inexistante."""
    response = client.get('/book/fake_Competition/Simply Lift', follow_redirects=True)

    assert response.status_code == 200  # redirection
    assert b"Something went wrong-please try again" in response.data


def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' in response.data
