
def test_integration(client, booking_service, json_loader_service, mock_clubs, mock_competitions):
    # page d'accueil
    response = client.get('/')
    assert response.status_code == 200

    # Identification de l'utilisateur + chargement de la page welcome
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})  # Utilisez l'email approprié
    assert b'Welcome, john@simplylift.co' in response.data  # Vérifie que le bon email est affiché
    assert b'Points available: 13' in response.data  # Vérifie que les points sont corrects

    # chargement de la page de reservation (booking)
    competition_name = 'Fall Classic 2025'
    club_name = 'Simply Lift'
    competition = booking_service.get_competition_by_name(competition_name)
    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200
    assert bytes(competition_name, 'utf-8') in response.data
    assert bytes(club_name, 'utf-8') in response.data
    assert bytes(str(competition['numberOfPlaces']), 'utf-8') in response.data

    # Post du formulaire de resa et retour sur la page d'accueil
    response = client.post('/purchasePlaces', data={'club': club_name, 'competition': competition_name, 'places': 1})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    assert b'Welcome, john@simplylift.co' in response.data

    # Test de deconnexion
    response = client.get('/logout', follow_redirects=True)
    assert b'Logout!' in response.data
    assert b'Welcome' in response.data
