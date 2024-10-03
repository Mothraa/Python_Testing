import pytest
# memo : pas besoin d'importer les fixtures présentes dans conftest, pytest s'en charge !
# TODO : validation email : (email-validator ou pyIsEmail ou par regex) en complément de la verif de base du template


@pytest.mark.unit
def test_index_endpoint(client):
    """Check if we are on the right main page"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'GUDLFT Registration' in response.data


@pytest.mark.unit
def test_no_email(client):
    """test response when no email is POST"""
    # POST avec le champ email vide et on suit la redirection
    response = client.post('/showSummary', data={'email': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email not found' in response.data


@pytest.mark.unit
def test_email_valid(client, mock_clubs):
    """test response when a valid email is POST"""
    response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})
    assert response.status_code == 200
    assert b'Welcome, kate@shelifts.co.uk' in response.data


@pytest.mark.unit
def test_email_not_valid(client):
    """test response when a NOT valid email is POST"""
    response = client.post('/showSummary', data={'email': 'pipo@mail.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email not found' in response.data


@pytest.mark.unit
def test_purchase_places_in_a_past_competition(client, mocker, mock_clubs, mock_competitions, booking_service):
    """test when we try to book places in a past competition (forbidden case)"""
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


@pytest.mark.unit
def test_book_with_unknown_club(client, mock_clubs, mock_competitions):
    """test booking with an unknown club name"""
    response = client.get('/book/Spring Festival/fake_Club', follow_redirects=True)

    assert response.status_code == 200  # redirection
    assert b"Something went wrong-please try again" in response.data


@pytest.mark.unit
def test_book_with_unknown_competition(client, mock_clubs, mock_competitions):
    """test booking with an unknown competition name"""
    response = client.get('/book/fake_Competition/Simply Lift', follow_redirects=True)

    assert response.status_code == 200  # redirection
    assert b"Something went wrong-please try again" in response.data


@pytest.mark.unit
def test_logout(client):
    """logout test"""
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' in response.data
