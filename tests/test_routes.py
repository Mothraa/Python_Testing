# memo : pas besoin d'importer les fixtures présentes dans conftest, pytest s'en charge !
# TODO : validation format email : (email-validator ou pyIsEmail ou par regex) en complément de la verif de base du template


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


def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' in response.data

    # # On verifie ensuite que l'accès est refusé - ou redir 302 (dans le cas de gestion de session)
    # response = client.get('/showSummary', follow_redirects=True)
    # assert response.status_code == 403 or response.status_code == 302
